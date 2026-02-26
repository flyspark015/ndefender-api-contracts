# N-Defender API Contracts (Single Source of Truth)

This repository is the **canonical contract** for all N-Defender REST + WebSocket APIs (TX/RX), covering:
- Backend Aggregator (public API)
- System Controller (local system controls)
- AntSDR Scan
- RemoteID Engine
- Observability

Canonical contract:
- `docs/ALL_IN_ONE_API.md`

## Architecture (Ports + Services)
```
                    Public Internet
                          |
                          |  https://n.flyspark.in/api/v1
                          v
                  +--------------------+
                  |  Backend Aggregator |
                  |  FastAPI :8001      |
                  +--------------------+
                    |        |       |
                    |        |       |
     +--------------+   +----+----+  +-----------------+
     | System Ctrl  |   | RFScan |  | RemoteID Engine |
     | FastAPI :8002|   | :8890 |  | (local /api/v1)  |
     +--------------+   +--------+  +-----------------+

NOTE: Legacy Flask on :8000 must be OFF (no exposure).
```

Service map:
- Aggregator: `http://127.0.0.1:8001/api/v1` (public: `https://n.flyspark.in/api/v1`)
- System Controller: `http://127.0.0.1:8002/api/v1`
- AntSDR Scan: `http://127.0.0.1:8890/api/v1`
- RemoteID Engine: `http://127.0.0.1:<port>/api/v1` (service-local)

## Contract Rules (Non‑Negotiable)
- `timestamp_ms` only (epoch milliseconds) everywhere.
- GPS uses `latitude` / `longitude` (no `lat`/`lng`).
- Frequencies use `freq_hz` (Hz).
- Signal is `*_dbm` (dBm).
- WS envelope is `{type,timestamp_ms,source,data}`.
- Errors for FastAPI: `{"detail":"..."}`.
- Commands: body is `{"payload":{...},"confirm":false}`.
- Dangerous commands require `confirm=true`.
- Rate limits: 10/min commands, 2/min dangerous.

## Entry Points
- Canonical contract: `docs/ALL_IN_ONE_API.md`
- WebSocket catalog: `docs/WEBSOCKET_EVENTS.md`
- OpenAPI: `docs/OPENAPI.yaml`
- Models: `docs/MODELS/`
- Endpoints: `docs/ENDPOINTS/`
- Schemas: `schemas/`
- Types: `types/`
- Docs index: `docs/INDEX.md`

## RX Flows (Status / Telemetry / Contacts)
1) Call `GET /status` (REST snapshot).
2) Connect WS `/api/v1/ws`.
3) Merge incremental WS updates (`SYSTEM_UPDATE`, `CONTACT_*`, `TELEMETRY_UPDATE`).
4) Reconnect on WS drop and re‑fetch `/status`.

## TX Flows (Commands)
1) Send command via REST with `{payload, confirm}`.
2) REST returns `CommandResult` with `command_id`.
3) WS emits `COMMAND_ACK` with matching correlation key.

## Error Model (FastAPI)
```json
{"detail":"<reason>"}
```

## Examples (Every Endpoint)
Base URLs used below:
- `BASE=http://127.0.0.1:8001/api/v1` (Aggregator)
- `SC=http://127.0.0.1:8002/api/v1` (System Controller)
- `RF=http://127.0.0.1:8890/api/v1` (AntSDR Scan)

### Backend Aggregator (REST)

#### `GET /health`
```bash
curl -sS $BASE/health
```
```json
{"status":"ok","timestamp_ms":1700000000000}
```

