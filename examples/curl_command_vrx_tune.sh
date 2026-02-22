#!/usr/bin/env bash
set -euo pipefail

BASE_URL=${BASE_URL:-"http://127.0.0.1:8001/api/v1"}
VRX_ID=${VRX_ID:-1}
FREQ_HZ=${FREQ_HZ:-5740000000}

curl -sS -X POST "$BASE_URL/vrx/tune" \
  -H "Content-Type: application/json" \
  -d "{\"payload\":{\"vrx_id\":$VRX_ID,\"freq_hz\":$FREQ_HZ}}" | jq .
