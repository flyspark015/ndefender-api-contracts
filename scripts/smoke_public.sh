#!/usr/bin/env bash
set -euo pipefail

BASE="${BASE:-https://n.flyspark.in/api/v1}"

curl -fsS "$BASE/health"
curl -fsS "$BASE/status"
curl -fsS "$BASE/contacts" || true

curl -fsS "$BASE/gps" || true
curl -fsS "$BASE/network/wifi/state" || true
curl -fsS "$BASE/network/bluetooth/state" || true

if command -v websocat >/dev/null 2>&1; then
  echo "WS test (10s)"
  timeout 10s websocat -q "${WS:-wss://n.flyspark.in/api/v1/ws}" || true
else
  echo "websocat not found; use tools/validate_contract.py for WS checks" >&2
fi
