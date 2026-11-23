param(
    [string]$UvPath = '',
    [string]$Python311 = ''
)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $projectRoot
if (-not $UvPath) { $UvPath = Join-Path $env:LOCALAPPDATA 'Programs/Jan/uv.exe' }
if (-not $Python311) { $Python311 = Join-Path $env:USERPROFILE '.local/bin/python3.11.exe' }
if (-not (Test-Path -LiteralPath $UvPath)) { throw 'Specify -UvPath for a uv executable.' }
if (-not (Test-Path -LiteralPath $Python311)) { throw 'Specify -Python311 for an installed Python 3.11 executable.' }
$trainingPython = Join-Path $projectRoot '.venv-train/Scripts/python.exe'
if (-not (Test-Path -LiteralPath $trainingPython)) {
    & $UvPath venv .venv-train --python $Python311
    if ($LASTEXITCODE -ne 0) { throw 'Virtual environment creation failed.' }
}
python scripts/parallel_download.py
if ($LASTEXITCODE -ne 0) { throw 'CUDA wheel download failed.' }
$wheelMetadata = Get-Content -LiteralPath 'tmp/training_wheels/torch_wheel.json' -Raw | ConvertFrom-Json
$wheelPath = Join-Path $projectRoot ('tmp/training_wheels/' + $wheelMetadata.filename)
& $UvPath pip install --python $trainingPython $wheelPath
if ($LASTEXITCODE -ne 0) { throw 'CUDA PyTorch installation failed.' }
& $UvPath pip install --python $trainingPython -r requirements-train.txt
if ($LASTEXITCODE -ne 0) { throw 'Training dependency installation failed.' }
& $trainingPython scripts/check_training_env.py
if ($LASTEXITCODE -ne 0) { throw 'CUDA/NF4 environment verification failed.' }
