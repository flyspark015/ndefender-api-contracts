# N-Defender API Contracts (Single Source of Truth)

This repository is the canonical specification for all N-Defender REST + WebSocket APIs, covering backend, system controls, RF scan, RemoteID, firmware integration, UI/UX integration, and AI tooling.

Canonical contract:
- `docs/ALL_IN_ONE_API.md`

## Architecture Overview
```
                     Public Internet
                            |
                            |  https://n.flyspark.in/api/v1
                            v
                    +----------------------+
                    | Backend Aggregator   |
                    | FastAPI :8001        |
                    +----------------------+
                       |         |        |
                       |         |        |
         +-------------+   +-----+-----+  +--------------------+
         | System Ctrl |   | RFScan   |  | RemoteID Engine    |
         | FastAPI:8002|   | :8890    |  | (local /api/v1)    |
         +-------------+   +----------+  +--------------------+

Legacy Flask on :8000 is removed/disabled (security hardening).
```

## Topology and Ports
- Aggregator API: `http://127.0.0.1:8001/api/v1`
- System Controller API: `http://127.0.0.1:8002/api/v1`
- RFScan API: `http://127.0.0.1:8890/api/v1`
- Legacy Flask `:8000`: removed/disabled (do not use)

## Contract Rules (Non‑Negotiable)
- Time fields are milliseconds: `timestamp_ms`, `last_update_ms`.
- GPS uses `latitude` and `longitude` only.
- Frequency uses `freq_hz` only.
- Signal uses `rssi_dbm` (dBm).
- WS envelope is `{type,timestamp_ms,source,data}`.
- FastAPI errors are `{"detail":"..."}`.
- Commands use `{"payload":{...},"confirm":false}`.
- Dangerous commands require confirm-gating (see TX section).

## Quick Start (Local)
1. REST snapshot:
```bash
curl -sS http://127.0.0.1:8001/api/v1/status
```
2. WebSocket:
```bash
websocat ws://127.0.0.1:8001/api/v1/ws
```
3. Smoke checks:
```bash
scripts/smoke_local.sh
```

## Validation
- Full contract validation:
```bash
scripts/validate.sh
```

## Routing Canonicalization
- OpenAPI paths are **relative** to the server base in `docs/OPENAPI.yaml` (which includes `/api/v1`).
- README lists **canonical full paths** that include `/api/v1/...`.
- CI enforces that README canonical paths match OpenAPI canonical paths.
- Legacy aliases such as `/status` and `/ws` are **backward‑compat only** if they exist on a given deployment.

## API Index (Strict, CI‑checked)
The list below must exactly match OpenAPI paths. Do not edit without updating OpenAPI.

<!-- API_INDEX_START -->
- GET /api/v1/antsdr
- GET /api/v1/antsdr/gain
- GET /api/v1/antsdr/stats
- GET /api/v1/antsdr/sweep/state
- GET /api/v1/antsdr-scan/config
- GET /api/v1/antsdr-scan/device
- GET /api/v1/antsdr-scan/events/last
- GET /api/v1/antsdr-scan/gain
- GET /api/v1/antsdr-scan/health
- GET /api/v1/antsdr-scan/stats
- GET /api/v1/antsdr-scan/sweep/state
- GET /api/v1/antsdr-scan/version
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
- POST /api/v1/antsdr/device/reset
- POST /api/v1/antsdr/gain/set
- POST /api/v1/antsdr/sweep/start
- POST /api/v1/antsdr/sweep/stop
- POST /api/v1/antsdr-scan/config/reload
- POST /api/v1/antsdr-scan/device/calibrate
- POST /api/v1/antsdr-scan/device/reset
- POST /api/v1/antsdr-scan/gain/set
- POST /api/v1/antsdr-scan/sweep/start
- POST /api/v1/antsdr-scan/sweep/stop
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

