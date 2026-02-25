# N-Defender Unified API (All-in-One) 📡

This document is the single, production-grade reference for **all REST + WebSocket APIs** in the N-Defender unified system. It consolidates Backend Aggregator (primary), System Controller, Observability, and subsystem-local APIs (AntSDR Scan, RemoteID Engine), plus UI integration guidance.

---

## ✅ Source of Truth Rules (Non‑Negotiable)
- JSONL logs are the ground truth for AntSDR and RemoteID events.
- WebSocket is the fast path for UI responsiveness and can be transient.
- REST snapshots are authoritative for UI rendering and state recovery.

---

## 🔑 Auth, RBAC, and Security

### Current Deployment (No Auth Required)
- Auth headers are optional and not required.
- `X-API-Key` / `X-Role` are ignored if provided.
- Perimeter controls (VPN, allowlists, reverse proxy) are recommended.

### System Controller
- No API key required in current deployment.

### Observability
- No API key required in current deployment.

### AntSDR Scan (Local API)
- No API key required in current deployment.

### RemoteID Engine (Local API)
- No API key enforcement.

---

## ⏱️ Units & Naming Rules
- Timestamps are integer **milliseconds** since epoch unless noted.
- JSONL uses `timestamp`; REST/WS uses `timestamp_ms`.
- Frequencies use Hertz: `freq_hz`, `bucket_hz`, `step_hz`, `start_hz`, `stop_hz`.
- Latitude/Longitude use decimal degrees: `lat`, `lon`.
- Distances use meters when present: `distance_m`.

---

## ❗ Error Response Formats

### FastAPI Services (Aggregator / System Controller / Observability)
```json
{"detail": "<message>"}
```

### AntSDR Scan (aiohttp)
```json
{"error": {"code": "<code>", "message": "<message>"}}
```

### RemoteID Engine (embedded HTTP)
- Unknown endpoints return `404` with no JSON body.

---

## 🌐 Backend Aggregator API (Primary)
**Base URL:** `/api/v1`

Common headers:
- None required in current deployment.

Common errors:
- `429` Rate limit exceeded (command endpoints)

### `GET /health`
### `GET /health`
**Auth:** None (no headers required).

Response fields:
- `status` string
- `timestamp_ms` integer

Example response:
```json
{"status":"ok","timestamp_ms":1700000000000}
```

Errors: `403`.

---

### `GET /status`
**Auth:** None (no headers required).

Response fields:
- `timestamp_ms` integer
- `system` object
- `power` object
- `rf` object
- `remote_id` object
- `vrx` object
- `fpv` object
- `video` object
- `services` array
- `network` object
- `audio` object
- `contacts` array
- `replay` object
- `overall_ok` boolean

Example response:
```json
{
  "timestamp_ms": 1700000000000,
  "system": {"status": "ok"},
  "power": {"status": "ok"},
  "rf": {"status": "offline", "last_error": "antsdr_unreachable", "scan_active": false},
  "remote_id": {"state": "degraded", "capture_active": true, "last_error": "no_odid_frames"},
  "vrx": {"selected": 1, "vrx": []},
  "fpv": {"selected": 1, "freq_hz": 5740000000, "rssi_raw": 120},
  "video": {"selected": 1, "status": "ok"},
  "services": [],
  "network": {},
  "audio": {},
  "contacts": [],
  "replay": {"active": false, "source": "none"},
  "overall_ok": false
}
```

Errors: `403`.

---

### `GET /contacts`
**Auth:** None (no headers required).

Response fields:
- `contacts` array of unified contact objects

Unified contact fields (base):
- `id` string
- `type` string (`REMOTE_ID|RF|FPV`)
- `source` string (`remoteid|antsdr|esp32`)
- `last_seen_ts` integer
- `last_seen_uptime_ms` integer (optional; uptime-based timestamp when provided by device)
- `severity` string (`critical|high|medium|low|unknown`)

RemoteID contact fields:
- `model` string
- `operator_id` string
- `lat` number
- `lon` number
- `altitude_m` number
- `speed_m_s` number

RF contact fields:
- `freq_hz` number
- `bucket_hz` number
- `band` string
- `snr_db` number
- `peak_db` number
- `noise_floor_db` number
- `bandwidth_class` string
- `confidence` number
- `features.prominence_db` number
- `features.cluster_size` integer
- `features.pattern_hint` string
- `features.hop_hint` string
- `features.bandwidth_est_hz` number
- `features.burstiness` number
- `features.hop_rate_hz` number
- `features.control_score` number
- `features.class_path` array of string
- `features.classification_confidence` number
- `features.control_correlation` boolean

