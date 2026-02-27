#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   BASE_URL=http://127.0.0.1:8001/api/v1 ./gps.sh
#   BASE_URL=https://<host>/api/v1 ./gps.sh

BASE_URL="${BASE_URL:-http://127.0.0.1:8001/api/v1}"

curl -sS "$BASE_URL/gps"