## TX Commands (Confirm‑Gating + Rate Limits)
All command endpoints accept:
```json
{"payload":{},"confirm":false}
```
All command endpoints return `CommandResult`:
```json
{"command":"scan/start","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

Confirm‑gating rules:
- Dangerous commands require `confirm=true`.
- First call with `confirm=false` must return HTTP 400:
```json
{"detail":"confirm_required"}
```
- Second call with `confirm=true` succeeds.

Dangerous endpoints:
- `POST /api/v1/system/reboot`
- `POST /api/v1/system/shutdown`
- `POST /api/v1/system-controller/system/reboot`
- `POST /api/v1/system-controller/system/shutdown`
- `POST /api/v1/system-controller/services/{name}/restart`
- `POST /api/v1/antsdr/device/reset`
- `POST /api/v1/antsdr-scan/device/reset`
- `POST /api/v1/antsdr-scan/device/calibrate`

Rate limits:
- Commands: 10/min
- Dangerous: 2/min

## WebSocket (RX Events)
Envelope:
```json
{"type":"EVENT_TYPE","timestamp_ms":1700000000000,"source":"aggregator","data":{}}
```
Liveness requirement: >=3 messages within 10 seconds.

### Event Types (Aggregator WS)
SYSTEM_UPDATE:
```json
{"type":"SYSTEM_UPDATE","timestamp_ms":1700000000000,"source":"aggregator","data":{"timestamp_ms":1700000000000,"overall_ok":false}}
```
COMMAND_ACK:
```json
{"type":"COMMAND_ACK","timestamp_ms":1700000000000,"source":"aggregator","data":{"command":"scan/start","command_id":"uuid","ok":true,"detail":null}}
```
HEARTBEAT:
```json
{"type":"HEARTBEAT","timestamp_ms":1700000000000,"source":"aggregator","data":{"timestamp_ms":1700000000000}}
```
ESP32_TELEMETRY:
```json
{"type":"ESP32_TELEMETRY","timestamp_ms":1700000000000,"source":"esp32","data":{"type":"telemetry","timestamp_ms":1000,"sel":1,"vrx":[{"id":1,"freq_hz":5740000000,"rssi_raw":219}],"video":{"selected":1},"led":{"r":0,"y":1,"g":0},"sys":{"uptime_ms":1000,"heap":123456}}}
```
LOG_EVENT:
```json
{"type":"LOG_EVENT","timestamp_ms":1700000000000,"source":"esp32","data":{"type":"log_event","timestamp_ms":1000,"message":"boot"}}
```
CONTACT_NEW / CONTACT_UPDATE / CONTACT_LOST:
```json
{"type":"CONTACT_NEW","timestamp_ms":1700000000000,"source":"remoteid","data":{"id":"rid:ABC123","type":"REMOTE_ID","lat":37.42,"lon":-122.08,"last_seen_ts":1700000000000}}
```
RF_CONTACT_NEW / RF_CONTACT_UPDATE / RF_CONTACT_LOST:
```json
{"type":"RF_CONTACT_UPDATE","timestamp_ms":1700000000000,"source":"antsdr","data":{"id":"rf:5658000000","freq_hz":5658000000,"rssi_dbm":-48,"last_seen_ts":1700000000000}}
```
TELEMETRY_UPDATE:
```json
{"type":"TELEMETRY_UPDATE","timestamp_ms":1700000000000,"source":"aggregator","data":{"timestamp_ms":1700000000000,"system":{"status":"ok"}}}
```
REPLAY_STATE:
```json
{"type":"REPLAY_STATE","timestamp_ms":1700000000000,"source":"remoteid","data":{"active":false,"source":"none"}}
```

### Event Types (System Controller WS)
LOG_EVENT:
```json
{"type":"LOG_EVENT","timestamp_ms":1700000000000,"source":"system","data":{"message":"HELLO"}}
```
SYSTEM_STATUS:
```json
{"type":"SYSTEM_STATUS","timestamp_ms":1700000000000,"source":"system","data":{"timestamp_ms":1700000000000,"system":{"status":"ok"}}}
```
UPS_UPDATE:
```json
{"type":"UPS_UPDATE","timestamp_ms":1700000000000,"source":"system","data":{"timestamp_ms":1700000000000,"status":"ok","soc_percent":98}}
```
SERVICE_UPDATE:
```json
{"type":"SERVICE_UPDATE","timestamp_ms":1700000000000,"source":"system","data":{"name":"gpsd","active_state":"active","sub_state":"running"}}
```
NETWORK_UPDATE:
```json
{"type":"NETWORK_UPDATE","timestamp_ms":1700000000000,"source":"system","data":{"wifi":{"timestamp_ms":1700000000000,"enabled":true,"connected":true,"ssid":"lab"}}}
```
AUDIO_UPDATE:
```json
{"type":"AUDIO_UPDATE","timestamp_ms":1700000000000,"source":"system","data":{"timestamp_ms":1700000000000,"muted":false,"volume_percent":100}}
```
COMMAND_ACK:
```json
{"type":"COMMAND_ACK","timestamp_ms":1700000000000,"source":"system","data":{"command":"services/restart","ok":true,"detail":null}}
```

### Minimal WebSocket Clients
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

## API Reference (REST)
All examples use:
- Aggregator: `http://127.0.0.1:8001/api/v1`
- System Controller: `http://127.0.0.1:8002/api/v1`
- RFScan: `http://127.0.0.1:8890/api/v1`

### Backend Aggregator (Read)
GET /api/v1/health
Purpose: health check.
Request:
```json
{}
```
Success:
```json
{"status":"ok","timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"internal_error"}
```

GET /api/v1/status
Purpose: full snapshot.
Request:
```json
{}
```
Success:
```json
{"timestamp_ms":1700000000000,"overall_ok":false,"system":{"status":"degraded"},"power":{"status":"ok","soc_percent":98},"rf":{"status":"offline","last_error":"antsdr_unreachable"},"remote_id":{"state":"degraded","mode":"live","capture_active":true},"vrx":{"selected":1,"scan_state":"idle","sys":{"status":"CONNECTED"},"vrx":[{"id":1,"freq_hz":5740000000,"rssi_raw":632}]},"fpv":{"selected":1,"scan_state":"idle","freq_hz":5740000000,"rssi_raw":632},"video":{"selected":1,"status":"ok"},"services":[],"network":{"wifi":{"timestamp_ms":1700000000000,"enabled":true,"connected":true,"ssid":"lab","ip":"192.168.1.35"},"bluetooth":{"timestamp_ms":1700000000000,"enabled":false,"scanning":false,"paired_count":0,"connected_devices":[]}},"gps":{"timestamp_ms":1700000000000,"fix":"NO_FIX","satellites":{"in_view":0,"in_use":0},"last_update_ms":1700000000000,"source":"gpsd"},"esp32":{"timestamp_ms":1700000000000,"connected":true,"last_seen_ms":1700000000000},"antsdr":{"timestamp_ms":1700000000000,"connected":false,"last_error":"antsdr_unreachable"},"audio":{"timestamp_ms":1700000000000,"status":"ok","muted":false,"volume_percent":100},"contacts":[],"replay":{"active":false,"source":"none"}}
```
Errors:
```json
{"detail":"internal_error"}
```

