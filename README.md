# N-Defender API Contracts (Single Source of Truth)

This repository is the canonical specification for all N-Defender REST + WebSocket APIs, covering backend, system controls, RF scan, RemoteID, firmware integration, UI/UX integration, and AI tooling.

Canonical contract:
- `docs/ALL_IN_ONE_API.md`

Deep‑dive API guide:
- `docs/api/README.md`

## Architecture Overview
```
                     Public Internet
                            |
                            |  https://n.flyspark.in/api/v1
                            v
                    +----------------------+
 UI / AI / Figma -->| Backend Aggregator   |
                    | FastAPI :8001        |
                    +----------------------+
                       |         |        |
                       |         |        |
         +-------------+   +-----+-----+  +--------------------+
         | System Ctrl |   | RFScan   |  | RemoteID Engine    |
         | FastAPI:8002|   | :8890    |  | (local /api/v1)    |
         +-------------+   +----------+  +--------------------+
                       |
                       +--------------------+
                       | ESP32 Panel (serial)
                       +--------------------+

Legacy Flask on :8000 is removed/disabled (security hardening).
```

## Port Map and Ownership
- Aggregator (public API, primary): `http://127.0.0.1:8001/api/v1`
- System Controller (system controls): `http://127.0.0.1:8002/api/v1`
- RFScan (AntSDR scan): `http://127.0.0.1:8890/api/v1`
- RemoteID Engine (service-local): `http://127.0.0.1:<port>/api/v1`

## Naming & Units
- All timestamps are epoch milliseconds: `timestamp_ms`, `last_update_ms`.
- GPS uses `latitude`/`longitude`.
- RemoteID contacts use `lat`/`lon` per Contact schema.
- Frequencies use `freq_hz` (Hz).
- Signal strength uses `rssi_dbm` (dBm).

### Endpoint Ownership (Prefix Map)
| Service | Canonical Prefix |
|---------|------------------|
| Aggregator | `/api/v1/*` (default) |
| System Controller | `/api/v1/system-controller/*` |
| RFScan (AntSDR Scan) | `/api/v1/antsdr-scan/*` |
| RemoteID Engine | `/api/v1/remoteid-engine/*` |
| Observability | `/api/v1/observability/*` |

## RX vs TX Flows
**RX (status + events)**
1) `GET /api/v1/status` → full snapshot.
2) `WS /api/v1/ws` → `SYSTEM_UPDATE`, `CONTACT_*`, `TELEMETRY_UPDATE`, `REPLAY_STATE`, `HEARTBEAT`.
3) On WS disconnect: re-fetch `/api/v1/status`, then reconnect.

**TX (commands)**
1) Send REST command with `{"payload":{...},"confirm":false}`.
2) REST returns `CommandResult` with `command_id`.
3) WS emits `COMMAND_ACK` with matching correlation key.

## Confirm‑Gating Lifecycle (Dangerous Commands)
Dangerous commands require two steps:
1) First call with `confirm=false` **must return** HTTP 400: `{"detail":"confirm_required"}`.
2) Second call with `confirm=true` executes the command.

UI guidance: show a modal requiring explicit confirmation and send `confirm=true` only after user approval.
The 400 must occur **before** any state change is triggered.

Dangerous endpoints (confirm required):
- `POST /api/v1/system/reboot`
- `POST /api/v1/system/shutdown`
- `POST /api/v1/system-controller/system/reboot`
- `POST /api/v1/system-controller/system/shutdown`
- `POST /api/v1/system-controller/services/{name}/restart`
- `POST /api/v1/antsdr/device/reset`
- `POST /api/v1/antsdr-scan/device/reset`
- `POST /api/v1/antsdr-scan/device/calibrate`

## Error Taxonomy (FastAPI)
| HTTP | Reason | Example |
|------|--------|---------|
| 400 | confirm_required | `{"detail":"confirm_required"}` |
| 422 | validation_error | `{"detail":"validation_error"}` |
| 503 | service_unavailable | `{"detail":"service_unavailable"}` |
| 504 | upstream_timeout | `{"detail":"upstream_timeout"}` |
| 409 | busy/conflict | `{"detail":"invalid_state"}` |

## Routing Canonicalization
- OpenAPI paths are relative to server base `/api/v1` in `docs/OPENAPI.yaml`.
- README lists canonical full paths `/api/v1/...`.
- CI enforces canonical equivalence.
- Legacy aliases (`/status`, `/ws`) are backward‑compat only if present.

