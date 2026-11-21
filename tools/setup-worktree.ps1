# Windows Orca setup hook. Run explicitly; never prints environment file contents.
[CmdletBinding()]
param(
    [string]$WorktreePath = $env:ORCA_WORKTREE_PATH,
    [string]$SourceRootPath = $env:ORCA_ROOT_PATH,
    [string]$PythonVersion = '3.12',
    [switch]$PlanOnly
)

$ErrorActionPreference = 'Stop'
if (-not $WorktreePath) {
    $WorktreePath = Split-Path -Parent $PSScriptRoot
}
$taskRoot = (Resolve-Path -LiteralPath $WorktreePath).Path
$projectRelative = 'courses/ai-applications/experiments/cos-agent'
$projectPath = Join-Path $taskRoot $projectRelative
foreach ($requiredFile in @('pyproject.toml', 'uv.lock', '.env.example')) {
    if (-not (Test-Path -LiteralPath (Join-Path $projectPath $requiredFile) -PathType Leaf)) {
        throw "Missing project file: $requiredFile in $projectPath"
    }
}

$targetEnv = Join-Path $projectPath '.env'
$envSource = Join-Path $projectPath '.env.example'
if ($SourceRootPath) {
    $resolvedSource = (Resolve-Path -LiteralPath $SourceRootPath).Path
    $sourceEnv = Join-Path (Join-Path $resolvedSource $projectRelative) '.env'
    if (Test-Path -LiteralPath $sourceEnv -PathType Leaf) {
        $envSource = $sourceEnv
    }
}

if ($PlanOnly) {
    Write-Output "Worktree: $taskRoot"
    Write-Output "Project: $projectPath"
    Write-Output 'Environment: preserve existing .env; otherwise copy source .env or .env.example.'
    Write-Output "Dependencies: uv sync --locked --group dev --python $PythonVersion"
    Write-Output 'Creates a worktree-local .venv; may download Python and packages.'
    return
}

Get-Command uv -ErrorAction Stop | Out-Null
if (-not (Test-Path -LiteralPath $targetEnv)) {
    Copy-Item -LiteralPath $envSource -Destination $targetEnv
    Write-Output 'Created local project .env (contents not displayed).'
} else {
    Write-Output 'Preserved existing project .env.'
}

New-Item -ItemType Directory -Path (Join-Path $taskRoot 'outputs') -Force | Out-Null
Push-Location -LiteralPath $projectPath
try {
    & uv sync --locked --group dev --python $PythonVersion
    if ($LASTEXITCODE -ne 0) {
        throw "uv sync failed with exit code $LASTEXITCODE"
    }
} finally {
    Pop-Location
}
Write-Output 'Worktree setup complete. Use uv run from the cos-agent project directory.'
Write-Output 'To load its .env explicitly: uv run --env-file .env <command>'