#### `GET /status`
```bash
curl -sS $BASE/status
```
```json
{"timestamp_ms":1700000000000,"overall_ok":false,"system":{"status":"degraded","uptime_s":1},"power":{"status":"ok","soc_percent":98},"rf":{"status":"offline","last_error":"antsdr_unreachable"},"remote_id":{"state":"degraded","mode":"live","capture_active":true},"vrx":{"selected":1,"scan_state":"idle","sys":{"status":"CONNECTED"},"vrx":[{"id":1,"freq_hz":5740000000,"rssi_raw":632}]},"fpv":{"selected":1,"scan_state":"idle","freq_hz":5740000000,"rssi_raw":632},"video":{"selected":1,"status":"ok"},"services":[{"name":"ndefender-backend","active_state":"active","sub_state":"running","restart_count":0}],"network":{"wifi":{"timestamp_ms":1700000000000,"enabled":true,"connected":true,"ssid":"lab","ip":"192.168.1.35"},"bluetooth":{"timestamp_ms":1700000000000,"enabled":false,"scanning":false,"paired_count":0,"connected_devices":[]}},"gps":{"timestamp_ms":1700000000000,"fix":"NO_FIX","satellites":{"in_view":0,"in_use":0},"last_update_ms":1700000000000,"source":"gpsd"},"esp32":{"timestamp_ms":1700000000000,"connected":true,"last_seen_ms":1700000000000},"antsdr":{"timestamp_ms":1700000000000,"connected":false,"last_error":"antsdr_unreachable"},"audio":{"timestamp_ms":1700000000000,"status":"ok","muted":false,"volume_percent":100},"contacts":[],"replay":{"active":false,"source":"none"}}
```

#### `GET /contacts`
```bash
curl -sS $BASE/contacts
```
```json
{"contacts":[{"id":"fpv:1","type":"FPV","source":"esp32","last_seen_ts":1700000000000,"severity":"unknown","vrx_id":1,"freq_hz":5740000000,"rssi_raw":632,"selected":1}]}
```

#### `GET /system`
```bash
curl -sS $BASE/system
```
```json
{"timestamp_ms":1700000000000,"status":"ok","uptime_s":4671,"version":{"app":"ndefender-backend-aggregator","git_sha":"dev","build_ts":1700000000000}}
```

#### `GET /power`
```bash
curl -sS $BASE/power
```
```json
{"timestamp_ms":1700000000000,"status":"ok","pack_voltage_v":16.6,"current_a":-0.01,"soc_percent":98}
```

#### `GET /rf`
```bash
curl -sS $BASE/rf
```
```json
{"status":"offline","scan_active":false,"last_error":"antsdr_unreachable","last_event_type":"RF_SCAN_OFFLINE","last_timestamp_ms":1700000000000}
```

#### `GET /video`
```bash
curl -sS $BASE/video
```
```json
{"selected":1,"status":"ok"}
```

#### `GET /services`
```bash
curl -sS $BASE/services
```
```json
[{"name":"ndefender-backend","active_state":"active","sub_state":"running","restart_count":0}]
```

#### `GET /network` (summary)
```bash
curl -sS $BASE/network
```
```json
{"wifi":{"timestamp_ms":1700000000000,"enabled":true,"connected":true,"ssid":"lab","ip":"192.168.1.35"},"bluetooth":{"timestamp_ms":1700000000000,"enabled":false,"scanning":false,"paired_count":0,"connected_devices":[]}}
```

#### `GET /network/wifi/state`
```bash
curl -sS $BASE/network/wifi/state
```
```json
{"timestamp_ms":1700000000000,"enabled":true,"connected":true,"ssid":"lab","ip":"192.168.1.35","last_update_ms":1700000000000}
```

#### `GET /network/wifi/scan`
```bash
curl -sS $BASE/network/wifi/scan
```
```json
{"timestamp_ms":1700000000000,"networks":[{"ssid":"lab","bssid":"aa:bb:cc:dd:ee:ff","security":"wpa2","signal_dbm":-48,"channel":6,"frequency_mhz":2437,"known":true}]}
```

#### `GET /network/bluetooth/state`
```bash
curl -sS $BASE/network/bluetooth/state
```
```json
{"timestamp_ms":1700000000000,"enabled":false,"scanning":false,"paired_count":0,"connected_devices":[],"last_update_ms":1700000000000}
```

#### `GET /network/bluetooth/devices`
```bash
curl -sS $BASE/network/bluetooth/devices
```
```json
{"timestamp_ms":1700000000000,"devices":[{"addr":"00:11:22:33:44:55","name":"sensor","paired":true,"connected":false,"rssi_dbm":-40}]}
```

