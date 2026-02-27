#!/usr/bin/env bash
set -euo pipefail

pass=true

BASE="${BASE:-http://127.0.0.1:8001/api/v1}"
SC="${SC:-http://127.0.0.1:8002/api/v1}"
RF="${RF:-http://127.0.0.1:8890/api/v1}"

if command -v ss >/dev/null 2>&1; then
  ss -lntp | egrep '(:8001|:8002|:8890|:8000)\b' || true
  if ss -lntp | grep -q ':8000'; then
    echo "FAIL: legacy :8000 is listening" >&2
    pass=false
  fi
else
  echo "ss not available; skipping port checks" >&2
fi

status_json=$(curl -fsS "$BASE/status")
python3 - <<'PY' <<<"$status_json" || pass=false
import json,sys
j=json.load(sys.stdin)
assert "timestamp_ms" in j, "timestamp_ms missing"
assert isinstance(j["timestamp_ms"], int), "timestamp_ms must be int"
print("status ok: timestamp_ms present")
PY

curl -fsS "$BASE/health" >/dev/null || pass=false
curl -fsS "$BASE/contacts" >/dev/null || true
curl -fsS "$BASE/gps" >/dev/null || pass=false
curl -fsS "$BASE/network/wifi/state" >/dev/null || pass=false
curl -fsS "$BASE/network/bluetooth/state" >/dev/null || pass=false
curl -fsS "$BASE/antsdr" >/dev/null || pass=false
curl -fsS "$BASE/remote_id/status" >/dev/null || pass=false
curl -fsS "$BASE/esp32" >/dev/null || pass=false

resp=$(curl -sS -i -X POST "$BASE/system/reboot" \
  -H 'Content-Type: application/json' \
  -d '{"payload":{},"confirm":false}' | sed -n '1,25p')

echo "$resp"
if echo "$resp" | grep -q "429"; then
  echo "FAIL: rate limit applied before confirm_required" >&2
  pass=false
fi
if ! echo "$resp" | grep -q "confirm_required"; then
  echo "FAIL: confirm_required not returned" >&2
  pass=false
fi

if command -v websocat >/dev/null 2>&1; then
  timeout 10s websocat -q "${WS:-ws://127.0.0.1:8001/api/v1/ws}" || true
else
  echo "websocat not found; use tools/validate_contract.py for WS checks" >&2
fi

curl -fsS "$SC/health" >/dev/null || pass=false
curl -fsS "$RF/health" >/dev/null || pass=false

if $pass; then
  echo "SMOKE_LOCAL: PASS"
  exit 0
else
  echo "SMOKE_LOCAL: FAIL"
  exit 1
fi
