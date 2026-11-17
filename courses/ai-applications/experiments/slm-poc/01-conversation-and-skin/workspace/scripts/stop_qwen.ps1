$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$pidFile = Join-Path $projectRoot 'output/runtime/qwen-server.pid'
$modelPath = Join-Path $projectRoot 'models/qwen2.5-3b-instruct/qwen2.5-3b-instruct-q4_k_m.gguf'
if (Test-Path -LiteralPath $pidFile) {
    $serverPid = [int](Get-Content -LiteralPath $pidFile -Raw)
    $process = Get-CimInstance Win32_Process -Filter "ProcessId = $serverPid"
    if ($process -and $process.Name -eq 'llama-server.exe' -and $process.CommandLine.Contains($modelPath)) {
        Stop-Process -Id $serverPid
        Write-Output "Stopped project Qwen server PID $serverPid"
    } elseif ($process) {
        throw 'PID now belongs to another process; refusing to stop it.'
    }
    Remove-Item -LiteralPath $pidFile
}