GET /api/v1/contacts
Purpose: unified contacts list.
Request:
```json
{}
```
Success:
```json
{"contacts":[{"id":"fpv:1","type":"FPV","source":"esp32","last_seen_ts":1700000000000,"severity":"unknown","vrx_id":1,"freq_hz":5740000000,"rssi_raw":632,"selected":1}]}
```
Errors:
```json
{"detail":"internal_error"}
```

GET /api/v1/system
Purpose: system stats summary.
Request:
```json
{}
```
Success:
```json
{"timestamp_ms":1700000000000,"status":"ok","uptime_s":4671}
```
Errors:
```json
{"detail":"internal_error"}
```

GET /api/v1/power
Purpose: UPS/power snapshot.
Request:
```json
{}
```
Success:
```json
{"timestamp_ms":1700000000000,"status":"ok","soc_percent":98}
```
Errors:
```json
{"detail":"internal_error"}
```

GET /api/v1/rf
Purpose: RF scan health snapshot.
Request:
```json
{}
```
Success:
```json
{"status":"offline","scan_active":false,"last_error":"antsdr_unreachable","last_event_type":"RF_SCAN_OFFLINE","last_timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"internal_error"}
```

GET /api/v1/video
Purpose: video selection and health.
Request:
```json
{}
```
Success:
```json
{"selected":1,"status":"ok"}
```
Errors:
```json
{"detail":"internal_error"}
```

GET /api/v1/services
Purpose: systemd summary.
Request:
```json
{}
```
Success:
```json
[{"name":"ndefender-backend","active_state":"active","sub_state":"running","restart_count":0}]
```
Errors:
```json
{"detail":"internal_error"}
```

GET /api/v1/network
Purpose: network summary.
Request:
```json
{}
```
Success:
```json
{"wifi":{"timestamp_ms":1700000000000,"enabled":true,"connected":true,"ssid":"lab"},"bluetooth":{"timestamp_ms":1700000000000,"enabled":false,"scanning":false,"paired_count":0,"connected_devices":[]}}
```
Errors:
```json
{"detail":"internal_error"}
```

GET /api/v1/network/wifi/state
Purpose: Wi‑Fi state.
Request:
```json
{}
```
Success:
```json
{"timestamp_ms":1700000000000,"enabled":true,"connected":true,"ssid":"lab","ip":"192.168.1.35","last_update_ms":1700000000000}
```
Errors:
```json
{"detail":"internal_error"}
```

GET /api/v1/network/wifi/scan
Purpose: Wi‑Fi scan list.
Request:
```json
{}
```
Success:
```json
{"timestamp_ms":1700000000000,"networks":[{"ssid":"lab","bssid":"aa:bb:cc:dd:ee:ff","security":"wpa2","signal_dbm":-48,"channel":6,"frequency_mhz":2437,"known":true}]}
```
Errors:
```json
{"detail":"internal_error"}
```

GET /api/v1/network/bluetooth/state
Purpose: Bluetooth state.
Request:
```json
{}
```
Success:
```json
{"timestamp_ms":1700000000000,"enabled":false,"scanning":false,"paired_count":0,"connected_devices":[],"last_update_ms":1700000000000}
```
Errors:
```json
{"detail":"internal_error"}
```

GET /api/v1/network/bluetooth/devices
Purpose: Bluetooth device list.
Request:
```json
{}
```
Success:
```json
{"timestamp_ms":1700000000000,"devices":[{"addr":"00:11:22:33:44:55","name":"sensor","paired":true,"connected":false,"rssi_dbm":-40}]}
```
Errors:
```json
{"detail":"internal_error"}
```

GET /api/v1/audio
Purpose: audio state.
Request:
```json
{}
```
Success:
```json
{"timestamp_ms":1700000000000,"status":"ok","muted":false,"volume_percent":100}
```
Errors:
```json
{"detail":"internal_error"}
```

GET /api/v1/gps
Purpose: GPS state.
Request:
```json
{}
```
Success:
```json
{"timestamp_ms":1700000000000,"fix":"NO_FIX","satellites":{"in_view":0,"in_use":0},"latitude":null,"longitude":null,"last_update_ms":1700000000000,"source":"gpsd"}
```
Errors:
```json
{"detail":"internal_error"}
```

GET /api/v1/esp32
Purpose: ESP32 status.
Request:
```json
{}
```
Success:
```json
{"timestamp_ms":1700000000000,"connected":true,"last_seen_ms":1700000000000,"heartbeat":{"ok":true,"interval_ms":1000,"last_heartbeat_ms":1700000000000},"capabilities":{"leds":true,"vrx":true,"video_switch":true}}
```
Errors:
```json
{"detail":"internal_error"}
```

GET /api/v1/esp32/config
Purpose: ESP32 config.
Request:
```json
{}
```
Success:
```json
{"timestamp_ms":1700000000000,"config":{"vrx_default_id":1},"schema_version":"1"}
```
Errors:
```json
{"detail":"internal_error"}
```

