#!/usr/bin/env bash
set -euo pipefail

BASE_URL=${BASE_URL:-"http://127.0.0.1:8001/api/v1"}
API_KEY=${API_KEY:-""}
ROLE=${ROLE:-"operator"}
VRX_ID=${VRX_ID:-1}
FREQ_HZ=${FREQ_HZ:-5740000000}

if [[ -z "$API_KEY" ]]; then
  echo "ERROR: API_KEY is required" >&2
  exit 1
fi

curl -sS -X POST "$BASE_URL/vrx/tune" \
  -H "X-API-Key: $API_KEY" \
  -H "X-Role: $ROLE" \
  -H "Content-Type: application/json" \
  -d "{\"payload\":{\"vrx_id\":$VRX_ID,\"freq_hz\":$FREQ_HZ}}" | jq .
