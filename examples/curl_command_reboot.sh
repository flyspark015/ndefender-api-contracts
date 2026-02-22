#!/usr/bin/env bash
set -euo pipefail

BASE_URL=${BASE_URL:-"http://127.0.0.1:8001/api/v1"}

curl -sS -X POST "$BASE_URL/system/reboot" \
  -H "Content-Type: application/json" \
  -d '{"confirm":true}' | jq .
