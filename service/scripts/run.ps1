$ErrorActionPreference = "Stop"

$DEBUG = $env:DEBUG
if (-not $DEBUG) { $DEBUG = "false" }
$DEBUG = $DEBUG.ToLower()
function Run($cmd, $cmdArgs) {
    if ($DEBUG -eq "true") {
        Write-Host "+ $cmd $($cmdArgs -join ' ')"
    }
    & $cmd @cmdArgs
}

if ($args.Count -lt 1) {
    Write-Host "Error: MODE is required."
    Write-Host "Usage: ./run.ps1 {dev|prod|debug|elastic}"
    exit 1
}

$MODE = $args[0].ToLower()

if ($MODE -notin @("dev","prod","debug","elastic")) {
    Write-Host "Error: Invalid mode '$MODE'"
    Write-Host "Usage: ./run.ps1 {dev|prod|debug|elastic}"
    exit 1
}

$DOCKER_BIN = Get-Command docker -ErrorAction SilentlyContinue
if (-not $DOCKER_BIN) {
    Write-Host "Docker not found"
    exit 1
}

$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$SCRIPT_DIR = Resolve-Path $SCRIPT_DIR
$PROJECT_ROOT = Resolve-Path "$SCRIPT_DIR\..\.."
$COMPOSE_FILE = "$PROJECT_ROOT\service\docker\dsangel\docker-compose.$MODE.yml"
$COMPOSE_UP_ARGS = @("-d", "--build")
if ($MODE -eq "prod") {
    $COMPOSE_UP_ARGS += @("--force-recreate", "--pull", "always")
}

$composeArgs = @("compose",  "-f", $COMPOSE_FILE, "up") + $COMPOSE_UP_ARGS

Run "docker" $composeArgs
