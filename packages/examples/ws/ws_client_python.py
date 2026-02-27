# Usage:
#   WS_URL=ws://127.0.0.1:8001/api/v1/ws python3 ws_client_python.py
#   WS_URL=wss://<host>/api/v1/ws python3 ws_client_python.py

import json
import os

try:
    import websocket
except Exception as exc:
    raise SystemExit(f"websocket-client not installed: {exc}")

ws_url = os.getenv("WS_URL", "ws://127.0.0.1:8001/api/v1/ws")
ws = websocket.WebSocket()
ws.connect(ws_url)
print("connected")
while True:
    msg = ws.recv()
    try:
        print(json.dumps(json.loads(msg)))
    except Exception:
        print(msg)
