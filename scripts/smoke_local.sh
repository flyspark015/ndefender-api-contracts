#!/usr/bin/env bash
set -euo pipefail

BASE="${BASE:-http://127.0.0.1:8001/api/v1}"

curl -fsS "$BASE/health"
curl -fsS "$BASE/status"
curl -fsS "$BASE/contacts" || true

curl -fsS "$BASE/gps"
curl -fsS "$BASE/network/wifi/state"
curl -fsS "$BASE/network/bluetooth/state"

curl -fsS "$BASE/antsdr"
curl -fsS "$BASE/remote_id/status"
curl -fsS "$BASE/esp32"

if command -v websocat >/dev/null 2>&1; then
  echo "WS test (10s)"
  timeout 10s websocat -q "${WS:-ws://127.0.0.1:8001/api/v1/ws}" || true
else
  echo "websocat not found; use tools/validate_contract.py for WS checks" >&2
fi
