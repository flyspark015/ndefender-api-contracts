from __future__ import annotations

import asyncio
import time
from fastapi import FastAPI, WebSocket

from shared.ndefender_common.cors import install_cors
from shared.ndefender_common.ws import send_hello, send_system_update, heartbeat_loop

app = FastAPI()
install_cors(app)


def _now_ms() -> int:
    return int(time.time() * 1000)


@app.get("/api/v1/health")
def health() -> dict:
    return {"status": "ok", "timestamp_ms": _now_ms()}


@app.get("/api/v1/status")
def status() -> dict:
    return {
        "timestamp_ms": _now_ms(),
        "system": {"status": "degraded", "cpu_temp_c": 36.9, "cpu_usage_percent": 15.8, "ram_used_mb": 1931, "ram_total_mb": 16215, "disk_used_gb": 70, "disk_total_gb": 117, "uptime_s": 4671},
        "power": {"status": "ok", "pack_voltage_v": 16.62, "current_a": -0.01, "soc_percent": 98, "state": "IDLE"},
        "rf": {"status": "offline", "last_error": "antsdr_unreachable", "scan_active": False, "last_event_type": "RF_SCAN_OFFLINE", "last_timestamp_ms": _now_ms(), "last_event": {"reason": "antsdr_unreachable"}},
        "remote_id": {"state": "DEGRADED", "mode": "live", "capture_active": True, "last_error": "no_odid_frames", "last_event_type": "REMOTEID_STALE", "last_timestamp_ms": _now_ms(), "last_event": {"reason": "no_odid_frames"}},
        "vrx": {"selected": 1, "scan_state": "idle", "vrx": [{"id": 1, "freq_hz": 5740000000, "rssi_raw": 632}]},
        "fpv": {"selected": 1, "scan_state": "idle", "freq_hz": 5740000000, "rssi_raw": 632},
        "video": {"selected": 1, "status": "ok"},
        "services": [{"name": "ndefender-backend", "active_state": "active", "sub_state": "running", "restart_count": 0}],
        "network": {"status": "ok", "connected": True, "ip_v4": "192.168.1.35", "ssid": "example"},
        "audio": {"status": "ok", "muted": False, "volume_percent": 100},
        "contacts": [],
        "replay": {"active": False, "source": "none"},
        "overall_ok": False,
    }


@app.websocket("/api/v1/ws")
async def ws_endpoint(ws: WebSocket) -> None:
    await ws.accept()
    # CONTRACT GAP: HELLO is not yet formalized.
    await send_hello(ws)
    await send_system_update(ws, status())
    # CONTRACT GAP: HEARTBEAT emitted for liveness (not yet formalized).
    await heartbeat_loop(ws, interval_s=3.0)