## API Index (Strict, CI‑checked)
<!-- API_INDEX_START -->
- GET /api/v1/antsdr
- GET /api/v1/antsdr-scan/config
- GET /api/v1/antsdr-scan/device
- GET /api/v1/antsdr-scan/events/last
- GET /api/v1/antsdr-scan/gain
- GET /api/v1/antsdr-scan/health
- GET /api/v1/antsdr-scan/stats
- GET /api/v1/antsdr-scan/sweep/state
- GET /api/v1/antsdr-scan/version
- GET /api/v1/antsdr/gain
- GET /api/v1/antsdr/stats
- GET /api/v1/antsdr/sweep/state
- GET /api/v1/audio
- GET /api/v1/contacts
- GET /api/v1/esp32
- GET /api/v1/esp32/config
- GET /api/v1/gps
- GET /api/v1/health
- GET /api/v1/network
- GET /api/v1/network/bluetooth/devices
- GET /api/v1/network/bluetooth/state
- GET /api/v1/network/wifi/scan
- GET /api/v1/network/wifi/state
- GET /api/v1/observability/config
- GET /api/v1/observability/health
- GET /api/v1/observability/health/detail
- GET /api/v1/observability/status
- GET /api/v1/observability/version
- GET /api/v1/power
- GET /api/v1/remote_id
- GET /api/v1/remote_id/contacts
- GET /api/v1/remote_id/stats
- GET /api/v1/remoteid-engine/contacts
- GET /api/v1/remoteid-engine/health
- GET /api/v1/remoteid-engine/replay/state
- GET /api/v1/remoteid-engine/stats
- GET /api/v1/remoteid-engine/status
- GET /api/v1/rf
- GET /api/v1/services
- GET /api/v1/status
- GET /api/v1/system
- GET /api/v1/system-controller/audio
- GET /api/v1/system-controller/gps
- GET /api/v1/system-controller/health
- GET /api/v1/system-controller/network
- GET /api/v1/system-controller/network/bluetooth/devices
- GET /api/v1/system-controller/network/bluetooth/state
- GET /api/v1/system-controller/network/wifi/scan
- GET /api/v1/system-controller/network/wifi/state
- GET /api/v1/system-controller/services
- GET /api/v1/system-controller/status
- GET /api/v1/system-controller/system
- GET /api/v1/system-controller/ups
- GET /api/v1/system-controller/ws
- GET /api/v1/video
- GET /api/v1/ws
- POST /api/v1/antsdr-scan/config/reload
- POST /api/v1/antsdr-scan/device/calibrate
- POST /api/v1/antsdr-scan/device/reset
- POST /api/v1/antsdr-scan/gain/set
- POST /api/v1/antsdr-scan/sweep/start
- POST /api/v1/antsdr-scan/sweep/stop
- POST /api/v1/antsdr/device/reset
- POST /api/v1/antsdr/gain/set
- POST /api/v1/antsdr/sweep/start
- POST /api/v1/antsdr/sweep/stop
- POST /api/v1/audio/mute
- POST /api/v1/audio/volume
- POST /api/v1/esp32/buttons/simulate
- POST /api/v1/esp32/buzzer
- POST /api/v1/esp32/config
- POST /api/v1/esp32/leds
- POST /api/v1/gps/restart
- POST /api/v1/network/bluetooth/disable
- POST /api/v1/network/bluetooth/enable
- POST /api/v1/network/bluetooth/pair
- POST /api/v1/network/bluetooth/scan/start
- POST /api/v1/network/bluetooth/scan/stop
- POST /api/v1/network/bluetooth/unpair
- POST /api/v1/network/wifi/connect
- POST /api/v1/network/wifi/disable
- POST /api/v1/network/wifi/disconnect
- POST /api/v1/network/wifi/enable
- POST /api/v1/observability/diag/bundle
- POST /api/v1/remote_id/monitor/start
- POST /api/v1/remote_id/monitor/stop
- POST /api/v1/remoteid-engine/monitor/start
- POST /api/v1/remoteid-engine/monitor/stop
- POST /api/v1/remoteid-engine/replay/start
- POST /api/v1/remoteid-engine/replay/stop
- POST /api/v1/scan/start
- POST /api/v1/scan/stop
- POST /api/v1/system-controller/audio/mute
- POST /api/v1/system-controller/audio/volume
- POST /api/v1/system-controller/gps/restart
- POST /api/v1/system-controller/network/bluetooth/disable
- POST /api/v1/system-controller/network/bluetooth/enable
- POST /api/v1/system-controller/network/bluetooth/pair
- POST /api/v1/system-controller/network/bluetooth/scan/start
- POST /api/v1/system-controller/network/bluetooth/scan/stop
- POST /api/v1/system-controller/network/bluetooth/unpair
- POST /api/v1/system-controller/network/wifi/connect
- POST /api/v1/system-controller/network/wifi/disable
- POST /api/v1/system-controller/network/wifi/disconnect
- POST /api/v1/system-controller/network/wifi/enable
- POST /api/v1/system-controller/services/{name}/restart
- POST /api/v1/system-controller/system/reboot
- POST /api/v1/system-controller/system/shutdown
- POST /api/v1/system/reboot
- POST /api/v1/system/shutdown
- POST /api/v1/video/select
- POST /api/v1/vrx/tune
<!-- API_INDEX_END -->

## WebSocket (RX Events)
Envelope:
```json
{"type":"EVENT_TYPE","timestamp_ms":1700000000000,"source":"aggregator","data":{}}
```
Liveness: >=3 messages in 10s.

Examples:
```json
{"type":"TELEMETRY_UPDATE","timestamp_ms":1700000000000,"source":"aggregator","data":{"timestamp_ms":1700000000000,"system":{"status":"ok"}}}
```
```json
{"type":"CONTACT_NEW","timestamp_ms":1700000000000,"source":"remoteid","data":{"id":"rid:123","type":"REMOTE_ID","last_seen_ts":1700000000000,"lat":23.0,"lon":72.0}}
```
```json
{"type":"CONTACT_UPDATE","timestamp_ms":1700000000000,"source":"remoteid","data":{"id":"rid:123","last_seen_ts":1700000000000}}
```
```json
{"type":"CONTACT_LOST","timestamp_ms":1700000000000,"source":"remoteid","data":{"id":"rid:123","last_seen_ts":1700000000000}}
```
```json
{"type":"REPLAY_STATE","timestamp_ms":1700000000000,"source":"remoteid","data":{"active":false,"source":"none"}}
```
```json
{"type":"COMMAND_ACK","timestamp_ms":1700000000000,"source":"aggregator","data":{"command":"scan/start","command_id":"uuid","ok":true,"detail":null}}
```

Reconnect rules: exponential backoff (1s, 2s, 5s, 10s), refresh `/api/v1/status` after reconnect.

### WebSocket Clients
JavaScript:
```js
const ws = new WebSocket("ws://127.0.0.1:8001/api/v1/ws");
ws.onmessage = (evt) => console.log(JSON.parse(evt.data));
```
Python:
```python
import websocket, json
ws = websocket.WebSocket()
ws.connect("ws://127.0.0.1:8001/api/v1/ws")
print(json.loads(ws.recv()))
```

## Endpoint Reference (Per Endpoint)
All examples use `BASE=http://127.0.0.1:8001/api/v1` unless noted.

### Backend Aggregator API