#### `GET /audio`
```bash
curl -sS $BASE/audio
```
```json
{"timestamp_ms":1700000000000,"status":"ok","muted":false,"volume_percent":100}
```

#### `GET /gps`
```bash
curl -sS $BASE/gps
```
```json
{"timestamp_ms":1700000000000,"fix":"NO_FIX","satellites":{"in_view":0,"in_use":0},"last_update_ms":1700000000000,"source":"gpsd"}
```

#### `GET /esp32`
```bash
curl -sS $BASE/esp32
```
```json
{"timestamp_ms":1700000000000,"connected":true,"last_seen_ms":1700000000000,"heartbeat":{"ok":true,"interval_ms":1000,"last_heartbeat_ms":1700000000000},"capabilities":{"leds":true,"vrx":true,"video_switch":true}}
```

#### `GET /esp32/config`
```bash
curl -sS $BASE/esp32/config
```
```json
{"timestamp_ms":1700000000000,"config":{"vrx_default_id":1},"schema_version":"1"}
```

#### `GET /antsdr`
```bash
curl -sS $BASE/antsdr
```
```json
{"timestamp_ms":1700000000000,"connected":false,"last_error":"antsdr_unreachable"}
```

#### `GET /antsdr/sweep/state`
```bash
curl -sS $BASE/antsdr/sweep/state
```
```json
{"timestamp_ms":1700000000000,"running":false,"plans":[{"name":"default","start_hz":5700000000,"end_hz":5900000000,"step_hz":2000000}]}
```

#### `GET /antsdr/gain`
```bash
curl -sS $BASE/antsdr/gain
```
```json
{"timestamp_ms":1700000000000,"mode":"auto"}
```

#### `GET /antsdr/stats`
```bash
curl -sS $BASE/antsdr/stats
```
```json
{"timestamp_ms":1700000000000,"frames_processed":10,"events_emitted":5}
```

#### `GET /remote_id`
```bash
curl -sS $BASE/remote_id
```
```json
{"timestamp_ms":1700000000000,"state":"degraded","mode":"live","capture_active":true,"last_error":"no_odid_frames"}
```

#### `GET /remote_id/contacts`
```bash
curl -sS $BASE/remote_id/contacts
```
```json
{"timestamp_ms":1700000000000,"contacts":[{"id":"rid:123","type":"REMOTE_ID","source":"remoteid","last_seen_ts":1700000000000,"severity":"unknown","lat":23.0,"lon":72.0}]}
```

#### `GET /remote_id/stats`
```bash
curl -sS $BASE/remote_id/stats
```
```json
{"timestamp_ms":1700000000000,"frames":10,"decoded":2,"dropped":0,"dedupe_hits":1}
```