GET /api/v1/antsdr
Purpose: AntSDR summary (aggregated).
Request:
```json
{}
```
Success:
```json
{"timestamp_ms":1700000000000,"connected":false,"last_error":"antsdr_unreachable"}
```
Errors:
```json
{"detail":"internal_error"}
```

GET /api/v1/antsdr/sweep/state
Purpose: AntSDR sweep state (aggregated).
Request:
```json
{}
```
Success:
```json
{"timestamp_ms":1700000000000,"running":false,"plans":[{"name":"default","start_hz":5700000000,"end_hz":5900000000,"step_hz":2000000}]}
```
Errors:
```json
{"detail":"internal_error"}
```

GET /api/v1/antsdr/gain
Purpose: AntSDR gain state (aggregated).
Request:
```json
{}
```
Success:
```json
{"timestamp_ms":1700000000000,"mode":"auto"}
```
Errors:
```json
{"detail":"internal_error"}
```

GET /api/v1/antsdr/stats
Purpose: AntSDR stats (aggregated).
Request:
```json
{}
```
Success:
```json
{"timestamp_ms":1700000000000,"frames_processed":10,"events_emitted":5}
```
Errors:
```json
{"detail":"internal_error"}
```

GET /api/v1/remote_id
Purpose: RemoteID summary (aggregated).
Request:
```json
{}
```
Success:
```json
{"timestamp_ms":1700000000000,"state":"degraded","mode":"live","capture_active":true,"last_error":"no_odid_frames"}
```
Errors:
```json
{"detail":"internal_error"}
```

GET /api/v1/remote_id/contacts
Purpose: RemoteID contacts (aggregated).
Request:
```json
{}
```
Success:
```json
{"timestamp_ms":1700000000000,"contacts":[{"id":"rid:123","type":"REMOTE_ID","source":"remoteid","last_seen_ts":1700000000000,"severity":"unknown","lat":23.0,"lon":72.0}]}
```
Errors:
```json
{"detail":"internal_error"}
```

GET /api/v1/remote_id/stats
Purpose: RemoteID stats (aggregated).
Request:
```json
{}
```
Success:
```json
{"timestamp_ms":1700000000000,"frames":10,"decoded":2,"dropped":0,"dedupe_hits":1}
```
Errors:
```json
{"detail":"internal_error"}
```

GET /api/v1/ws
Purpose: WS upgrade endpoint.
Request:
```json
{}
```
Success:
```json
{"detail":"upgrade_to_websocket"}
```
Errors:
```json
{"detail":"bad_request"}
```

### Backend Aggregator (Write)
POST /api/v1/vrx/tune
Purpose: tune VRX.
Request:
```json
{"payload":{"vrx_id":1,"freq_hz":5740000000},"confirm":false}
```
Success:
```json
{"command":"vrx/tune","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"invalid_state"}
```

POST /api/v1/scan/start
Purpose: start scan.
Request:
```json
{"payload":{},"confirm":false}
```
Success:
```json
{"command":"scan/start","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"rate_limited"}
```

POST /api/v1/scan/stop
Purpose: stop scan.
Request:
```json
{"payload":{},"confirm":false}
```
Success:
```json
{"command":"scan/stop","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"rate_limited"}
```

POST /api/v1/video/select
Purpose: select video input.
Request:
```json
{"payload":{"sel":1},"confirm":false}
```
Success:
```json
{"command":"video/select","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"invalid_state"}
```

POST /api/v1/audio/mute
Purpose: mute/unmute.
Request:
```json
{"payload":{"muted":true},"confirm":false}
```
Success:
```json
{"command":"audio/mute","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"invalid_state"}
```

POST /api/v1/audio/volume
Purpose: set volume.
Request:
```json
{"payload":{"volume_percent":50},"confirm":false}
```
Success:
```json
{"command":"audio/volume","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"invalid_state"}
```

POST /api/v1/network/wifi/enable
Purpose: enable Wi‑Fi.
Request:
```json
{"payload":{"enabled":true},"confirm":false}
```
Success:
```json
{"command":"network/wifi/enable","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"invalid_state"}
```

POST /api/v1/network/wifi/disable
Purpose: disable Wi‑Fi.
Request:
```json
{"payload":{},"confirm":false}
```
Success:
```json
{"command":"network/wifi/disable","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"invalid_state"}
```

POST /api/v1/network/wifi/connect
Purpose: connect Wi‑Fi.
Request:
```json
{"payload":{"ssid":"lab","password":"secret"},"confirm":false}
```
Success:
```json
{"command":"network/wifi/connect","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"invalid_state"}
```

POST /api/v1/network/wifi/disconnect
Purpose: disconnect Wi‑Fi.
Request:
```json
{"payload":{},"confirm":false}
```
Success:
```json
{"command":"network/wifi/disconnect","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"invalid_state"}
```

POST /api/v1/network/bluetooth/enable
Purpose: enable Bluetooth.
Request:
```json
{"payload":{"enabled":true},"confirm":false}
```
Success:
```json
{"command":"network/bluetooth/enable","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"invalid_state"}
```

POST /api/v1/network/bluetooth/disable
Purpose: disable Bluetooth.
Request:
```json
{"payload":{},"confirm":false}
```
Success:
```json
{"command":"network/bluetooth/disable","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"invalid_state"}
```

POST /api/v1/network/bluetooth/scan/start
Purpose: start BT scan.
Request:
```json
{"payload":{},"confirm":false}
```
Success:
```json
{"command":"network/bluetooth/scan/start","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"invalid_state"}
```

