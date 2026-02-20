#!/usr/bin/env bash
set -euo pipefail

BASE_URL=${BASE_URL:-"http://127.0.0.1:8001/api/v1"}
API_KEY=${API_KEY:-""}
ROLE=${ROLE:-"admin"}

if [[ -z "$API_KEY" ]]; then
  echo "ERROR: API_KEY is required" >&2
  exit 1
fi

curl -sS -X POST "$BASE_URL/system/reboot" \
  -H "X-API-Key: $API_KEY" \
  -H "X-Role: $ROLE" \
  -H "Content-Type: application/json" \
  -d '{"confirm":true}' | jq .
