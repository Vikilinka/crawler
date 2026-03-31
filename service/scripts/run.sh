#!/usr/bin/env bash
set -euo pipefail

DEBUG="${DEBUG:-false}"
DEBUG="${DEBUG,,}"
run() {
  if [[ "$DEBUG" == "true" ]]; then
    echo "+ $*"
  fi
  "$@"
}

if [[ $# -lt 1 ]]; then
  echo "Error: MODE is required."
  echo "Usage: $0 {dev|prod|debug|elastic}"
  exit 1
fi

MODE="${1,,}"

case "$MODE" in
  dev|prod|debug|elastic)
    ;;
  *)
    echo "Error: Invalid mode '$MODE'"
    echo "Usage: $0 {dev|prod|debug|elastic}"
    exit 1
    ;;
esac

DOCKER_BIN="$(command -v docker || true)"
if [[ -z "$DOCKER_BIN" ]]; then
  echo "Docker not found"
  exit 1
fi

SCRIPT_DIR="$(realpath "$(dirname "${BASH_SOURCE[0]}")")"
PROJECT_ROOT="$(realpath "$SCRIPT_DIR/../..")"
COMPOSE_FILE="$PROJECT_ROOT/service/docker/dsangel/docker-compose.$MODE.yml"
COMPOSE_UP_ARGS=(-d --build)
if [[ "$MODE" == "prod" ]]; then
  COMPOSE_UP_ARGS+=(--force-recreate --pull always)
fi

run "$DOCKER_BIN" compose -f "$COMPOSE_FILE" up "${COMPOSE_UP_ARGS[@]}"