POST /api/v1/network/bluetooth/scan/stop
Purpose: stop BT scan.
Request:
```json
{"payload":{},"confirm":false}
```
Success:
```json
{"command":"network/bluetooth/scan/stop","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"invalid_state"}
```

POST /api/v1/network/bluetooth/pair
Purpose: pair device.
Request:
```json
{"payload":{"addr":"00:11:22:33:44:55","pin":"0000"},"confirm":false}
```
Success:
```json
{"command":"network/bluetooth/pair","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"invalid_state"}
```

POST /api/v1/network/bluetooth/unpair
Purpose: unpair device.
Request:
```json
{"payload":{"addr":"00:11:22:33:44:55"},"confirm":false}
```
Success:
```json
{"command":"network/bluetooth/unpair","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"invalid_state"}
```

POST /api/v1/gps/restart
Purpose: restart GPS (confirm required).
Request:
```json
{"payload":{},"confirm":true}
```
Success:
```json
{"command":"gps/restart","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"confirm_required"}
```

POST /api/v1/esp32/buzzer
Purpose: buzzer control.
Request:
```json
{"payload":{"mode":"beep","duration_ms":250},"confirm":false}
```
Success:
```json
{"command":"esp32/buzzer","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"invalid_state"}
```

POST /api/v1/esp32/leds
Purpose: LED control.
Request:
```json
{"payload":{"red":true,"yellow":false,"green":false},"confirm":false}
```
Success:
```json
{"command":"esp32/leds","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"invalid_state"}
```

POST /api/v1/esp32/buttons/simulate
Purpose: simulate button (local-only).
Request:
```json
{"payload":{"button":"mute","action":"press"},"confirm":false}
```
Success:
```json
{"command":"esp32/buttons/simulate","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"local_only"}
```

POST /api/v1/esp32/config
Purpose: write ESP32 config.
Request:
```json
{"payload":{"config":{"vrx_default_id":1}},"confirm":false}
```
Success:
```json
{"command":"esp32/config","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"invalid_state"}
```

POST /api/v1/antsdr/sweep/start
Purpose: start AntSDR sweep.
Request:
```json
{"payload":{"plan":"default"},"confirm":false}
```
Success:
```json
{"command":"antsdr/sweep/start","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"invalid_state"}
```

POST /api/v1/antsdr/sweep/stop
Purpose: stop AntSDR sweep.
Request:
```json
{"payload":{},"confirm":false}
```
Success:
```json
{"command":"antsdr/sweep/stop","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"invalid_state"}
```

POST /api/v1/antsdr/gain/set
Purpose: set AntSDR gain.
Request:
```json
{"payload":{"mode":"auto"},"confirm":false}
```
Success:
```json
{"command":"antsdr/gain/set","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"invalid_state"}
```

POST /api/v1/antsdr/device/reset
Purpose: reset AntSDR device (dangerous).
Request:
```json
{"payload":{},"confirm":true}
```
Success:
```json
{"command":"antsdr/device/reset","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"confirm_required"}
```

POST /api/v1/remote_id/monitor/start
Purpose: start RemoteID monitor.
Request:
```json
{"payload":{},"confirm":false}
```
Success:
```json
{"command":"remote_id/monitor/start","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"invalid_state"}
```

POST /api/v1/remote_id/monitor/stop
Purpose: stop RemoteID monitor.
Request:
```json
{"payload":{},"confirm":false}
```
Success:
```json
{"command":"remote_id/monitor/stop","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"invalid_state"}
```

POST /api/v1/system/reboot
Purpose: reboot system (dangerous).
Request:
```json
{"payload":{},"confirm":true}
```
Success:
```json
{"command":"system/reboot","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"confirm_required"}
```

POST /api/v1/system/shutdown
Purpose: shutdown system (dangerous).
Request:
```json
{"payload":{},"confirm":true}
```
Success:
```json
{"command":"system/shutdown","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"confirm_required"}
```

### System Controller (Read)
GET /api/v1/system-controller/health
Purpose: health check.
Request:
```json
{}
```
Success:
```json
{"status":"ok","timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"internal_error"}
```

GET /api/v1/system-controller/status
Purpose: system-controller snapshot.
Request:
```json
{}
```
Success:
```json
{"timestamp_ms":1700000000000,"system":{"status":"ok"},"ups":{"status":"ok"},"services":[],"network":{},"audio":{}}
```
Errors:
```json
{"detail":"internal_error"}
```

GET /api/v1/system-controller/system
Purpose: system stats.
Request:
```json
{}
```
Success:
```json
{"timestamp_ms":1700000000000,"status":"ok","uptime_s":4671}
```
Errors:
```json
{"detail":"internal_error"}
```

GET /api/v1/system-controller/ups
Purpose: UPS snapshot.
Request:
```json
{}
```
Success:
```json
{"timestamp_ms":1700000000000,"status":"ok","soc_percent":98}
```
Errors:
```json
{"detail":"internal_error"}
```

GET /api/v1/system-controller/services
Purpose: service list.
Request:
```json
{}
```
Success:
```json
[{"name":"gpsd","active_state":"active","sub_state":"running","restart_count":0}]
```
Errors:
```json
{"detail":"internal_error"}
```

