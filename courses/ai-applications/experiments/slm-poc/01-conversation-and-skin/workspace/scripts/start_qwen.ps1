param(
    [string]$ServerPath = '',
    [int]$Port = 18080,
    [int]$ContextSize = 8192,
    [string]$LoraPath = ''
)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$modelPath = Join-Path $projectRoot 'models/qwen2.5-3b-instruct/qwen2.5-3b-instruct-q4_k_m.gguf'
$templatePath = Join-Path $projectRoot 'models/qwen2.5-3b-instruct/chat_template.jinja'
$runtimeDir = Join-Path $projectRoot 'output/runtime'
$pidFile = Join-Path $runtimeDir 'qwen-server.pid'
if ($LoraPath) {
    $LoraPath = [System.IO.Path]::GetFullPath((Join-Path $projectRoot $LoraPath))
    if (-not (Test-Path -LiteralPath $LoraPath)) { throw 'LoRA GGUF file not found.' }
}
if (-not (Test-Path -LiteralPath $modelPath)) { throw 'Run python scripts/setup_qwen.py first.' }
if (-not $ServerPath) {
    $engineRoot = Join-Path $env:APPDATA 'Jan/data/llamacpp/backends'
    $ServerPath = Get-ChildItem -LiteralPath $engineRoot -Recurse -Filter 'llama-server.exe' -ErrorAction SilentlyContinue |
        Where-Object { $_.FullName -match 'win-cuda' } |
        Sort-Object FullName -Descending | Select-Object -First 1 -ExpandProperty FullName
}
if (-not $ServerPath -or -not (Test-Path -LiteralPath $ServerPath)) {
    throw 'GPU llama-server.exe not found. Supply -ServerPath with a trusted llama.cpp Windows CUDA binary.'
}
New-Item -ItemType Directory -Force -Path $runtimeDir | Out-Null
if (Test-Path -LiteralPath $pidFile) {
    $existingPid = [int](Get-Content -LiteralPath $pidFile -Raw)
    $existing = Get-CimInstance Win32_Process -Filter "ProcessId = $existingPid"
    if ($existing -and $existing.ExecutablePath -eq $ServerPath -and $existing.CommandLine.Contains($modelPath)) {
        $config = Get-Content -LiteralPath (Join-Path $runtimeDir 'server_config.json') -Raw | ConvertFrom-Json
        if ([string]$config.adapter -ne $LoraPath -or [int]$config.port -ne $Port) {
            throw 'Existing project server has different adapter/port; stop it first.'
        }
        Write-Output "Existing project server PID $existingPid; http://127.0.0.1:$Port"
        exit 0
    }
}
$portProbe = New-Object System.Net.Sockets.TcpClient
try {
    $portProbe.Connect('127.0.0.1', $Port)
    throw "Port $Port is in use; choose another -Port."
} catch [System.Net.Sockets.SocketException] {
    # Connection refused means the loopback port is available.
} finally {
    $portProbe.Dispose()
}
$arguments = @('-m', ('"' + $modelPath + '"'), '--alias', 'qwen2.5-3b-instruct',
    '--host', '127.0.0.1', '--port', "$Port", '-c', "$ContextSize", '-np', '1',
    '-ngl', 'all', '--jinja', '--chat-template-file', ('"' + $templatePath + '"'),
    '-b', '512', '-ub', '128', '--threads', '8', '--cache-ram', '256', '--no-webui')
if ($LoraPath) { $arguments += @('--lora', ('"' + $LoraPath + '"')) }
$process = Start-Process -FilePath $ServerPath -ArgumentList $arguments -WorkingDirectory $projectRoot -WindowStyle Hidden -PassThru `
    -RedirectStandardOutput (Join-Path $runtimeDir 'server.stdout.log') `
    -RedirectStandardError (Join-Path $runtimeDir 'server.stderr.log')
$process.Id | Set-Content -LiteralPath $pidFile
[pscustomobject]@{pid=$process.Id;engine=$ServerPath;port=$Port;context=$ContextSize;model=$modelPath;adapter=$LoraPath} |
    ConvertTo-Json | Set-Content -Encoding UTF8 -LiteralPath (Join-Path $runtimeDir 'server_config.json')
Write-Output "Started Qwen PID $($process.Id); http://127.0.0.1:$Port; logs: $runtimeDir"
