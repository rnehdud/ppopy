param([string]$ServerPath = '', [int]$Port = 18081, [int]$ContextSize = 8192, [string]$LoraPath = '')
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$modelPath = Join-Path $projectRoot 'models/qwen3-4b-instruct-2507/Qwen3-4B-Instruct-2507-Q4_K_M.gguf'
$templatePath = Join-Path $projectRoot 'models/qwen3-4b-instruct-2507/chat_template.jinja'
$runtimeDir = Join-Path $projectRoot 'output/runtime-qwen3'
$pidFile = Join-Path $runtimeDir 'qwen3-server.pid'
if ($LoraPath) {
    $LoraPath = [System.IO.Path]::GetFullPath((Join-Path $projectRoot $LoraPath))
    if (-not (Test-Path -LiteralPath $LoraPath)) { throw 'LoRA GGUF file not found.' }
}
if (-not (Test-Path -LiteralPath $modelPath) -or -not (Test-Path -LiteralPath $templatePath)) {
    throw 'Run python scripts/setup_qwen3.py first.'
}
if (-not $ServerPath) {
    $engineRoot = Join-Path $env:APPDATA 'Jan/data/llamacpp/backends'
    $ServerPath = Get-ChildItem -LiteralPath $engineRoot -Recurse -Filter 'llama-server.exe' -ErrorAction SilentlyContinue |
        Where-Object { $_.FullName -match 'win-cuda' } |
        Sort-Object FullName -Descending | Select-Object -First 1 -ExpandProperty FullName
}
if (-not $ServerPath -or -not (Test-Path -LiteralPath $ServerPath)) { throw 'CUDA llama-server not found.' }
New-Item -ItemType Directory -Force -Path $runtimeDir | Out-Null
if (Test-Path -LiteralPath $pidFile) {
    $existingPid = [int](Get-Content -LiteralPath $pidFile -Raw)
    $existing = Get-CimInstance Win32_Process -Filter "ProcessId = $existingPid"
    if ($existing) { throw 'A Qwen3 PID file is already in use; stop it first.' }
}
$probe = New-Object System.Net.Sockets.TcpClient
try { $probe.Connect('127.0.0.1', $Port); throw "Port $Port is in use." }
catch [System.Net.Sockets.SocketException] {} finally { $probe.Dispose() }
$arguments = @('-m', ('"' + $modelPath + '"'), '--alias', 'qwen3-4b-instruct-2507',
    '--host', '127.0.0.1', '--port', "$Port", '-c', "$ContextSize", '-np', '1',
    '-ngl', 'all', '--jinja', '--chat-template-file', ('"' + $templatePath + '"'),
    '-b', '512', '-ub', '128', '--threads', '8', '--cache-ram', '256', '--no-webui')
if ($LoraPath) { $arguments += @('--lora', ('"' + $LoraPath + '"')) }
$process = Start-Process -FilePath $ServerPath -ArgumentList $arguments -WorkingDirectory $projectRoot -WindowStyle Hidden -PassThru `
    -RedirectStandardOutput (Join-Path $runtimeDir 'server.stdout.log') `
    -RedirectStandardError (Join-Path $runtimeDir 'server.stderr.log')
$process.Id | Set-Content -LiteralPath $pidFile
[pscustomobject]@{pid=$process.Id;engine=$ServerPath;port=$Port;context=$ContextSize;model=$modelPath;adapter=$LoraPath;template=$templatePath} |
    ConvertTo-Json | Set-Content -Encoding UTF8 -LiteralPath (Join-Path $runtimeDir 'server_config.json')
Write-Output "Started Qwen3 PID $($process.Id); http://127.0.0.1:$Port"
