#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   BASE_URL=http://127.0.0.1:8001/api/v1 ./antsdr.sh
#   BASE_URL=https://<host>/api/v1 ./antsdr.sh

BASE_URL="${BASE_URL:-http://127.0.0.1:8001/api/v1}"

curl -sS "$BASE_URL/antsdr"
curl -sS "$BASE_URL/antsdr/sweep/state"
curl -sS "$BASE_URL/antsdr/gain"
curl -sS "$BASE_URL/antsdr/stats"