FPV contact fields:
- `vrx_id` integer
- `freq_hz` number
- `rssi_raw` integer
- `selected` integer

Example response:
```json
{
  "contacts": [
    {"id":"rf:5658000000","type":"RF","source":"antsdr","last_seen_ts":1700000000000,"severity":"high","freq_hz":5658000000}
  ]
}
```

Errors: `403`.

---

### `GET /system`
**Auth:** None (no headers required).

Response fields (System Controller `SystemStats`):
- `uptime_s` integer
- `cpu_temp_c` number
- `cpu_usage_percent` number
- `load_1m` number
- `load_5m` number
- `load_15m` number
- `ram_used_mb` integer
- `ram_total_mb` integer
- `disk_used_gb` integer
- `disk_total_gb` integer
- `throttled_flags` integer

Example response:
```json
{"cpu_temp_c":45.2,"cpu_usage_percent":12.5,"ram_used_mb":410,"disk_used_gb":12}
```

---

### `GET /power`
**Auth:** None (no headers required).

Response fields (UPS telemetry):
- `pack_voltage_v` number
- `current_a` number
- `input_vbus_v` number
- `input_power_w` number
- `soc_percent` integer
- `time_to_empty_s` integer
- `time_to_full_s` integer
- `per_cell_v` array of number
- `state` string (`IDLE|CHARGING|FAST_CHARGING|DISCHARGING|UNKNOWN`)

Example response:
```json
{"pack_voltage_v":12.4,"current_a":1.2,"soc_percent":78,"state":"DISCHARGING","per_cell_v":[4.1,4.1,4.1]}
```

---

### `GET /rf`
**Auth:** None (no headers required).

Response fields:
- `last_event_type` string
- `last_event` object
- `last_timestamp_ms` integer

Example response:
```json
{"last_event_type":"RF_CONTACT_UPDATE","last_event":{"id":"rf:5658000000"},"last_timestamp_ms":1700000000000}
```

---

### `GET /video`
**Auth:** None (no headers required).

Response fields:
- `selected` integer

Example response:
```json
{"selected":2}
```

---

### `GET /services`
**Auth:** None (no headers required).

Response is an array of objects with fields:
- `name` string
- `active_state` string
- `sub_state` string
- `restart_count` integer

Example response:
```json
[{"name":"ndefender-system-controller","active_state":"active","sub_state":"running","restart_count":1}]
```

---

### `GET /network`
**Auth:** None (no headers required).

Response fields:
- `connected` boolean
- `ssid` string
- `ip_v4` string
- `ip_v6` string

Example response:
```json
{"connected":true,"ssid":"MyWiFi","ip_v4":"192.168.1.100","ip_v6":"fe80::1"}
```

---

### `GET /audio`
**Auth:** None (no headers required).

Response fields:
- `volume_percent` integer
- `muted` boolean

Example response:
```json
{"volume_percent":60,"muted":false}
```

---

### Command Endpoints
All command endpoints accept:
```json
{"payload":{},"confirm":false}
```

