$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$pidFile = Join-Path $projectRoot 'output/runtime-qwen3/qwen3-server.pid'
$modelPath = Join-Path $projectRoot 'models/qwen3-4b-instruct-2507/Qwen3-4B-Instruct-2507-Q4_K_M.gguf'
if (Test-Path -LiteralPath $pidFile) {
    $serverPid = [int](Get-Content -LiteralPath $pidFile -Raw)
    $process = Get-CimInstance Win32_Process -Filter "ProcessId = $serverPid"
    if ($process -and $process.Name -eq 'llama-server.exe' -and $process.CommandLine.Contains($modelPath)) {
        Stop-Process -Id $serverPid
        Write-Output "Stopped project Qwen3 server PID $serverPid"
    } elseif ($process) { throw 'PID belongs to another process; refusing to stop it.' }
    Remove-Item -LiteralPath $pidFile
}
