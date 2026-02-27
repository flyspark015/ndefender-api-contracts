#!/usr/bin/env bash
set -euo pipefail

WS_URL="${WS_URL:-ws://127.0.0.1:8001/api/v1/ws}"
export WS_URL

python3 - <<'PY' || {
  if command -v websocat >/dev/null 2>&1; then
    echo "Fallback to websocat" >&2
    timeout 5s websocat -q "$WS_URL" >/dev/null 2>&1 && exit 0
  fi
  exit 1
}
import json
import os
import sys
try:
    import websocket
except Exception as exc:
    print(f"websocket module unavailable: {exc}")
    raise SystemExit(1)

ws = websocket.WebSocket()
ws.settimeout(5)
ws.connect(os.environ["WS_URL"])
msg = ws.recv()
print(msg)
try:
    json.loads(msg)
    raise SystemExit(0)
except Exception:
    raise SystemExit(1)
PY