All command endpoints return **CommandResult**:
```json
{"command":"vrx/tune","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

#### `POST /vrx/tune`
**Auth:** None (no headers required).

Payload fields:
- `vrx_id` integer (1‑3)
- `freq_hz` integer

Example request:
```json
{"payload":{"vrx_id":1,"freq_hz":5740000000}}
```

Example response:
```json
{"command":"vrx/tune","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

Errors: `403`, `429`.

---

#### `POST /scan/start`
**Auth:** None (no headers required).

Payload fields:
- `dwell_ms` integer
- `step_hz` integer
- `start_hz` integer
- `stop_hz` integer

Example request:
```json
{"payload":{"dwell_ms":200,"step_hz":2000000,"start_hz":5645000000,"stop_hz":5865000000}}
```

Example response:
```json
{"command":"scan/start","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

Errors: `403`, `429`.

---

#### `POST /scan/stop`
**Auth:** None (no headers required).

Example request:
```json
{"payload":{}}
```

Example response:
```json
{"command":"scan/stop","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

Errors: `403`, `429`.

---

#### `POST /video/select`
**Auth:** None (no headers required).

Payload fields:
- `ch` integer (1‑3)

Example request:
```json
{"payload":{"ch":2}}
```

Example response:
```json
{"command":"video/select","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

Errors: `403`, `429`.

---

#### `POST /system/reboot`
**Auth:** None (no headers required).

Requirements:
- `confirm=true`
- `safety.allow_unsafe_operations=true`
- Dangerous command rate limit applies

Example request:
```json
{"confirm":true}
```

Example response:
```json
{"command":"system/reboot","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

Errors: `400`, `403`, `429`.

---

#### `POST /system/shutdown`
Same requirements as reboot.

Example request:
```json
{"confirm":true}
```

Example response:
```json
{"command":"system/shutdown","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

Errors: `400`, `403`, `429`.

---

### Rate Limits (Aggregator)
- `command_per_minute`: **10/min**
- `dangerous_per_minute`: **2/min**

---

### WebSocket
**Endpoint:** `WS /api/v1/ws`

Envelope fields:
- `type` string
- `timestamp_ms` integer
- `source` string
- `data` object

On connect, the server immediately sends **SYSTEM_UPDATE** containing the full snapshot.
The server also emits **HEARTBEAT** events periodically to keep clients live.

Example envelope:
```json
{"type":"SYSTEM_UPDATE","timestamp_ms":1700000000000,"source":"aggregator","data":{"timestamp_ms":1700000000000,"contacts":[]}}
```

Event types (full catalog in `docs/WEBSOCKET_EVENTS.md`):
- `HEARTBEAT`
- `SYSTEM_UPDATE`
- `COMMAND_ACK`
- `ESP32_TELEMETRY`
- `LOG_EVENT`
- `CONTACT_NEW`, `CONTACT_UPDATE`, `CONTACT_LOST`
- `RF_CONTACT_NEW`, `RF_CONTACT_UPDATE`, `RF_CONTACT_LOST`
- `TELEMETRY_UPDATE`, `REPLAY_STATE`

---

## ⚙️ System Controller API
**Base URL:** `/api/v1`

Common headers:
- None required in current deployment.

Common errors:
- `400` Confirm required for reboot/shutdown/restart
- `403` Unsafe operations disabled
- `429` Cooldown active

### `GET /health`
Response fields:
- `ok` boolean
- `timestamp_ms` integer
- `version` string

Example response:
```json
{"ok":true,"timestamp_ms":1700000000000,"version":"0.1.0"}
```

---

### `GET /status`
**Auth:** None (no headers required).

Response fields:
- `timestamp_ms` integer
- `system` object
- `ups` object
- `services` array
- `network` object
- `audio` object

Example response:
```json
{"timestamp_ms":1700000000000,"system":{"cpu_temp_c":45.2},"ups":{"soc_percent":78,"state":"DISCHARGING"},"services":[],"network":{},"audio":{}}
```


---

### `GET /system`
Response fields:
- `uptime_s`, `cpu_temp_c`, `cpu_usage_percent`, `load_1m`, `load_5m`, `load_15m`
- `ram_used_mb`, `ram_total_mb`, `disk_used_gb`, `disk_total_gb`, `throttled_flags`

Example response:
```json
{"cpu_temp_c":45.2,"cpu_usage_percent":12.5}
```

---

### `GET /ups`
Response fields:
- `pack_voltage_v`, `current_a`, `input_vbus_v`, `input_power_w`
- `soc_percent`, `time_to_empty_s`, `time_to_full_s`
- `per_cell_v`, `state`

Example response:
```json
{"pack_voltage_v":12.4,"current_a":1.2,"soc_percent":78,"state":"DISCHARGING","per_cell_v":[4.1,4.1,4.1]}
```

---

### `GET /services`
Response is an array of:
- `name`, `active_state`, `sub_state`, `restart_count`

Example response:
```json
[{"name":"ndefender-system-controller","active_state":"active","sub_state":"running","restart_count":1}]
```

---

### `POST /services/{name}/restart`
Request body:
```json
{"confirm": true}
```

Response:
```json
{"type":"COMMAND_ACK","timestamp_ms":1700000000000,"data":{"command":"service_restart","name":"ndefender-system-controller","ok":true}}
```

Cooldown: **10s**.
Errors: `400`, `429`.

---

### `GET /network`
Response fields:
- `connected`, `ssid`, `ip_v4`, `ip_v6`

Example response:
```json
{"connected":true,"ssid":"MyWiFi","ip_v4":"192.168.1.100","ip_v6":"fe80::1"}
```

---

### `GET /audio`
Response fields:
- `volume_percent`, `muted`

Example response:
```json
{"volume_percent":60,"muted":false}
```

---

### `POST /system/reboot`
Request body:
```json
{"confirm": true}
```

Response:
```json
{"type":"COMMAND_ACK","timestamp_ms":1700000000000,"data":{"command":"reboot","ok":true,"reason":null}}
```

Cooldown: **30s**.
Requires `NDEFENDER_ALLOW_UNSAFE=true`.
Errors: `400`, `403`, `429`.

---

### `POST /system/shutdown`
Same as reboot.

Example request:
```json
{"confirm": true}
```

Example response:
```json
{"type":"COMMAND_ACK","timestamp_ms":1700000000000,"data":{"command":"shutdown","ok":true,"reason":null}}
```

---

### System Controller WebSocket
**Endpoint:** `WS /api/v1/ws`

Envelope fields:
- `type` string
- `timestamp_ms` integer
- `source` string (always `system`)
- `data` object

On connect, server sends:
- `LOG_EVENT` with `{"message":"HELLO"}`
- `SYSTEM_STATUS` with current `system` snapshot

Example envelope:
```json
{"type":"SYSTEM_STATUS","timestamp_ms":1700000000000,"source":"system","data":{"cpu_temp_c":45.2}}
```

Event types:
- `SYSTEM_STATUS`
- `UPS_UPDATE`
- `SERVICE_UPDATE`
- `NETWORK_UPDATE`
- `AUDIO_UPDATE`
- `LOG_EVENT`
- `COMMAND_ACK`

---

## 📈 Observability API
**Base URL:** `/api/v1`

Common headers:
- None required in current deployment.

Common errors:
- `429` Rate limit exceeded

### `GET /health`
Response:
```json
{"status":"ok"}
```

### `GET /health/detail`
Response fields:
- `generated_ts` integer
- `subsystems` array of objects
- `status` string

Example response:
```json
{"generated_ts":1700000000000,"subsystems":[],"status":"ok"}
```

### `GET /status`
Response fields:
- `generated_ts` integer
- `overall_state` string
- `state_counts` object
- `subsystems` array

Example response:
```json
{"generated_ts":1700000000000,"overall_state":"OK","state_counts":{"OK":4},"subsystems":[]}
```

### `GET /version`
Response:
```json
{"version":"1.0.0","git_sha":"deadbeef"}
```

### `GET /config`
Response: sanitized config object.

Example response:
```json
{"service":{"host":"0.0.0.0","port":9109},"auth":{"enabled":false,"api_key":null},"rate_limit":{"enabled":false,"max_requests":60,"window_s":60}}
```

### `GET /metrics`
Response: Prometheus text exposition (`text/plain; version=0.0.4`).

Example response:
```text
# HELP ndefender_jsonl_tail_lag_seconds JSONL tail lag
# TYPE ndefender_jsonl_tail_lag_seconds gauge
ndefender_jsonl_tail_lag_seconds{subsystem="antsdr"} 0
```

### `POST /diag/bundle`
Local‑only endpoint.

Response:
```json
{"path":"/tmp/ndefender_diag_1700000000000.tar.gz","size_bytes":123456,"created_ts":1700000000000}
```

Cooldown: **60s**.
Errors: `403`, `429`, `500`.

---

## 📡 AntSDR Scan Local API (RF Engine)
**Base URL:** `/api/v1`

Common headers:
- None required in current deployment.

Common errors:
- `404` Not found
- `409` Conflict
- `429` Too many clients (WebSocket)

### `GET /health`
Response fields:
- `status` string
- `engine_running` boolean
- `ws_backend_connected` boolean
- `last_event_timestamp_ms` integer or null
- `timestamp_ms` integer

Example response:
```json
{"status":"ok","engine_running":true,"ws_backend_connected":true,"last_event_timestamp_ms":1700000000000,"timestamp_ms":1700000000000}
```

### `GET /version`
Response:
```json
{"version":"1.0.0"}
```

### `GET /stats`
Response fields:
- `frames_processed` integer
- `detections_processed` integer
- `events_emitted` integer

Example response:
```json
{"frames_processed":10,"detections_processed":23,"events_emitted":5}
```

### `GET /config`
Response fields:
- `radio` object
- `tracker` object
- `detector` object
- `sweep` object
- `ws` object
- `classification` object
- `api` object

Example response:
```json
{"radio":{"uri":"","sample_rate":0,"rx_buffer_size":4096},"tracker":{"bucket_hz":0,"ttl_s":0,"min_hits_to_confirm":0,"update_interval_s":0,"correlation_enabled":false,"correlation_window_ms":100},"detector":{"min_snr_db":0.0,"lo_guard_hz":0.0},"sweep":{"bands":[{"name":"2G4","start_hz":2400000000,"stop_hz":2480000000,"step_hz":2000000}],"dwell_ms":0},"ws":{"enabled":false,"url":"","connect_timeout_s":5.0,"send_timeout_s":2.0,"max_retries":3,"retry_backoff_s":1.0},"classification":{"profiles":"/path/to/classification_profiles.yaml","hop_window_ms":1000,"min_hop_hz":200000.0},"api":{"enabled":true,"bind":"127.0.0.1","port":8890,"api_key":"***","max_clients":25,"event_buffer":500}}
```

### `POST /config/reload`
Response:
```json
{"status":"ok"}
```
Errors: `409` when scan is running.

### `POST /run/start`
Response:
```json
{"status":"ok"}
```
Errors: `409` when already running.

### `POST /run/stop`
Response:
```json
{"status":"ok"}
```
Errors: `409` when not running.

### `POST /run/replay`
Request:
```json
{"log_path":"/opt/ndefender/logs/antsdr_scan.jsonl","output_path":"/tmp/replay.jsonl","max_events":100}
```

Response:
```json
{"status":"ok","frames":12,"detections":34,"events_emitted":100}
```

Errors: `400`, `404`, `409`.

### `GET /events/last?limit=50`
Response:
```json
{"events":[{"type":"RF_CONTACT_NEW","timestamp":1700000000000,"source":"antsdr","data":{"id":"rf:5658000000","freq_hz":5658000000}}]}
```

### `WS /events`
- Enforces `api.max_clients` limit; returns `429` if exceeded.

Envelope:
```json
{"type":"RF_CONTACT_UPDATE","timestamp":1700000000000,"source":"antsdr","data":{"id":"rf:5658000000","freq_hz":5658000000}}
```

---

## 🛰️ RemoteID Engine Local API
**Base URL:** `/api/v1`

Common errors:
- `404` Not found for unknown endpoints

### `GET /status`
Response fields:
- `state` string (`offline|ok|degraded|replay`)
- `last_ts` integer
- `contacts_active` integer
- `mode` string (`live|replay`)
- `updated_ts` integer

Example response:
```json
{"state":"ok","last_ts":1700000000000,"contacts_active":1,"mode":"live","updated_ts":1700000000000}
```

### `GET /health`
Same response as `/status`.

---

## 🧭 UI Integration Guidance

Recommended UI flow:
1. Fetch snapshot from Backend Aggregator `GET /api/v1/status`.
2. Connect WS to `WS /api/v1/ws` and apply incremental events.
3. On disconnect, re-fetch snapshot and reconnect.
4. Treat JSONL as the authoritative audit trail; WS may drop events.

Suggested state merge rules:
- Apply `SYSTEM_UPDATE` as a full overwrite of cached state.
- Apply `CONTACT_*` and `RF_CONTACT_*` as incremental updates.
- Apply `COMMAND_ACK` to show action confirmation.
- Display `timestamp_ms` and `last_seen_ts` as user-local time.

---

## 📎 Pagination Rules
- No REST endpoint uses pagination today.
- Bounded list: `GET /events/last?limit=N` (AntSDR only).

---

## ✅ Example Requests (Aggregator)

Health:
```bash
curl http://127.0.0.1:8001/api/v1/health
```

Status:
```bash
curl http://127.0.0.1:8001/api/v1/status
```

Contacts:
```bash
curl http://127.0.0.1:8001/api/v1/contacts
```

Command:
```bash
curl -X POST http://127.0.0.1:8001/api/v1/vrx/tune \
  -H "Content-Type: application/json" \
  -d '{"payload":{"vrx_id":1,"freq_hz":5740000000}}'
```
