# Usage:
#   WS_URL=ws://127.0.0.1:8001/api/v1/ws python3 ws_client_python.py
#   WS_URL=wss://<host>/api/v1/ws python3 ws_client_python.py

import json
import os
import time

try:
    import websocket
except Exception as exc:
    raise SystemExit(f"websocket-client not installed: {exc}")

ws_url = os.getenv("WS_URL", "ws://127.0.0.1:8001/api/v1/ws")
timeout_s = 5

print(f"CONNECTING {ws_url}")
ws = websocket.WebSocket()
ws.settimeout(timeout_s)
ws.connect(ws_url)
print("CONNECTED")

start = time.time()
try:
    msg = ws.recv()
    try:
        print(json.dumps(json.loads(msg)))
    except Exception:
        print(msg)
    ws.close()
    raise SystemExit(0)
except Exception:
    elapsed = time.time() - start
    if elapsed >= timeout_s:
        print("NO_MESSAGE_WITHIN_5S")
        ws.close()
        raise SystemExit(2)
    raise