#### GET /api/v1/antsdr

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/antsdr
```

Response:
```json
{
  "timestamp_ms": 1700000000000,
  "connected": false,
  "last_error": "antsdr_unreachable"
}
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### GET /api/v1/antsdr/gain

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/antsdr/gain
```

Response:
```json
{
  "timestamp_ms": 1700000000000,
  "mode": "auto"
}
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### GET /api/v1/antsdr/stats

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/antsdr/stats
```

Response:
```json
{
  "timestamp_ms": 1700000000000,
  "frames_processed": 10,
  "events_emitted": 5
}
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### GET /api/v1/antsdr/sweep/state

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/antsdr/sweep/state
```

Response:
```json
{
  "timestamp_ms": 1700000000000,
  "running": false,
  "plans": [
    {
      "name": "default",
      "start_hz": 5700000000,
      "end_hz": 5900000000,
      "step_hz": 2000000
    }
  ]
}
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### GET /api/v1/audio

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/audio
```

Response:
```json
{
  "timestamp_ms": 1700000000000,
  "status": "ok",
  "muted": false,
  "volume_percent": 100
}
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### GET /api/v1/contacts

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/contacts
```

Response:
```json
{
  "contacts": [
    {
      "id": "fpv:1",
      "type": "FPV",
      "source": "esp32",
      "last_seen_ts": 1700000000000,
      "severity": "unknown",
      "vrx_id": 1,
      "freq_hz": 5740000000,
      "rssi_raw": 632,
      "selected": 1
    }
  ]
}
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### GET /api/v1/esp32

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/esp32
```

Response:
```json
{
  "timestamp_ms": 1700000000000,
  "connected": true,
  "last_seen_ms": 1700000000000,
  "heartbeat": {
    "ok": true,
    "interval_ms": 1000,
    "last_heartbeat_ms": 1700000000000
  },
  "capabilities": {
    "leds": true,
    "vrx": true,
    "video_switch": true
  }
}
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### GET /api/v1/esp32/config

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/esp32/config
```

Response:
```json
{
  "timestamp_ms": 1700000000000,
  "config": {
    "vrx_default_id": 1
  },
  "schema_version": "1"
}
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### GET /api/v1/gps

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/gps
```

Response:
```json
{
  "timestamp_ms": 1700000000000,
  "fix": "NO_FIX",
  "satellites": {
    "in_view": 0,
    "in_use": 0
  },
  "latitude": null,
  "longitude": null,
  "last_update_ms": 1700000000000,
  "source": "gpsd"
}
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### GET /api/v1/health

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/health
```

Response:
```json
{
  "status": "ok",
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### GET /api/v1/network

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/network
```

Response:
```json
{
  "wifi": {
    "timestamp_ms": 1700000000000,
    "enabled": true,
    "connected": true,
    "ssid": "lab"
  },
  "bluetooth": {
    "timestamp_ms": 1700000000000,
    "enabled": false,
    "scanning": false,
    "paired_count": 0,
    "connected_devices": []
  }
}
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### GET /api/v1/network/bluetooth/devices

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/network/bluetooth/devices
```

Response:
```json
{
  "timestamp_ms": 1700000000000,
  "devices": [
    {
      "addr": "00:11:22:33:44:55",
      "name": "sensor",
      "paired": true,
      "connected": false,
      "rssi_dbm": -40
    }
  ]
}
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### GET /api/v1/network/bluetooth/state

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/network/bluetooth/state
```

Response:
```json
{
  "timestamp_ms": 1700000000000,
  "enabled": false,
  "scanning": false,
  "paired_count": 0,
  "connected_devices": [],
  "last_update_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### GET /api/v1/network/wifi/scan

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/network/wifi/scan
```

Response:
```json
{
  "timestamp_ms": 1700000000000,
  "networks": [
    {
      "ssid": "lab",
      "bssid": "aa:bb:cc:dd:ee:ff",
      "security": "wpa2",
      "signal_dbm": -48,
      "channel": 6,
      "frequency_mhz": 2437,
      "known": true
    }
  ]
}
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### GET /api/v1/network/wifi/state

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/network/wifi/state
```

Response:
```json
{
  "timestamp_ms": 1700000000000,
  "enabled": true,
  "connected": true,
  "ssid": "lab",
  "ip": "192.168.1.35",
  "last_update_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### GET /api/v1/power

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/power
```

Response:
```json
{
  "timestamp_ms": 1700000000000,
  "status": "ok",
  "soc_percent": 98
}
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### GET /api/v1/remote_id

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/remote_id
```

Response:
```json
{
  "timestamp_ms": 1700000000000,
  "state": "degraded",
  "mode": "live",
  "capture_active": true,
  "last_error": "no_odid_frames"
}
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### GET /api/v1/remote_id/contacts

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/remote_id/contacts
```

Response:
```json
{
  "timestamp_ms": 1700000000000,
  "contacts": [
    {
      "id": "rid:123",
      "type": "REMOTE_ID",
      "source": "remoteid",
      "last_seen_ts": 1700000000000,
      "severity": "unknown",
      "lat": 23.0,
      "lon": 72.0
    }
  ]
}
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### GET /api/v1/remote_id/stats

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/remote_id/stats
```

Response:
```json
{
  "timestamp_ms": 1700000000000,
  "frames": 10,
  "decoded": 2,
  "dropped": 0,
  "dedupe_hits": 1
}
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### GET /api/v1/rf

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/rf
```

Response:
```json
{
  "status": "offline",
  "scan_active": false,
  "last_error": "antsdr_unreachable",
  "last_event_type": "RF_SCAN_OFFLINE",
  "last_timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### GET /api/v1/services

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/services
```

Response:
```json
[
  {
    "name": "ndefender-backend",
    "active_state": "active",
    "sub_state": "running",
    "restart_count": 0
  }
]
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### GET /api/v1/status

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/status
```

Response:
```json
{
  "timestamp_ms": 1700000000000,
  "overall_ok": false,
  "system": {
    "status": "degraded",
    "uptime_s": 4671
  },
  "power": {
    "status": "ok",
    "soc_percent": 98
  },
  "rf": {
    "status": "offline",
    "scan_active": false,
    "last_error": "antsdr_unreachable",
    "last_timestamp_ms": 1700000000000
  },
  "remote_id": {
    "state": "degraded",
    "mode": "live",
    "capture_active": true
  },
  "vrx": {
    "selected": 1,
    "scan_state": "idle",
    "sys": {
      "status": "CONNECTED"
    },
    "vrx": [
      {
        "id": 1,
        "freq_hz": 5740000000,
        "rssi_raw": 632
      }
    ]
  },
  "fpv": {
    "selected": 1,
    "scan_state": "idle",
    "freq_hz": 5740000000,
    "rssi_raw": 632
  },
  "video": {
    "selected": 1,
    "status": "ok"
  },
  "services": [],
  "network": {
    "wifi": {
      "timestamp_ms": 1700000000000,
      "enabled": true,
      "connected": true,
      "ssid": "lab",
      "ip": "192.168.1.35"
    },
    "bluetooth": {
      "timestamp_ms": 1700000000000,
      "enabled": false,
      "scanning": false,
      "paired_count": 0,
      "connected_devices": []
    }
  },
  "gps": {
    "timestamp_ms": 1700000000000,
    "fix": "NO_FIX",
    "satellites": {
      "in_view": 0,
      "in_use": 0
    },
    "latitude": null,
    "longitude": null,
    "last_update_ms": 1700000000000,
    "source": "gpsd"
  },
  "esp32": {
    "timestamp_ms": 1700000000000,
    "connected": true,
    "last_seen_ms": 1700000000000
  },
  "antsdr": {
    "timestamp_ms": 1700000000000,
    "connected": false,
    "last_error": "antsdr_unreachable"
  },
  "audio": {
    "timestamp_ms": 1700000000000,
    "status": "ok",
    "muted": false,
    "volume_percent": 100
  },
  "contacts": [],
  "replay": {
    "active": false,
    "source": "none"
  }
}
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### GET /api/v1/system

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/system
```

Response:
```json
{
  "timestamp_ms": 1700000000000,
  "status": "ok",
  "uptime_s": 4671
}
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### GET /api/v1/video

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/video
```

Response:
```json
{
  "selected": 1,
  "status": "ok"
}
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### GET /api/v1/ws

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/ws
```

Response:
```json
{
  "detail": "upgrade_to_websocket"
}
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### POST /api/v1/antsdr/device/reset

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm_required on confirm=false; rate limits apply.

Request:
```json
{
  "payload": {},
  "confirm": true
}
```

Curl:
```bash
curl -sS -X POST $BASE/antsdr/device/reset -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": true}'
```

Response:
```json
{
  "command": "antsdr/device/reset",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "confirm_required"
}
```

#### POST /api/v1/antsdr/gain/set

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm=false allowed; rate limits apply.

Request:
```json
{
  "payload": {
    "mode": "auto"
  },
  "confirm": false
}
```

Curl:
```bash
curl -sS -X POST $BASE/antsdr/gain/set -H 'Content-Type: application/json' -d '{"payload": {"mode": "auto"}, "confirm": false}'
```

Response:
```json
{
  "command": "antsdr/gain/set",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "invalid_state"
}
```

#### POST /api/v1/antsdr/sweep/start

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm=false allowed; rate limits apply.

Request:
```json
{
  "payload": {
    "plan": "default"
  },
  "confirm": false
}
```

Curl:
```bash
curl -sS -X POST $BASE/antsdr/sweep/start -H 'Content-Type: application/json' -d '{"payload": {"plan": "default"}, "confirm": false}'
```

Response:
```json
{
  "command": "antsdr/sweep/start",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "invalid_state"
}
```

#### POST /api/v1/antsdr/sweep/stop

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm=false allowed; rate limits apply.

Request:
```json
{
  "payload": {},
  "confirm": false
}
```

Curl:
```bash
curl -sS -X POST $BASE/antsdr/sweep/stop -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

Response:
```json
{
  "command": "antsdr/sweep/stop",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "invalid_state"
}
```

#### POST /api/v1/audio/mute

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm=false allowed; rate limits apply.

Request:
```json
{
  "payload": {
    "muted": true
  },
  "confirm": false
}
```

Curl:
```bash
curl -sS -X POST $BASE/audio/mute -H 'Content-Type: application/json' -d '{"payload": {"muted": true}, "confirm": false}'
```

Response:
```json
{
  "command": "audio/mute",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "invalid_state"
}
```

#### POST /api/v1/audio/volume

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm=false allowed; rate limits apply.

Request:
```json
{
  "payload": {
    "volume_percent": 50
  },
  "confirm": false
}
```

Curl:
```bash
curl -sS -X POST $BASE/audio/volume -H 'Content-Type: application/json' -d '{"payload": {"volume_percent": 50}, "confirm": false}'
```

Response:
```json
{
  "command": "audio/volume",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "invalid_state"
}
```

#### POST /api/v1/esp32/buttons/simulate

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm=false allowed; rate limits apply.

Request:
```json
{
  "payload": {
    "button": "mute",
    "action": "press"
  },
  "confirm": false
}
```

Curl:
```bash
curl -sS -X POST $BASE/esp32/buttons/simulate -H 'Content-Type: application/json' -d '{"payload": {"button": "mute", "action": "press"}, "confirm": false}'
```

Response:
```json
{
  "command": "esp32/buttons/simulate",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "invalid_state"
}
```

#### POST /api/v1/esp32/buzzer

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm=false allowed; rate limits apply.

Request:
```json
{
  "payload": {
    "mode": "beep",
    "duration_ms": 250
  },
  "confirm": false
}
```

Curl:
```bash
curl -sS -X POST $BASE/esp32/buzzer -H 'Content-Type: application/json' -d '{"payload": {"mode": "beep", "duration_ms": 250}, "confirm": false}'
```

Response:
```json
{
  "command": "esp32/buzzer",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "invalid_state"
}
```

#### POST /api/v1/esp32/config

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm=false allowed; rate limits apply.

Request:
```json
{
  "payload": {
    "config": {
      "vrx_default_id": 1
    }
  },
  "confirm": false
}
```

Curl:
```bash
curl -sS -X POST $BASE/esp32/config -H 'Content-Type: application/json' -d '{"payload": {"config": {"vrx_default_id": 1}}, "confirm": false}'
```

Response:
```json
{
  "command": "esp32/config",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "invalid_state"
}
```

#### POST /api/v1/esp32/leds

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm=false allowed; rate limits apply.

Request:
```json
{
  "payload": {
    "red": true,
    "yellow": false,
    "green": false
  },
  "confirm": false
}
```

Curl:
```bash
curl -sS -X POST $BASE/esp32/leds -H 'Content-Type: application/json' -d '{"payload": {"red": true, "yellow": false, "green": false}, "confirm": false}'
```

Response:
```json
{
  "command": "esp32/leds",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "invalid_state"
}
```

#### POST /api/v1/gps/restart

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm=false allowed; rate limits apply.

Request:
```json
{
  "payload": {},
  "confirm": false
}
```

Curl:
```bash
curl -sS -X POST $BASE/gps/restart -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

Response:
```json
{
  "command": "gps/restart",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "invalid_state"
}
```

#### POST /api/v1/network/bluetooth/disable

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm=false allowed; rate limits apply.

Request:
```json
{
  "payload": {},
  "confirm": false
}
```

Curl:
```bash
curl -sS -X POST $BASE/network/bluetooth/disable -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

Response:
```json
{
  "command": "network/bluetooth/disable",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "invalid_state"
}
```

#### POST /api/v1/network/bluetooth/enable

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm=false allowed; rate limits apply.

Request:
```json
{
  "payload": {
    "enabled": true
  },
  "confirm": false
}
```

Curl:
```bash
curl -sS -X POST $BASE/network/bluetooth/enable -H 'Content-Type: application/json' -d '{"payload": {"enabled": true}, "confirm": false}'
```

Response:
```json
{
  "command": "network/bluetooth/enable",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "invalid_state"
}
```

#### POST /api/v1/network/bluetooth/pair

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm=false allowed; rate limits apply.

Request:
```json
{
  "payload": {
    "addr": "00:11:22:33:44:55",
    "pin": "0000"
  },
  "confirm": false
}
```

Curl:
```bash
curl -sS -X POST $BASE/network/bluetooth/pair -H 'Content-Type: application/json' -d '{"payload": {"addr": "00:11:22:33:44:55", "pin": "0000"}, "confirm": false}'
```

Response:
```json
{
  "command": "network/bluetooth/pair",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "invalid_state"
}
```

#### POST /api/v1/network/bluetooth/scan/start

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm=false allowed; rate limits apply.

Request:
```json
{
  "payload": {},
  "confirm": false
}
```

Curl:
```bash
curl -sS -X POST $BASE/network/bluetooth/scan/start -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

Response:
```json
{
  "command": "network/bluetooth/scan/start",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "invalid_state"
}
```

#### POST /api/v1/network/bluetooth/scan/stop

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm=false allowed; rate limits apply.

Request:
```json
{
  "payload": {},
  "confirm": false
}
```

Curl:
```bash
curl -sS -X POST $BASE/network/bluetooth/scan/stop -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

Response:
```json
{
  "command": "network/bluetooth/scan/stop",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "invalid_state"
}
```

#### POST /api/v1/network/bluetooth/unpair

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm=false allowed; rate limits apply.

Request:
```json
{
  "payload": {
    "addr": "00:11:22:33:44:55"
  },
  "confirm": false
}
```

Curl:
```bash
curl -sS -X POST $BASE/network/bluetooth/unpair -H 'Content-Type: application/json' -d '{"payload": {"addr": "00:11:22:33:44:55"}, "confirm": false}'
```

Response:
```json
{
  "command": "network/bluetooth/unpair",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "invalid_state"
}
```

#### POST /api/v1/network/wifi/connect

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm=false allowed; rate limits apply.

Request:
```json
{
  "payload": {
    "ssid": "lab",
    "password": "secret"
  },
  "confirm": false
}
```

Curl:
```bash
curl -sS -X POST $BASE/network/wifi/connect -H 'Content-Type: application/json' -d '{"payload": {"ssid": "lab", "password": "secret"}, "confirm": false}'
```

Response:
```json
{
  "command": "network/wifi/connect",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "invalid_state"
}
```

#### POST /api/v1/network/wifi/disable

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm=false allowed; rate limits apply.

Request:
```json
{
  "payload": {},
  "confirm": false
}
```

Curl:
```bash
curl -sS -X POST $BASE/network/wifi/disable -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

Response:
```json
{
  "command": "network/wifi/disable",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "invalid_state"
}
```

#### POST /api/v1/network/wifi/disconnect

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm=false allowed; rate limits apply.

Request:
```json
{
  "payload": {},
  "confirm": false
}
```

Curl:
```bash
curl -sS -X POST $BASE/network/wifi/disconnect -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

Response:
```json
{
  "command": "network/wifi/disconnect",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "invalid_state"
}
```

#### POST /api/v1/network/wifi/enable

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm=false allowed; rate limits apply.

Request:
```json
{
  "payload": {
    "enabled": true
  },
  "confirm": false
}
```

Curl:
```bash
curl -sS -X POST $BASE/network/wifi/enable -H 'Content-Type: application/json' -d '{"payload": {"enabled": true}, "confirm": false}'
```

Response:
```json
{
  "command": "network/wifi/enable",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "invalid_state"
}
```

#### POST /api/v1/remote_id/monitor/start

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm=false allowed; rate limits apply.

Request:
```json
{
  "payload": {},
  "confirm": false
}
```

Curl:
```bash
curl -sS -X POST $BASE/remote_id/monitor/start -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

Response:
```json
{
  "command": "remote_id/monitor/start",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "invalid_state"
}
```

#### POST /api/v1/remote_id/monitor/stop

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm=false allowed; rate limits apply.

Request:
```json
{
  "payload": {},
  "confirm": false
}
```

Curl:
```bash
curl -sS -X POST $BASE/remote_id/monitor/stop -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

Response:
```json
{
  "command": "remote_id/monitor/stop",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "invalid_state"
}
```

#### POST /api/v1/scan/start

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm=false allowed; rate limits apply.

Request:
```json
{
  "payload": {},
  "confirm": false
}
```

Curl:
```bash
curl -sS -X POST $BASE/scan/start -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

Response:
```json
{
  "command": "scan/start",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "invalid_state"
}
```

#### POST /api/v1/scan/stop

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm=false allowed; rate limits apply.

Request:
```json
{
  "payload": {},
  "confirm": false
}
```

Curl:
```bash
curl -sS -X POST $BASE/scan/stop -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

Response:
```json
{
  "command": "scan/stop",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "invalid_state"
}
```

#### POST /api/v1/system/reboot

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm_required on confirm=false; rate limits apply.

Request:
```json
{
  "payload": {},
  "confirm": true
}
```

Curl:
```bash
curl -sS -X POST $BASE/system/reboot -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": true}'
```

Response:
```json
{
  "command": "system/reboot",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "confirm_required"
}
```

#### POST /api/v1/system/shutdown

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm_required on confirm=false; rate limits apply.

Request:
```json
{
  "payload": {},
  "confirm": true
}
```

Curl:
```bash
curl -sS -X POST $BASE/system/shutdown -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": true}'
```

Response:
```json
{
  "command": "system/shutdown",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "confirm_required"
}
```

#### POST /api/v1/video/select

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm=false allowed; rate limits apply.

Request:
```json
{
  "payload": {
    "sel": 1
  },
  "confirm": false
}
```

Curl:
```bash
curl -sS -X POST $BASE/video/select -H 'Content-Type: application/json' -d '{"payload": {"sel": 1}, "confirm": false}'
```

Response:
```json
{
  "command": "video/select",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "invalid_state"
}
```

#### POST /api/v1/vrx/tune

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm=false allowed; rate limits apply.

Request:
```json
{
  "payload": {
    "vrx_id": 1,
    "freq_hz": 5740000000
  },
  "confirm": false
}
```

Curl:
```bash
curl -sS -X POST $BASE/vrx/tune -H 'Content-Type: application/json' -d '{"payload": {"vrx_id": 1, "freq_hz": 5740000000}, "confirm": false}'
```

Response:
```json
{
  "command": "vrx/tune",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "invalid_state"
}
```



### System Controller API

#### GET /api/v1/system-controller/audio

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/system-controller/audio
```

Response:
```json
{
  "timestamp_ms": 1700000000000,
  "status": "ok",
  "muted": false,
  "volume_percent": 100
}
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### GET /api/v1/system-controller/gps

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/system-controller/gps
```

Response:
```json
{
  "timestamp_ms": 1700000000000,
  "fix": "NO_FIX",
  "satellites": {
    "in_view": 0,
    "in_use": 0
  },
  "latitude": null,
  "longitude": null,
  "last_update_ms": 1700000000000,
  "source": "gpsd"
}
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### GET /api/v1/system-controller/health

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/system-controller/health
```

Response:
```json
{
  "status": "ok",
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### GET /api/v1/system-controller/network

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/system-controller/network
```

Response:
```json
{
  "wifi": {
    "timestamp_ms": 1700000000000,
    "enabled": true,
    "connected": true,
    "ssid": "lab"
  },
  "bluetooth": {
    "timestamp_ms": 1700000000000,
    "enabled": false,
    "scanning": false,
    "paired_count": 0,
    "connected_devices": []
  }
}
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### GET /api/v1/system-controller/network/bluetooth/devices

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/system-controller/network/bluetooth/devices
```

Response:
```json
{
  "timestamp_ms": 1700000000000,
  "devices": [
    {
      "addr": "00:11:22:33:44:55",
      "name": "sensor",
      "paired": true,
      "connected": false,
      "rssi_dbm": -40
    }
  ]
}
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### GET /api/v1/system-controller/network/bluetooth/state

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/system-controller/network/bluetooth/state
```

Response:
```json
{
  "timestamp_ms": 1700000000000,
  "enabled": false,
  "scanning": false,
  "paired_count": 0,
  "connected_devices": [],
  "last_update_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### GET /api/v1/system-controller/network/wifi/scan

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/system-controller/network/wifi/scan
```

Response:
```json
{
  "timestamp_ms": 1700000000000,
  "networks": [
    {
      "ssid": "lab",
      "bssid": "aa:bb:cc:dd:ee:ff",
      "security": "wpa2",
      "signal_dbm": -48,
      "channel": 6,
      "frequency_mhz": 2437,
      "known": true
    }
  ]
}
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### GET /api/v1/system-controller/network/wifi/state

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/system-controller/network/wifi/state
```

Response:
```json
{
  "timestamp_ms": 1700000000000,
  "enabled": true,
  "connected": true,
  "ssid": "lab",
  "ip": "192.168.1.35",
  "last_update_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### GET /api/v1/system-controller/services

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/system-controller/services
```

Response:
```json
[
  {
    "name": "gpsd",
    "active_state": "active",
    "sub_state": "running",
    "restart_count": 0
  }
]
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### GET /api/v1/system-controller/status

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/system-controller/status
```

Response:
```json
{
  "timestamp_ms": 1700000000000,
  "system": {
    "status": "ok"
  },
  "ups": {
    "status": "ok"
  },
  "services": [],
  "network": {},
  "audio": {}
}
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### GET /api/v1/system-controller/system

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/system-controller/system
```

Response:
```json
{
  "timestamp_ms": 1700000000000,
  "status": "ok",
  "uptime_s": 4671
}
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### GET /api/v1/system-controller/ups

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/system-controller/ups
```

Response:
```json
{
  "timestamp_ms": 1700000000000,
  "status": "ok",
  "soc_percent": 98
}
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### GET /api/v1/system-controller/ws

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/system-controller/ws
```

Response:
```json
{
  "detail": "upgrade_to_websocket"
}
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### POST /api/v1/system-controller/audio/mute

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm=false allowed; rate limits apply.

Request:
```json
{
  "payload": {
    "muted": true
  },
  "confirm": false
}
```

Curl:
```bash
curl -sS -X POST $BASE/system-controller/audio/mute -H 'Content-Type: application/json' -d '{"payload": {"muted": true}, "confirm": false}'
```

Response:
```json
{
  "command": "system-controller/audio/mute",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "invalid_state"
}
```

#### POST /api/v1/system-controller/audio/volume

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm=false allowed; rate limits apply.

Request:
```json
{
  "payload": {
    "volume_percent": 50
  },
  "confirm": false
}
```

Curl:
```bash
curl -sS -X POST $BASE/system-controller/audio/volume -H 'Content-Type: application/json' -d '{"payload": {"volume_percent": 50}, "confirm": false}'
```

Response:
```json
{
  "command": "system-controller/audio/volume",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "invalid_state"
}
```

#### POST /api/v1/system-controller/gps/restart

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm=false allowed; rate limits apply.

Request:
```json
{
  "payload": {},
  "confirm": false
}
```

Curl:
```bash
curl -sS -X POST $BASE/system-controller/gps/restart -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

Response:
```json
{
  "command": "system-controller/gps/restart",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "invalid_state"
}
```

#### POST /api/v1/system-controller/network/bluetooth/disable

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm=false allowed; rate limits apply.

Request:
```json
{
  "payload": {},
  "confirm": false
}
```

Curl:
```bash
curl -sS -X POST $BASE/system-controller/network/bluetooth/disable -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

Response:
```json
{
  "command": "system-controller/network/bluetooth/disable",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "invalid_state"
}
```

#### POST /api/v1/system-controller/network/bluetooth/enable

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm=false allowed; rate limits apply.

Request:
```json
{
  "payload": {
    "enabled": true
  },
  "confirm": false
}
```

Curl:
```bash
curl -sS -X POST $BASE/system-controller/network/bluetooth/enable -H 'Content-Type: application/json' -d '{"payload": {"enabled": true}, "confirm": false}'
```

Response:
```json
{
  "command": "system-controller/network/bluetooth/enable",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "invalid_state"
}
```

#### POST /api/v1/system-controller/network/bluetooth/pair

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm=false allowed; rate limits apply.

Request:
```json
{
  "payload": {
    "addr": "00:11:22:33:44:55",
    "pin": "0000"
  },
  "confirm": false
}
```

Curl:
```bash
curl -sS -X POST $BASE/system-controller/network/bluetooth/pair -H 'Content-Type: application/json' -d '{"payload": {"addr": "00:11:22:33:44:55", "pin": "0000"}, "confirm": false}'
```

Response:
```json
{
  "command": "system-controller/network/bluetooth/pair",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "invalid_state"
}
```

#### POST /api/v1/system-controller/network/bluetooth/scan/start

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm=false allowed; rate limits apply.

Request:
```json
{
  "payload": {},
  "confirm": false
}
```

Curl:
```bash
curl -sS -X POST $BASE/system-controller/network/bluetooth/scan/start -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

Response:
```json
{
  "command": "system-controller/network/bluetooth/scan/start",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "invalid_state"
}
```

#### POST /api/v1/system-controller/network/bluetooth/scan/stop

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm=false allowed; rate limits apply.

Request:
```json
{
  "payload": {},
  "confirm": false
}
```

Curl:
```bash
curl -sS -X POST $BASE/system-controller/network/bluetooth/scan/stop -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

Response:
```json
{
  "command": "system-controller/network/bluetooth/scan/stop",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "invalid_state"
}
```

#### POST /api/v1/system-controller/network/bluetooth/unpair

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm=false allowed; rate limits apply.

Request:
```json
{
  "payload": {
    "addr": "00:11:22:33:44:55"
  },
  "confirm": false
}
```

Curl:
```bash
curl -sS -X POST $BASE/system-controller/network/bluetooth/unpair -H 'Content-Type: application/json' -d '{"payload": {"addr": "00:11:22:33:44:55"}, "confirm": false}'
```

Response:
```json
{
  "command": "system-controller/network/bluetooth/unpair",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "invalid_state"
}
```

#### POST /api/v1/system-controller/network/wifi/connect

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm=false allowed; rate limits apply.

Request:
```json
{
  "payload": {
    "ssid": "lab",
    "password": "secret"
  },
  "confirm": false
}
```

Curl:
```bash
curl -sS -X POST $BASE/system-controller/network/wifi/connect -H 'Content-Type: application/json' -d '{"payload": {"ssid": "lab", "password": "secret"}, "confirm": false}'
```

Response:
```json
{
  "command": "system-controller/network/wifi/connect",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "invalid_state"
}
```

#### POST /api/v1/system-controller/network/wifi/disable

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm=false allowed; rate limits apply.

Request:
```json
{
  "payload": {},
  "confirm": false
}
```

Curl:
```bash
curl -sS -X POST $BASE/system-controller/network/wifi/disable -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

Response:
```json
{
  "command": "system-controller/network/wifi/disable",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "invalid_state"
}
```

#### POST /api/v1/system-controller/network/wifi/disconnect

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm=false allowed; rate limits apply.

Request:
```json
{
  "payload": {},
  "confirm": false
}
```

Curl:
```bash
curl -sS -X POST $BASE/system-controller/network/wifi/disconnect -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

Response:
```json
{
  "command": "system-controller/network/wifi/disconnect",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "invalid_state"
}
```

#### POST /api/v1/system-controller/network/wifi/enable

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm=false allowed; rate limits apply.

Request:
```json
{
  "payload": {
    "enabled": true
  },
  "confirm": false
}
```

Curl:
```bash
curl -sS -X POST $BASE/system-controller/network/wifi/enable -H 'Content-Type: application/json' -d '{"payload": {"enabled": true}, "confirm": false}'
```

Response:
```json
{
  "command": "system-controller/network/wifi/enable",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "invalid_state"
}
```

#### POST /api/v1/system-controller/services/{name}/restart

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm_required on confirm=false; rate limits apply.

Request:
```json
{
  "payload": {},
  "confirm": true
}
```

Curl:
```bash
curl -sS -X POST $BASE/system-controller/services/{name}/restart -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": true}'
```

Response:
```json
{
  "command": "system-controller/services/{name}/restart",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "confirm_required"
}
```

#### POST /api/v1/system-controller/system/reboot

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm_required on confirm=false; rate limits apply.

Request:
```json
{
  "payload": {},
  "confirm": true
}
```

Curl:
```bash
curl -sS -X POST $BASE/system-controller/system/reboot -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": true}'
```

Response:
```json
{
  "command": "system-controller/system/reboot",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "confirm_required"
}
```

#### POST /api/v1/system-controller/system/shutdown

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm_required on confirm=false; rate limits apply.

Request:
```json
{
  "payload": {},
  "confirm": true
}
```

Curl:
```bash
curl -sS -X POST $BASE/system-controller/system/shutdown -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": true}'
```

Response:
```json
{
  "command": "system-controller/system/shutdown",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "confirm_required"
}
```



### RFScan (AntSDR Scan) API

#### GET /api/v1/antsdr-scan/config

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/antsdr-scan/config
```

Response:
```json
{
  "timestamp_ms": 1700000000000,
  "output_jsonl": "/opt/ndefender/logs/antsdr_scan.jsonl"
}
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### GET /api/v1/antsdr-scan/device

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/antsdr-scan/device
```

Response:
```json
{
  "timestamp_ms": 1700000000000,
  "connected": false,
  "last_error": "device_not_connected"
}
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### GET /api/v1/antsdr-scan/events/last

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/antsdr-scan/events/last
```

Response:
```json
{
  "timestamp_ms": 1700000000000,
  "events": [
    {
      "type": "RF_CONTACT_NEW",
      "timestamp_ms": 1700000000000,
      "source": "antsdr",
      "data": {
        "id": "rf:1",
        "freq_hz": 5740000000,
        "rssi_dbm": -48
      }
    }
  ]
}
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### GET /api/v1/antsdr-scan/gain

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/antsdr-scan/gain
```

Response:
```json
{
  "timestamp_ms": 1700000000000,
  "mode": "auto"
}
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### GET /api/v1/antsdr-scan/health

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/antsdr-scan/health
```

Response:
```json
{
  "status": "ok",
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### GET /api/v1/antsdr-scan/stats

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/antsdr-scan/stats
```

Response:
```json
{
  "timestamp_ms": 1700000000000,
  "frames_processed": 10,
  "events_emitted": 5
}
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### GET /api/v1/antsdr-scan/sweep/state

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/antsdr-scan/sweep/state
```

Response:
```json
{
  "timestamp_ms": 1700000000000,
  "running": false,
  "plans": [
    {
      "name": "default",
      "start_hz": 5700000000,
      "end_hz": 5900000000,
      "step_hz": 2000000
    }
  ]
}
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### GET /api/v1/antsdr-scan/version

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/antsdr-scan/version
```

Response:
```json
{
  "version": "dev",
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### POST /api/v1/antsdr-scan/config/reload

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm=false allowed; rate limits apply.

Request:
```json
{
  "payload": {},
  "confirm": false
}
```

Curl:
```bash
curl -sS -X POST $BASE/antsdr-scan/config/reload -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

Response:
```json
{
  "command": "antsdr-scan/config/reload",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "invalid_state"
}
```

#### POST /api/v1/antsdr-scan/device/calibrate

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm_required on confirm=false; rate limits apply.

Request:
```json
{
  "payload": {
    "kind": "rf_dc"
  },
  "confirm": true
}
```

Curl:
```bash
curl -sS -X POST $BASE/antsdr-scan/device/calibrate -H 'Content-Type: application/json' -d '{"payload": {"kind": "rf_dc"}, "confirm": true}'
```

Response:
```json
{
  "command": "antsdr-scan/device/calibrate",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "confirm_required"
}
```

#### POST /api/v1/antsdr-scan/device/reset

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm_required on confirm=false; rate limits apply.

Request:
```json
{
  "payload": {},
  "confirm": true
}
```

Curl:
```bash
curl -sS -X POST $BASE/antsdr-scan/device/reset -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": true}'
```

Response:
```json
{
  "command": "antsdr-scan/device/reset",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "confirm_required"
}
```

#### POST /api/v1/antsdr-scan/gain/set

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm=false allowed; rate limits apply.

Request:
```json
{
  "payload": {
    "mode": "auto"
  },
  "confirm": false
}
```

Curl:
```bash
curl -sS -X POST $BASE/antsdr-scan/gain/set -H 'Content-Type: application/json' -d '{"payload": {"mode": "auto"}, "confirm": false}'
```

Response:
```json
{
  "command": "antsdr-scan/gain/set",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "invalid_state"
}
```

#### POST /api/v1/antsdr-scan/sweep/start

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm=false allowed; rate limits apply.

Request:
```json
{
  "payload": {
    "plan": "default"
  },
  "confirm": false
}
```

Curl:
```bash
curl -sS -X POST $BASE/antsdr-scan/sweep/start -H 'Content-Type: application/json' -d '{"payload": {"plan": "default"}, "confirm": false}'
```

Response:
```json
{
  "command": "antsdr-scan/sweep/start",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "invalid_state"
}
```

#### POST /api/v1/antsdr-scan/sweep/stop

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm=false allowed; rate limits apply.

Request:
```json
{
  "payload": {},
  "confirm": false
}
```

Curl:
```bash
curl -sS -X POST $BASE/antsdr-scan/sweep/stop -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

Response:
```json
{
  "command": "antsdr-scan/sweep/stop",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "invalid_state"
}
```



### RemoteID Engine API

#### GET /api/v1/remoteid-engine/contacts

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/remoteid-engine/contacts
```

Response:
```json
{
  "timestamp_ms": 1700000000000,
  "contacts": [
    {
      "id": "rid:123",
      "type": "REMOTE_ID",
      "source": "remoteid",
      "last_seen_ts": 1700000000000,
      "severity": "unknown",
      "lat": 23.0,
      "lon": 72.0
    }
  ]
}
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### GET /api/v1/remoteid-engine/health

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/remoteid-engine/health
```

Response:
```json
{
  "status": "ok",
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### GET /api/v1/remoteid-engine/replay/state

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/remoteid-engine/replay/state
```

Response:
```json
{
  "timestamp_ms": 1700000000000,
  "active": false,
  "source": "none"
}
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### GET /api/v1/remoteid-engine/stats

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/remoteid-engine/stats
```

Response:
```json
{
  "timestamp_ms": 1700000000000,
  "frames": 10,
  "decoded": 2,
  "dropped": 0,
  "dedupe_hits": 1
}
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### GET /api/v1/remoteid-engine/status

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/remoteid-engine/status
```

Response:
```json
{
  "timestamp_ms": 1700000000000,
  "state": "degraded",
  "mode": "live",
  "capture_active": true,
  "last_error": "no_odid_frames"
}
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### POST /api/v1/remoteid-engine/monitor/start

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm=false allowed; rate limits apply.

Request:
```json
{
  "payload": {},
  "confirm": false
}
```

Curl:
```bash
curl -sS -X POST $BASE/remoteid-engine/monitor/start -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

Response:
```json
{
  "command": "remoteid-engine/monitor/start",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "invalid_state"
}
```

#### POST /api/v1/remoteid-engine/monitor/stop

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm=false allowed; rate limits apply.

Request:
```json
{
  "payload": {},
  "confirm": false
}
```

Curl:
```bash
curl -sS -X POST $BASE/remoteid-engine/monitor/stop -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

Response:
```json
{
  "command": "remoteid-engine/monitor/stop",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "invalid_state"
}
```

#### POST /api/v1/remoteid-engine/replay/start

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm=false allowed; rate limits apply.

Request:
```json
{
  "payload": {
    "source": "file.jsonl"
  },
  "confirm": false
}
```

Curl:
```bash
curl -sS -X POST $BASE/remoteid-engine/replay/start -H 'Content-Type: application/json' -d '{"payload": {"source": "file.jsonl"}, "confirm": false}'
```

Response:
```json
{
  "command": "remoteid-engine/replay/start",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "invalid_state"
}
```

#### POST /api/v1/remoteid-engine/replay/stop

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm=false allowed; rate limits apply.

Request:
```json
{
  "payload": {},
  "confirm": false
}
```

Curl:
```bash
curl -sS -X POST $BASE/remoteid-engine/replay/stop -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

Response:
```json
{
  "command": "remoteid-engine/replay/stop",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "invalid_state"
}
```



### Observability API

#### GET /api/v1/observability/config

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/observability/config
```

Response:
```json
{
  "timestamp_ms": 1700000000000,
  "profile": "default"
}
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### GET /api/v1/observability/health

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/observability/health
```

Response:
```json
{
  "status": "ok",
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### GET /api/v1/observability/health/detail

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/observability/health/detail
```

Response:
```json
{
  "timestamp_ms": 1700000000000,
  "checks": []
}
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### GET /api/v1/observability/status

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/observability/status
```

Response:
```json
{
  "timestamp_ms": 1700000000000,
  "ok": true
}
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### GET /api/v1/observability/version

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: timestamps are ms; response is contract-shaped.

Request:
```json
{}
```

Curl:
```bash
curl -sS $BASE/observability/version
```

Response:
```json
{
  "timestamp_ms": 1700000000000,
  "version": "dev"
}
```

Errors (example):
```json
{
  "detail": "internal_error"
}
```

#### POST /api/v1/observability/diag/bundle

Purpose: See canonical contract in docs/ALL_IN_ONE_API.md.

Notes: confirm=false allowed; rate limits apply.

Request:
```json
{
  "payload": {},
  "confirm": false
}
```

Curl:
```bash
curl -sS -X POST $BASE/observability/diag/bundle -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

Response:
```json
{
  "command": "observability/diag/bundle",
  "command_id": "uuid",
  "accepted": true,
  "detail": null,
  "timestamp_ms": 1700000000000
}
```

Errors (example):
```json
{
  "detail": "invalid_state"
}
```



## Data Model / Contracts
- TypeScript: `packages/contracts-ts/` (alias to `types/`)
- JSON Schema: `packages/contracts-schema/` (alias to `schemas/`)
- OpenAPI: `packages/openapi/` (alias to `docs/OPENAPI.yaml`)

## Integration Guide for UI (Figma → UI)
- Render `/api/v1/status` first, then merge WS updates.
- Display units exactly: `freq_hz`, `rssi_dbm`, `timestamp_ms`, `latitude`, `longitude`.
- Show explicit offline/degraded reasons using `status` and `last_error`.
- Stale detection: compare `timestamp_ms` to wall time; show stale badge if > 5s.
- Confirm‑gated actions must show a modal and re‑submit with `confirm=true`.
- Threat sorting rules: not implemented in contract; preserve API order.

## Integration Guide for AI Tools
- Use `/api/v1/status` for state, WS for live updates.
- Do not send dangerous commands without explicit operator confirmation.

## Firmware Integration (ESP32)
- ACK correlation uses `data.id == command_id`.
- Telemetry should include uptime fields for health.

## Tooling
- List endpoints: `scripts/docs_endpoints.sh`
- Smoke tests: `scripts/smoke_local.sh`, `scripts/smoke_public.sh`, `scripts/smoke_ws.sh`