GET /api/v1/system-controller/network
Purpose: network summary.
Request:
```json
{}
```
Success:
```json
{"wifi":{"timestamp_ms":1700000000000,"enabled":true,"connected":true,"ssid":"lab"},"bluetooth":{"timestamp_ms":1700000000000,"enabled":false,"scanning":false,"paired_count":0,"connected_devices":[]}}
```
Errors:
```json
{"detail":"internal_error"}
```

GET /api/v1/system-controller/network/wifi/state
Purpose: Wi‑Fi state.
Request:
```json
{}
```
Success:
```json
{"timestamp_ms":1700000000000,"enabled":true,"connected":true,"ssid":"lab","ip":"192.168.1.35","last_update_ms":1700000000000}
```
Errors:
```json
{"detail":"internal_error"}
```

GET /api/v1/system-controller/network/wifi/scan
Purpose: Wi‑Fi scan list.
Request:
```json
{}
```
Success:
```json
{"timestamp_ms":1700000000000,"networks":[{"ssid":"lab","bssid":"aa:bb:cc:dd:ee:ff","security":"wpa2","signal_dbm":-48,"channel":6,"frequency_mhz":2437,"known":true}]}
```
Errors:
```json
{"detail":"internal_error"}
```

GET /api/v1/system-controller/network/bluetooth/state
Purpose: Bluetooth state.
Request:
```json
{}
```
Success:
```json
{"timestamp_ms":1700000000000,"enabled":false,"scanning":false,"paired_count":0,"connected_devices":[],"last_update_ms":1700000000000}
```
Errors:
```json
{"detail":"internal_error"}
```

GET /api/v1/system-controller/network/bluetooth/devices
Purpose: Bluetooth devices.
Request:
```json
{}
```
Success:
```json
{"timestamp_ms":1700000000000,"devices":[{"addr":"00:11:22:33:44:55","name":"sensor","paired":true,"connected":false,"rssi_dbm":-40}]}
```
Errors:
```json
{"detail":"internal_error"}
```

GET /api/v1/system-controller/gps
Purpose: GPS state.
Request:
```json
{}
```
Success:
```json
{"timestamp_ms":1700000000000,"fix":"NO_FIX","satellites":{"in_view":0,"in_use":0},"latitude":null,"longitude":null,"last_update_ms":1700000000000,"source":"gpsd"}
```
Errors:
```json
{"detail":"internal_error"}
```

GET /api/v1/system-controller/audio
Purpose: audio state.
Request:
```json
{}
```
Success:
```json
{"timestamp_ms":1700000000000,"status":"ok","muted":false,"volume_percent":100}
```
Errors:
```json
{"detail":"internal_error"}
```

GET /api/v1/system-controller/ws
Purpose: WS upgrade for system controller.
Request:
```json
{}
```
Success:
```json
{"detail":"upgrade_to_websocket"}
```
Errors:
```json
{"detail":"bad_request"}
```

### System Controller (Write)
POST /api/v1/system-controller/services/{name}/restart
Purpose: restart service (dangerous).
Request:
```json
{"payload":{},"confirm":true}
```
Success:
```json
{"command":"services/restart","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"confirm_required"}
```

POST /api/v1/system-controller/network/wifi/enable
Purpose: enable Wi‑Fi.
Request:
```json
{"payload":{"enabled":true},"confirm":false}
```
Success:
```json
{"command":"network/wifi/enable","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"invalid_state"}
```

POST /api/v1/system-controller/network/wifi/disable
Purpose: disable Wi‑Fi.
Request:
```json
{"payload":{},"confirm":false}
```
Success:
```json
{"command":"network/wifi/disable","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"invalid_state"}
```

POST /api/v1/system-controller/network/wifi/connect
Purpose: connect Wi‑Fi.
Request:
```json
{"payload":{"ssid":"lab","password":"secret"},"confirm":false}
```
Success:
```json
{"command":"network/wifi/connect","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"invalid_state"}
```

POST /api/v1/system-controller/network/wifi/disconnect
Purpose: disconnect Wi‑Fi.
Request:
```json
{"payload":{},"confirm":false}
```
Success:
```json
{"command":"network/wifi/disconnect","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"invalid_state"}
```

POST /api/v1/system-controller/network/bluetooth/enable
Purpose: enable Bluetooth.
Request:
```json
{"payload":{"enabled":true},"confirm":false}
```
Success:
```json
{"command":"network/bluetooth/enable","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"invalid_state"}
```

POST /api/v1/system-controller/network/bluetooth/disable
Purpose: disable Bluetooth.
Request:
```json
{"payload":{},"confirm":false}
```
Success:
```json
{"command":"network/bluetooth/disable","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"invalid_state"}
```

POST /api/v1/system-controller/network/bluetooth/scan/start
Purpose: start BT scan.
Request:
```json
{"payload":{},"confirm":false}
```
Success:
```json
{"command":"network/bluetooth/scan/start","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"invalid_state"}
```

POST /api/v1/system-controller/network/bluetooth/scan/stop
Purpose: stop BT scan.
Request:
```json
{"payload":{},"confirm":false}
```
Success:
```json
{"command":"network/bluetooth/scan/stop","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"invalid_state"}
```

POST /api/v1/system-controller/network/bluetooth/pair
Purpose: pair device.
Request:
```json
{"payload":{"addr":"00:11:22:33:44:55","pin":"0000"},"confirm":false}
```
Success:
```json
{"command":"network/bluetooth/pair","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"invalid_state"}
```

