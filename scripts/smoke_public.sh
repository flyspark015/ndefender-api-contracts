#!/usr/bin/env bash
set -euo pipefail

BASE="${BASE:-https://n.flyspark.in/api/v1}"

if [[ "$BASE" == http://127.0.0.1:* || "$BASE" == http://localhost:* ]]; then
  if command -v ss >/dev/null 2>&1; then
    ss -lntp | egrep '(:8001|:8002|:8890|:8000)\b' || true
    if ss -lntp | grep -q ':8000'; then
      echo "FAIL: legacy :8000 is listening" >&2
      exit 1
    fi
  fi
else
  echo "Skipping local port checks (BASE is remote)"
fi

curl -fsS "$BASE/health" >/dev/null
curl -fsS "$BASE/status" >/dev/null
curl -fsS "$BASE/contacts" >/dev/null || true

resp=$(curl -sS -i -X POST "$BASE/system/reboot" \
  -H 'Content-Type: application/json' \
  -d '{"payload":{},"confirm":false}' | sed -n '1,25p')

echo "$resp"
if echo "$resp" | grep -q "429"; then
  echo "FAIL: rate limit applied before confirm_required" >&2
  exit 1
fi
if ! echo "$resp" | grep -Eq "confirm_required|unsafe_disabled|local_only"; then
  echo "FAIL: expected confirm_required or unsafe_disabled/local_only" >&2
  exit 1
fi

if command -v websocat >/dev/null 2>&1; then
  timeout 10s websocat -q "${WS:-wss://n.flyspark.in/api/v1/ws}" || true
else
  echo "websocat not found; use tools/validate_contract.py for WS checks" >&2
fi
