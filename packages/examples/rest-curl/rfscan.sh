#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   BASE_URL=http://127.0.0.1:8890/api/v1 ./rfscan.sh
#   BASE_URL=https://<host>/api/v1 ./rfscan.sh

BASE_URL="${BASE_URL:-http://127.0.0.1:8890/api/v1}"

curl -sS "$BASE_URL/health"
curl -sS "$BASE_URL/version"
curl -sS "$BASE_URL/stats"
curl -sS "$BASE_URL/device"
curl -sS "$BASE_URL/sweep/state"
curl -sS "$BASE_URL/gain"
curl -sS "$BASE_URL/config"
curl -sS "$BASE_URL/events/last?limit=1" || true