POST /api/v1/system-controller/network/bluetooth/unpair
Purpose: unpair device.
Request:
```json
{"payload":{"addr":"00:11:22:33:44:55"},"confirm":false}
```
Success:
```json
{"command":"network/bluetooth/unpair","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"invalid_state"}
```

POST /api/v1/system-controller/gps/restart
Purpose: restart GPS (confirm required).
Request:
```json
{"payload":{},"confirm":true}
```
Success:
```json
{"command":"gps/restart","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"confirm_required"}
```

POST /api/v1/system-controller/audio/mute
Purpose: mute/unmute.
Request:
```json
{"payload":{"muted":true},"confirm":false}
```
Success:
```json
{"command":"audio/mute","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"invalid_state"}
```

POST /api/v1/system-controller/audio/volume
Purpose: set volume.
Request:
```json
{"payload":{"volume_percent":50},"confirm":false}
```
Success:
```json
{"command":"audio/volume","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"invalid_state"}
```

POST /api/v1/system-controller/system/reboot
Purpose: reboot system (dangerous).
Request:
```json
{"payload":{},"confirm":true}
```
Success:
```json
{"command":"system/reboot","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"confirm_required"}
```

POST /api/v1/system-controller/system/shutdown
Purpose: shutdown system (dangerous).
Request:
```json
{"payload":{},"confirm":true}
```
Success:
```json
{"command":"system/shutdown","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"confirm_required"}
```

### AntSDR Scan (Read)
GET /api/v1/antsdr-scan/health
Purpose: RFScan health.
Request:
```json
{}
```
Success:
```json
{"status":"ok","timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"internal_error"}
```

GET /api/v1/antsdr-scan/version
Purpose: RFScan version.
Request:
```json
{}
```
Success:
```json
{"version":"dev","timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"internal_error"}
```

GET /api/v1/antsdr-scan/stats
Purpose: RFScan stats.
Request:
```json
{}
```
Success:
```json
{"timestamp_ms":1700000000000,"frames_processed":10,"events_emitted":5}
```
Errors:
```json
{"detail":"internal_error"}
```

GET /api/v1/antsdr-scan/device
Purpose: RF device status.
Request:
```json
{}
```
Success:
```json
{"timestamp_ms":1700000000000,"connected":false,"last_error":"device_not_connected"}
```
Errors:
```json
{"detail":"internal_error"}
```

GET /api/v1/antsdr-scan/sweep/state
Purpose: sweep state.
Request:
```json
{}
```
Success:
```json
{"timestamp_ms":1700000000000,"running":false,"plans":[{"name":"default","start_hz":5700000000,"end_hz":5900000000,"step_hz":2000000}]}
```
Errors:
```json
{"detail":"internal_error"}
```

GET /api/v1/antsdr-scan/gain
Purpose: gain state.
Request:
```json
{}
```
Success:
```json
{"timestamp_ms":1700000000000,"mode":"auto"}
```
Errors:
```json
{"detail":"internal_error"}
```

GET /api/v1/antsdr-scan/config
Purpose: scan config.
Request:
```json
{}
```
Success:
```json
{"timestamp_ms":1700000000000,"output_jsonl":"/opt/ndefender/logs/antsdr_scan.jsonl"}
```
Errors:
```json
{"detail":"internal_error"}
```

GET /api/v1/antsdr-scan/events/last
Purpose: last RF events.
Request:
```json
{}
```
Success:
```json
{"timestamp_ms":1700000000000,"events":[{"type":"RF_CONTACT_NEW","timestamp_ms":1700000000000,"source":"antsdr","data":{"id":"rf:1","freq_hz":5740000000,"rssi_dbm":-48}}]}
```
Errors:
```json
{"detail":"internal_error"}
```

### AntSDR Scan (Write)
POST /api/v1/antsdr-scan/config/reload
Purpose: reload config.
Request:
```json
{"payload":{},"confirm":false}
```
Success:
```json
{"command":"config/reload","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"invalid_state"}
```

POST /api/v1/antsdr-scan/sweep/start
Purpose: start sweep.
Request:
```json
{"payload":{"plan":"default"},"confirm":false}
```
Success:
```json
{"command":"sweep/start","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"invalid_state"}
```

POST /api/v1/antsdr-scan/sweep/stop
Purpose: stop sweep.
Request:
```json
{"payload":{},"confirm":false}
```
Success:
```json
{"command":"sweep/stop","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"invalid_state"}
```

POST /api/v1/antsdr-scan/gain/set
Purpose: set gain.
Request:
```json
{"payload":{"mode":"auto"},"confirm":false}
```
Success:
```json
{"command":"gain/set","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"invalid_state"}
```

POST /api/v1/antsdr-scan/device/reset
Purpose: reset device (dangerous).
Request:
```json
{"payload":{},"confirm":true}
```
Success:
```json
{"command":"device/reset","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"confirm_required"}
```

POST /api/v1/antsdr-scan/device/calibrate
Purpose: calibrate device (dangerous).
Request:
```json
{"payload":{"kind":"rf_dc"},"confirm":true}
```
Success:
```json
{"command":"device/calibrate","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"confirm_required"}
```

### RemoteID Engine (Read)
GET /api/v1/remoteid-engine/health
Purpose: RemoteID health.
Request:
```json
{}
```
Success:
```json
{"status":"ok","timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"internal_error"}
```

