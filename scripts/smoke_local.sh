#!/usr/bin/env bash
set -euo pipefail

BASE="${BASE:-http://127.0.0.1:8001/api/v1}"
SC="${SC:-http://127.0.0.1:8002/api/v1}"
RF="${RF:-http://127.0.0.1:8890/api/v1}"

if command -v ss >/dev/null 2>&1; then
  ss -lntp | egrep '(:8001|:8002|:8890|:8000)\b' || true
  if ss -lntp | grep -q ':8000'; then
    echo "FAIL: legacy :8000 is listening" >&2
    exit 1
  fi
else
  echo "ss not available; skipping port checks" >&2
fi

status_json=$(curl -fsS "$BASE/status")
python3 - <<'PY' <<EOF_JSON
import json,sys
j=json.load(sys.stdin)
assert "timestamp_ms" in j, "timestamp_ms missing"
print("status ok: timestamp_ms present")
PY
EOF_JSON

curl -fsS "$BASE/health" >/dev/null
curl -fsS "$BASE/contacts" >/dev/null || true
curl -fsS "$BASE/gps" >/dev/null
curl -fsS "$BASE/network/wifi/state" >/dev/null
curl -fsS "$BASE/network/bluetooth/state" >/dev/null
curl -fsS "$BASE/antsdr" >/dev/null
curl -fsS "$BASE/remote_id/status" >/dev/null
curl -fsS "$BASE/esp32" >/dev/null

resp=$(curl -sS -i -X POST "$BASE/system/reboot" \
  -H 'Content-Type: application/json' \
  -d '{"payload":{},"confirm":false}' | sed -n '1,25p')

echo "$resp"
if echo "$resp" | grep -q "429"; then
  echo "FAIL: rate limit applied before confirm_required" >&2
  exit 1
fi
if ! echo "$resp" | grep -q "confirm_required"; then
  echo "FAIL: confirm_required not returned" >&2
  exit 1
fi

if command -v websocat >/dev/null 2>&1; then
  timeout 10s websocat -q "${WS:-ws://127.0.0.1:8001/api/v1/ws}" || true
else
  echo "websocat not found; use tools/validate_contract.py for WS checks" >&2
fi

curl -fsS "$SC/health" >/dev/null
curl -fsS "$RF/health" >/dev/null