### Backend Aggregator (Commands)
All commands accept:
```json
{"payload":{},"confirm":false}
```
All responses are `CommandResult`:
```json
{"command":"vrx/tune","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /vrx/tune`
```bash
curl -sS -X POST $BASE/vrx/tune -H 'Content-Type: application/json' -d '{"payload":{"vrx_id":1,"freq_hz":5740000000},"confirm":false}'
```
```json
{"command":"vrx/tune","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /scan/start`
```bash
curl -sS -X POST $BASE/scan/start -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```
```json
{"command":"scan/start","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /scan/stop`
```bash
curl -sS -X POST $BASE/scan/stop -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```
```json
{"command":"scan/stop","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /video/select`
```bash
curl -sS -X POST $BASE/video/select -H 'Content-Type: application/json' -d '{"payload":{"sel":1},"confirm":false}'
```
```json
{"command":"video/select","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /audio/mute`
```bash
curl -sS -X POST $BASE/audio/mute -H 'Content-Type: application/json' -d '{"payload":{"muted":true},"confirm":false}'
```
```json
{"command":"audio/mute","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /audio/volume`
```bash
curl -sS -X POST $BASE/audio/volume -H 'Content-Type: application/json' -d '{"payload":{"volume_percent":50},"confirm":false}'
```
```json
{"command":"audio/volume","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /network/wifi/enable`
```bash
curl -sS -X POST $BASE/network/wifi/enable -H 'Content-Type: application/json' -d '{"payload":{"enabled":true},"confirm":false}'
```
```json
{"command":"network/wifi/enable","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /network/wifi/disable`
```bash
curl -sS -X POST $BASE/network/wifi/disable -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```
```json
{"command":"network/wifi/disable","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /network/wifi/connect`
```bash
curl -sS -X POST $BASE/network/wifi/connect -H 'Content-Type: application/json' -d '{"payload":{"ssid":"lab","password":"secret"},"confirm":false}'
```
```json
{"command":"network/wifi/connect","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /network/wifi/disconnect`
```bash
curl -sS -X POST $BASE/network/wifi/disconnect -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```
```json
{"command":"network/wifi/disconnect","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /network/bluetooth/enable`
```bash
curl -sS -X POST $BASE/network/bluetooth/enable -H 'Content-Type: application/json' -d '{"payload":{"enabled":true},"confirm":false}'
```
```json
{"command":"network/bluetooth/enable","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /network/bluetooth/disable`
```bash
curl -sS -X POST $BASE/network/bluetooth/disable -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```
```json
{"command":"network/bluetooth/disable","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /network/bluetooth/scan/start`
```bash
curl -sS -X POST $BASE/network/bluetooth/scan/start -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```
```json
{"command":"network/bluetooth/scan/start","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /network/bluetooth/scan/stop`
```bash
curl -sS -X POST $BASE/network/bluetooth/scan/stop -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```
```json
{"command":"network/bluetooth/scan/stop","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /network/bluetooth/pair`
```bash
curl -sS -X POST $BASE/network/bluetooth/pair -H 'Content-Type: application/json' -d '{"payload":{"addr":"00:11:22:33:44:55","pin":"0000"},"confirm":false}'
```
```json
{"command":"network/bluetooth/pair","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /network/bluetooth/unpair`
```bash
curl -sS -X POST $BASE/network/bluetooth/unpair -H 'Content-Type: application/json' -d '{"payload":{"addr":"00:11:22:33:44:55"},"confirm":false}'
```
```json
{"command":"network/bluetooth/unpair","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /gps/restart`
```bash
curl -sS -X POST $BASE/gps/restart -H 'Content-Type: application/json' -d '{"payload":{},"confirm":true}'
```
```json
{"command":"gps/restart","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /esp32/buzzer`
```bash
curl -sS -X POST $BASE/esp32/buzzer -H 'Content-Type: application/json' -d '{"payload":{"mode":"beep","duration_ms":250},"confirm":false}'
```
```json
{"command":"esp32/buzzer","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /esp32/leds`
```bash
curl -sS -X POST $BASE/esp32/leds -H 'Content-Type: application/json' -d '{"payload":{"red":true,"green":false,"yellow":false},"confirm":false}'
```
```json
{"command":"esp32/leds","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /esp32/buttons/simulate`
```bash
curl -sS -X POST $BASE/esp32/buttons/simulate -H 'Content-Type: application/json' -d '{"payload":{"button":"mute","action":"press"},"confirm":false}'
```
```json
{"command":"esp32/buttons/simulate","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /esp32/config`
```bash
curl -sS -X POST $BASE/esp32/config -H 'Content-Type: application/json' -d '{"payload":{"config":{"vrx_default_id":1}},"confirm":false}'
```
```json
{"command":"esp32/config","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /antsdr/sweep/start`
```bash
curl -sS -X POST $BASE/antsdr/sweep/start -H 'Content-Type: application/json' -d '{"payload":{"plan":"default"},"confirm":false}'
```
```json
{"command":"antsdr/sweep/start","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /antsdr/sweep/stop`
```bash
curl -sS -X POST $BASE/antsdr/sweep/stop -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```
```json
{"command":"antsdr/sweep/stop","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /antsdr/gain/set`
```bash
curl -sS -X POST $BASE/antsdr/gain/set -H 'Content-Type: application/json' -d '{"payload":{"mode":"auto"},"confirm":false}'
```
```json
{"command":"antsdr/gain/set","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /antsdr/device/reset` (dangerous)
```bash
curl -sS -X POST $BASE/antsdr/device/reset -H 'Content-Type: application/json' -d '{"payload":{},"confirm":true}'
```
```json
{"command":"antsdr/device/reset","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /remote_id/monitor/start`
```bash
curl -sS -X POST $BASE/remote_id/monitor/start -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```
```json
{"command":"remote_id/monitor/start","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /remote_id/monitor/stop`
```bash
curl -sS -X POST $BASE/remote_id/monitor/stop -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```
```json
{"command":"remote_id/monitor/stop","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /system/reboot` (dangerous)
```bash
curl -sS -X POST $BASE/system/reboot -H 'Content-Type: application/json' -d '{"payload":{},"confirm":true}'
```
```json
{"command":"system/reboot","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /system/shutdown` (dangerous)
```bash
curl -sS -X POST $BASE/system/shutdown -H 'Content-Type: application/json' -d '{"payload":{},"confirm":true}'
```
```json
{"command":"system/shutdown","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

### System Controller (REST)

#### `GET /health`
```bash
curl -sS $SC/health
```
```json
{"status":"ok","timestamp_ms":1700000000000}
```

#### `GET /status`
```bash
curl -sS $SC/status
```
```json
{"timestamp_ms":1700000000000,"system":{"status":"ok"},"ups":{"status":"ok"},"services":[],"network":{},"audio":{}}
```

#### `GET /system`
```bash
curl -sS $SC/system
```
```json
{"timestamp_ms":1700000000000,"status":"ok","uptime_s":4671}
```

#### `GET /ups`
```bash
curl -sS $SC/ups
```
```json
{"timestamp_ms":1700000000000,"status":"ok","soc_percent":98}
```

#### `GET /services`
```bash
curl -sS $SC/services
```
```json
[{"name":"gpsd","active_state":"active","sub_state":"running","restart_count":0}]
```

#### `GET /network` (summary)
```bash
curl -sS $SC/network
```
```json
{"wifi":{"timestamp_ms":1700000000000,"enabled":true,"connected":true,"ssid":"lab"},"bluetooth":{"timestamp_ms":1700000000000,"enabled":false,"scanning":false,"paired_count":0,"connected_devices":[]}}
```

#### `GET /network/wifi/state`
```bash
curl -sS $SC/network/wifi/state
```
```json
{"timestamp_ms":1700000000000,"enabled":true,"connected":true,"ssid":"lab","ip":"192.168.1.35","last_update_ms":1700000000000}
```

#### `GET /network/wifi/scan`
```bash
curl -sS $SC/network/wifi/scan
```
```json
{"timestamp_ms":1700000000000,"networks":[{"ssid":"lab","bssid":"aa:bb:cc:dd:ee:ff","security":"wpa2","signal_dbm":-48,"channel":6,"frequency_mhz":2437,"known":true}]}
```

#### `GET /network/bluetooth/state`
```bash
curl -sS $SC/network/bluetooth/state
```
```json
{"timestamp_ms":1700000000000,"enabled":false,"scanning":false,"paired_count":0,"connected_devices":[],"last_update_ms":1700000000000}
```

#### `GET /network/bluetooth/devices`
```bash
curl -sS $SC/network/bluetooth/devices
```
```json
{"timestamp_ms":1700000000000,"devices":[{"addr":"00:11:22:33:44:55","name":"sensor","paired":true,"connected":false,"rssi_dbm":-40}]}
```

#### `GET /gps`
```bash
curl -sS $SC/gps
```
```json
{"timestamp_ms":1700000000000,"fix":"NO_FIX","satellites":{"in_view":0,"in_use":0},"last_update_ms":1700000000000,"source":"gpsd"}
```

#### `GET /audio`
```bash
curl -sS $SC/audio
```
```json
{"timestamp_ms":1700000000000,"status":"ok","muted":false,"volume_percent":100}
```

### System Controller (Commands)

#### `POST /services/{name}/restart`
```bash
curl -sS -X POST $SC/services/gpsd/restart -H 'Content-Type: application/json' -d '{"payload":{},"confirm":true}'
```
```json
{"command":"services/restart","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /network/wifi/enable`
```bash
curl -sS -X POST $SC/network/wifi/enable -H 'Content-Type: application/json' -d '{"payload":{"enabled":true},"confirm":false}'
```
```json
{"command":"network/wifi/enable","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /network/wifi/disable`
```bash
curl -sS -X POST $SC/network/wifi/disable -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```
```json
{"command":"network/wifi/disable","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /network/wifi/connect`
```bash
curl -sS -X POST $SC/network/wifi/connect -H 'Content-Type: application/json' -d '{"payload":{"ssid":"lab","password":"secret"},"confirm":false}'
```
```json
{"command":"network/wifi/connect","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /network/wifi/disconnect`
```bash
curl -sS -X POST $SC/network/wifi/disconnect -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```
```json
{"command":"network/wifi/disconnect","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /network/bluetooth/enable`
```bash
curl -sS -X POST $SC/network/bluetooth/enable -H 'Content-Type: application/json' -d '{"payload":{"enabled":true},"confirm":false}'
```
```json
{"command":"network/bluetooth/enable","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /network/bluetooth/disable`
```bash
curl -sS -X POST $SC/network/bluetooth/disable -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```
```json
{"command":"network/bluetooth/disable","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /network/bluetooth/scan/start`
```bash
curl -sS -X POST $SC/network/bluetooth/scan/start -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```
```json
{"command":"network/bluetooth/scan/start","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /network/bluetooth/scan/stop`
```bash
curl -sS -X POST $SC/network/bluetooth/scan/stop -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```
```json
{"command":"network/bluetooth/scan/stop","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /network/bluetooth/pair`
```bash
curl -sS -X POST $SC/network/bluetooth/pair -H 'Content-Type: application/json' -d '{"payload":{"addr":"00:11:22:33:44:55","pin":"0000"},"confirm":false}'
```
```json
{"command":"network/bluetooth/pair","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /network/bluetooth/unpair`
```bash
curl -sS -X POST $SC/network/bluetooth/unpair -H 'Content-Type: application/json' -d '{"payload":{"addr":"00:11:22:33:44:55"},"confirm":false}'
```
```json
{"command":"network/bluetooth/unpair","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /gps/restart`
```bash
curl -sS -X POST $SC/gps/restart -H 'Content-Type: application/json' -d '{"payload":{},"confirm":true}'
```
```json
{"command":"gps/restart","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /audio/mute`
```bash
curl -sS -X POST $SC/audio/mute -H 'Content-Type: application/json' -d '{"payload":{"muted":true},"confirm":false}'
```
```json
{"command":"audio/mute","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /audio/volume`
```bash
curl -sS -X POST $SC/audio/volume -H 'Content-Type: application/json' -d '{"payload":{"volume_percent":50},"confirm":false}'
```
```json
{"command":"audio/volume","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /system/reboot` (dangerous)
```bash
curl -sS -X POST $SC/system/reboot -H 'Content-Type: application/json' -d '{"payload":{},"confirm":true}'
```
```json
{"command":"system/reboot","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /system/shutdown` (dangerous)
```bash
curl -sS -X POST $SC/system/shutdown -H 'Content-Type: application/json' -d '{"payload":{},"confirm":true}'
```
```json
{"command":"system/shutdown","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

### AntSDR Scan (REST)

#### `GET /health`
```bash
curl -sS $RF/health
```
```json
{"status":"ok","timestamp_ms":1700000000000}
```

#### `GET /version`
```bash
curl -sS $RF/version
```
```json
{"version":"dev","timestamp_ms":1700000000000}
```

#### `GET /stats`
```bash
curl -sS $RF/stats
```
```json
{"timestamp_ms":1700000000000,"frames_processed":10,"events_emitted":5}
```

#### `GET /device`
```bash
curl -sS $RF/device
```
```json
{"timestamp_ms":1700000000000,"connected":false,"last_error":"device_not_connected"}
```

#### `GET /sweep/state`
```bash
curl -sS $RF/sweep/state
```
```json
{"timestamp_ms":1700000000000,"running":false,"plans":[{"name":"default","start_hz":5700000000,"end_hz":5900000000,"step_hz":2000000}]}
```

#### `GET /gain`
```bash
curl -sS $RF/gain
```
```json
{"timestamp_ms":1700000000000,"mode":"auto"}
```

#### `GET /config`
```bash
curl -sS $RF/config
```
```json
{"timestamp_ms":1700000000000,"output_jsonl":"/opt/ndefender/logs/antsdr_scan.jsonl"}
```

#### `GET /events/last?limit=1`
```bash
curl -sS "$RF/events/last?limit=1"
```
```json
{"timestamp_ms":1700000000000,"events":[{"type":"RF_CONTACT_NEW","timestamp_ms":1700000000000,"source":"antsdr","data":{"id":"rf:1","freq_hz":5740000000,"rssi_dbm":-48}}]}
```

### AntSDR Scan (Commands)

#### `POST /config/reload`
```bash
curl -sS -X POST $RF/config/reload -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```
```json
{"command":"config/reload","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /sweep/start`
```bash
curl -sS -X POST $RF/sweep/start -H 'Content-Type: application/json' -d '{"payload":{"plan":"default"},"confirm":false}'
```
```json
{"command":"sweep/start","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /sweep/stop`
```bash
curl -sS -X POST $RF/sweep/stop -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```
```json
{"command":"sweep/stop","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /gain/set`
```bash
curl -sS -X POST $RF/gain/set -H 'Content-Type: application/json' -d '{"payload":{"mode":"auto"},"confirm":false}'
```
```json
{"command":"gain/set","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /device/reset` (dangerous)
```bash
curl -sS -X POST $RF/device/reset -H 'Content-Type: application/json' -d '{"payload":{},"confirm":true}'
```
```json
{"command":"device/reset","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /device/calibrate` (dangerous)
```bash
curl -sS -X POST $RF/device/calibrate -H 'Content-Type: application/json' -d '{"payload":{"kind":"rf_dc"},"confirm":true}'
```
```json
{"command":"device/calibrate","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /run/start` (legacy)
```bash
curl -sS -X POST $RF/run/start -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```
```json
{"command":"run/start","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /run/stop` (legacy)
```bash
curl -sS -X POST $RF/run/stop -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```
```json
{"command":"run/stop","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /run/replay` (legacy)
```bash
curl -sS -X POST $RF/run/replay -H 'Content-Type: application/json' -d '{"payload":{"source":"file.jsonl"},"confirm":false}'
```
```json
{"command":"run/replay","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

### RemoteID Engine (REST)

Base is service-local `/api/v1`:

#### `GET /health`
```bash
curl -sS http://127.0.0.1:<remoteid_port>/api/v1/health
```
```json
{"status":"ok","timestamp_ms":1700000000000}
```

#### `GET /status`
```bash
curl -sS http://127.0.0.1:<remoteid_port>/api/v1/status
```
```json
{"timestamp_ms":1700000000000,"state":"degraded","mode":"live","capture_active":true,"last_error":"no_odid_frames"}
```

#### `GET /contacts`
```bash
curl -sS http://127.0.0.1:<remoteid_port>/api/v1/contacts
```
```json
{"timestamp_ms":1700000000000,"contacts":[{"id":"rid:123","type":"REMOTE_ID","source":"remoteid","last_seen_ts":1700000000000,"severity":"unknown","lat":23.0,"lon":72.0}]}
```

#### `GET /stats`
```bash
curl -sS http://127.0.0.1:<remoteid_port>/api/v1/stats
```
```json
{"timestamp_ms":1700000000000,"frames":10,"decoded":2,"dropped":0,"dedupe_hits":1}
```

#### `GET /replay/state`
```bash
curl -sS http://127.0.0.1:<remoteid_port>/api/v1/replay/state
```
```json
{"timestamp_ms":1700000000000,"active":false,"source":"none"}
```

### RemoteID Engine (Commands)

#### `POST /monitor/start`
```bash
curl -sS -X POST http://127.0.0.1:<remoteid_port>/api/v1/monitor/start -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```
```json
{"command":"monitor/start","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /monitor/stop`
```bash
curl -sS -X POST http://127.0.0.1:<remoteid_port>/api/v1/monitor/stop -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```
```json
{"command":"monitor/stop","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /replay/start`
```bash
curl -sS -X POST http://127.0.0.1:<remoteid_port>/api/v1/replay/start -H 'Content-Type: application/json' -d '{"payload":{"source":"file.jsonl"},"confirm":false}'
```
```json
{"command":"replay/start","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /replay/stop`
```bash
curl -sS -X POST http://127.0.0.1:<remoteid_port>/api/v1/replay/stop -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```
```json
{"command":"replay/stop","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

### Observability (REST)

#### `GET /health`
```bash
curl -sS http://127.0.0.1:<obs_port>/api/v1/health
```
```json
{"status":"ok","timestamp_ms":1700000000000}
```

#### `GET /health/detail`
```bash
curl -sS http://127.0.0.1:<obs_port>/api/v1/health/detail
```
```json
{"timestamp_ms":1700000000000,"checks":[]}
```

#### `GET /status`
```bash
curl -sS http://127.0.0.1:<obs_port>/api/v1/status
```
```json
{"timestamp_ms":1700000000000,"ok":true}
```

#### `GET /version`
```bash
curl -sS http://127.0.0.1:<obs_port>/api/v1/version
```
```json
{"timestamp_ms":1700000000000,"version":"dev"}
```

#### `GET /config`
```bash
curl -sS http://127.0.0.1:<obs_port>/api/v1/config
```
```json
{"timestamp_ms":1700000000000,"profile":"default"}
```

#### `GET /metrics`
```bash
curl -sS http://127.0.0.1:<obs_port>/api/v1/metrics
```
```json
{"timestamp_ms":1700000000000,"metrics":{}}
```

#### `POST /diag/bundle`
```bash
curl -sS -X POST http://127.0.0.1:<obs_port>/api/v1/diag/bundle -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```
```json
{"command":"diag/bundle","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

## WebSocket (Aggregator)

Connect:
```bash
websocat ws://127.0.0.1:8001/api/v1/ws
```

Example envelope:
```json
{"type":"SYSTEM_UPDATE","timestamp_ms":1700000000000,"source":"aggregator","data":{"timestamp_ms":1700000000000,"overall_ok":false}}
```

COMMAND_ACK example:
```json
{"type":"COMMAND_ACK","timestamp_ms":1700000000000,"source":"aggregator","data":{"command":"scan/start","command_id":"uuid","ok":true,"detail":null}}
```

## How to Run Locally
```bash
npm install
scripts/validate.sh
```

## How to Validate Contracts
```bash
scripts/validate.sh
```

## Smoke Tests (curl + websocat)
Local:
```bash
scripts/smoke_local.sh
```
Public:
```bash
scripts/smoke_public.sh
```

## Integration Steps (UI / AI Tools)
1) Use `GET /status` to render the initial UI.
2) Connect WS and merge incremental updates.
3) Use command endpoints for operator actions and wait for `COMMAND_ACK`.
4) Use error `detail` to display human‑readable failure reasons.

## Security Notes
- Do not expose legacy Flask on `:8000`.
- Keep reverse proxy / perimeter controls in front of the Aggregator.

## Docs Structure (Future‑Proof)
- `docs/INDEX.md` for navigation.
- `docs/api/`, `docs/contracts/`, `docs/guides/`, `docs/ops/`, `docs/evidence/` are aliases.
- `packages/` provides future packaging layout.