GET /api/v1/remoteid-engine/status
Purpose: RemoteID status.
Request:
```json
{}
```
Success:
```json
{"timestamp_ms":1700000000000,"state":"degraded","mode":"live","capture_active":true,"last_error":"no_odid_frames"}
```
Errors:
```json
{"detail":"internal_error"}
```

GET /api/v1/remoteid-engine/contacts
Purpose: RemoteID contacts.
Request:
```json
{}
```
Success:
```json
{"timestamp_ms":1700000000000,"contacts":[{"id":"rid:123","type":"REMOTE_ID","source":"remoteid","last_seen_ts":1700000000000,"severity":"unknown","lat":23.0,"lon":72.0}]}
```
Errors:
```json
{"detail":"internal_error"}
```

GET /api/v1/remoteid-engine/stats
Purpose: RemoteID stats.
Request:
```json
{}
```
Success:
```json
{"timestamp_ms":1700000000000,"frames":10,"decoded":2,"dropped":0,"dedupe_hits":1}
```
Errors:
```json
{"detail":"internal_error"}
```

GET /api/v1/remoteid-engine/replay/state
Purpose: replay state.
Request:
```json
{}
```
Success:
```json
{"timestamp_ms":1700000000000,"active":false,"source":"none"}
```
Errors:
```json
{"detail":"internal_error"}
```

### RemoteID Engine (Write)
POST /api/v1/remoteid-engine/monitor/start
Purpose: start monitor.
Request:
```json
{"payload":{},"confirm":false}
```
Success:
```json
{"command":"monitor/start","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"invalid_state"}
```

POST /api/v1/remoteid-engine/monitor/stop
Purpose: stop monitor.
Request:
```json
{"payload":{},"confirm":false}
```
Success:
```json
{"command":"monitor/stop","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"invalid_state"}
```

POST /api/v1/remoteid-engine/replay/start
Purpose: start replay.
Request:
```json
{"payload":{"source":"file.jsonl"},"confirm":false}
```
Success:
```json
{"command":"replay/start","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"invalid_state"}
```

POST /api/v1/remoteid-engine/replay/stop
Purpose: stop replay.
Request:
```json
{"payload":{},"confirm":false}
```
Success:
```json
{"command":"replay/stop","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"invalid_state"}
```

### Observability (Read)
GET /api/v1/observability/health
Purpose: observability health.
Request:
```json
{}
```
Success:
```json
{"status":"ok","timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"internal_error"}
```

GET /api/v1/observability/health/detail
Purpose: health details.
Request:
```json
{}
```
Success:
```json
{"timestamp_ms":1700000000000,"checks":[]}
```
Errors:
```json
{"detail":"internal_error"}
```

GET /api/v1/observability/status
Purpose: observability status.
Request:
```json
{}
```
Success:
```json
{"timestamp_ms":1700000000000,"ok":true}
```
Errors:
```json
{"detail":"internal_error"}
```

GET /api/v1/observability/version
Purpose: version.
Request:
```json
{}
```
Success:
```json
{"timestamp_ms":1700000000000,"version":"dev"}
```
Errors:
```json
{"detail":"internal_error"}
```

GET /api/v1/observability/config
Purpose: config.
Request:
```json
{}
```
Success:
```json
{"timestamp_ms":1700000000000,"profile":"default"}
```
Errors:
```json
{"detail":"internal_error"}
```

### Observability (Write)
POST /api/v1/observability/diag/bundle
Purpose: create diagnostics bundle.
Request:
```json
{"payload":{},"confirm":false}
```
Success:
```json
{"command":"diag/bundle","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
Errors:
```json
{"detail":"invalid_state"}
```

## Integration Guide for UI (Figma → UI)
- Always render the `/status` snapshot first, then merge WS updates.
- Display units exactly: `freq_hz`, `rssi_dbm`, `timestamp_ms`, `latitude`, `longitude`.
- Show explicit offline/degraded reasons using `status` and `last_error`.
- Use reconnect rules: on WS drop, re-fetch `/status`, then reconnect WS.
- Stale indicators: compare `timestamp_ms` and subsystem `last_update_ms` to wall time.
- Threat sorting rules: not implemented in contract; UI should preserve API order.

## Integration Guide for AI Tools
- Use `GET /status` as the primary state snapshot.
- Use WS `/api/v1/ws` for live updates and correlation of command results.
- Do not send dangerous commands unless explicitly allowed by the operator.
- Respect confirm‑gating and rate limits; treat `{"detail":"confirm_required"}` as a hard stop without explicit confirmation.

## Firmware Integration (ESP32 Panel)
- ESP32 telemetry must align with the WS envelope when proxied.
- ACK correlation must use `data.id == command_id` for ESP32 commands.
- Firmware should include uptime telemetry for latency and health checks.

## Data Model / Contracts
- TypeScript: `packages/contracts-ts/` (alias to `types/`)
- JSON Schema: `packages/contracts-schema/` (alias to `schemas/`)
- OpenAPI: `packages/openapi/` (alias to `docs/OPENAPI.yaml`)

## Legacy Paths
- `/status` and `/ws` are legacy aliases. Canonical paths are `/api/v1/status` and `/api/v1/ws`.

## Tooling
- List endpoints from OpenAPI and README:
```bash
scripts/docs_endpoints.sh
```

## Security
- Do not expose legacy Flask on `:8000`.
- Do not commit tokens or credentialed URLs.
