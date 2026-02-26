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
- Timestamps are integer **milliseconds** since epoch unless explicitly noted as uptime-based.
- **`timestamp_ms` is required everywhere** (REST, WS, JSONL). Plain `timestamp` is invalid.
- Frequencies use Hertz: `freq_hz`, `bucket_hz`, `step_hz`, `start_hz`, `stop_hz`.
- GPS uses `latitude`/`longitude`; RemoteID contacts use `lat`/`lon`.
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
- `overall_ok` boolean
- `system` object
- `power` object
- `rf` object
- `remote_id` object
- `vrx` object
- `fpv` object
- `video` object
- `services` array
- `network` object
- `gps` object
- `esp32` object
- `antsdr` object
- `audio` object
- `contacts` array
- `replay` object

Example response:
```json
{
  "timestamp_ms": 1700000000000,
  "overall_ok": false,
  "system": {
    "status": "degraded",
    "uptime_s": 4671,
    "version": {"app": "ndefender-backend-aggregator", "git_sha": "dev", "build_ts": 1700000000000},
    "cpu": {"temp_c": 36.9, "load1": 0.4, "load5": 0.6, "load15": 0.5, "usage_percent": 12.4},
    "ram": {"total_mb": 16215, "used_mb": 1931, "free_mb": 14284},
    "storage": {"root": {"total_gb": 117, "used_gb": 70, "free_gb": 46.5}}
  },
  "power": {
    "status": "ok",
    "pack_voltage_v": 16.6,
    "current_a": -0.01,
    "input_vbus_v": 0,
    "input_power_w": 0,
    "soc_percent": 98,
    "state": "IDLE",
    "time_to_empty_s": 1866420
  },
  "rf": {
    "status": "offline",
    "scan_active": false,
    "last_error": "antsdr_unreachable",
    "last_event_type": "RF_SCAN_OFFLINE",
    "last_timestamp_ms": 1700000000000,
    "last_event": {"reason": "antsdr_unreachable"}
  },
  "remote_id": {
    "state": "DEGRADED",
    "mode": "live",
    "capture_active": true,
    "last_error": "no_odid_frames",
    "last_event_type": "REMOTEID_STALE",
    "last_timestamp_ms": 1700000000000,
    "last_event": {"reason": "no_odid_frames"}
  },
  "vrx": {
    "selected": 1,
    "scan_state": "idle",
    "sys": {"uptime_ms": 4686359, "heap": 337624, "status": "CONNECTED"},
    "vrx": [
      {"id": 1, "freq_hz": 5740000000, "rssi_raw": 632},
      {"id": 2, "freq_hz": 5800000000, "rssi_raw": 234}
    ]
  },
  "fpv": {"selected": 1, "scan_state": "idle", "freq_hz": 5740000000, "rssi_raw": 632},
  "video": {"selected": 1, "status": "ok"},
  "services": [{"name": "ndefender-backend", "active_state": "active", "sub_state": "running", "restart_count": 0}],
  "network": {
    "wifi": {"timestamp_ms": 1700000000000, "enabled": true, "connected": true, "ssid": "lab", "ip": "192.168.1.35"},
    "bluetooth": {"timestamp_ms": 1700000000000, "enabled": false, "scanning": false, "paired_count": 0, "connected_devices": []}
  },
  "gps": {
    "timestamp_ms": 1700000000000,
    "fix": "NO_FIX",
    "satellites": {"in_view": 0, "in_use": 0},
    "last_update_ms": 1700000000000,
    "source": "gpsd",
    "last_error": "no_fix"
  },
  "esp32": {
    "timestamp_ms": 1700000000000,
    "connected": true,
    "last_seen_ms": 1700000000000,
    "heartbeat": {"ok": true, "interval_ms": 1000, "last_heartbeat_ms": 1700000000000},
    "capabilities": {"leds": true, "vrx": true, "video_switch": true}
  },
  "antsdr": {
    "timestamp_ms": 1700000000000,
    "connected": false,
    "last_error": "antsdr_unreachable"
  },
  "audio": {"timestamp_ms": 1700000000000, "status": "ok", "muted": false, "volume_percent": 100},
  "contacts": [
    {"id": "fpv:1", "type": "FPV", "source": "esp32", "last_seen_ts": 1700000000000, "severity": "unknown", "vrx_id": 1, "freq_hz": 5740000000, "rssi_raw": 632, "selected": 1, "last_seen_uptime_ms": 4686359}
  ],
  "replay": {"active": false, "source": "none"}
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
- `last_seen_uptime_ms` integer (ESP32 uptime-based timestamp, if available)

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
- `timestamp_ms` integer
- `status` string (`ok|degraded|offline`)
- `uptime_s` integer
- `version` object `{app, git_sha?, build_ts?}`
- `cpu` object `{temp_c, load1, load5, load15, usage_percent?}`
- `ram` object `{total_mb, used_mb, free_mb}`
- `storage` object `{root:{total_gb, used_gb, free_gb}, logs?:{total_gb, used_gb, free_gb}}`
- `last_error` string (optional)

Example response:
```json
{
  "timestamp_ms": 1700000000000,
  "status": "ok",
  "uptime_s": 4671,
  "version": {"app": "ndefender-system-controller", "git_sha": "dev", "build_ts": 1700000000000},
  "cpu": {"temp_c": 36.9, "load1": 0.4, "load5": 0.6, "load15": 0.5, "usage_percent": 12.4},
  "ram": {"total_mb": 16215, "used_mb": 1931, "free_mb": 14284},
  "storage": {"root": {"total_gb": 117, "used_gb": 70, "free_gb": 46.5}}
}
```

---

### `GET /power`
**Auth:** None (no headers required).

Response fields (UPS telemetry):
- `timestamp_ms` integer
- `status` string (`ok|degraded|offline`)
- `pack_voltage_v` number
- `current_a` number
- `input_vbus_v` number
- `input_power_w` number
- `soc_percent` integer
- `time_to_empty_s` integer
- `time_to_full_s` integer
- `per_cell_v` array of number
- `state` string (`IDLE|CHARGING|FAST_CHARGING|DISCHARGING|UNKNOWN`)
- `last_error` string (optional)

Example response:
```json
{"timestamp_ms":1700000000000,"status":"ok","pack_voltage_v":12.4,"current_a":1.2,"soc_percent":78,"state":"DISCHARGING","per_cell_v":[4.1,4.1,4.1]}
```

---

### `GET /rf`
**Auth:** None (no headers required).

Response fields:
- `status` string (`ok|degraded|offline|unknown`)
- `scan_active` boolean
- `last_error` string (optional)
- `last_event_type` string
- `last_event` object
- `last_timestamp_ms` integer

Example response:
```json
{"status":"offline","scan_active":false,"last_error":"antsdr_unreachable","last_event_type":"RF_SCAN_OFFLINE","last_event":{"reason":"antsdr_unreachable"},"last_timestamp_ms":1700000000000}
```

---

### `GET /video`
**Auth:** None (no headers required).

Response fields:
- `selected` integer
- `status` string (`ok|offline|unknown`)

Example response:
```json
{"selected":2,"status":"ok"}
```

---

### `GET /services`
**Auth:** None (no headers required).

Response is an array of objects with fields:
- `name` string
- `active_state` string
- `sub_state` string
- `restart_count` integer
- `uptime_s` integer (optional)
- `last_restart_ms` integer (optional)
- `last_error` string (optional)

Example response:
```json
[{"name":"ndefender-system-controller","active_state":"active","sub_state":"running","restart_count":1,"uptime_s":3600}]
```

---

### `GET /network` (summary)
**Auth:** None (no headers required).

Summary view for quick UI display (legacy compatible).

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

### `GET /network/wifi/state`
**Auth:** None (no headers required).

Response fields:
- `timestamp_ms` integer
- `enabled` boolean
- `connected` boolean
- `ssid` string (optional)
- `bssid` string (optional)
- `ip` string (optional)
- `rssi_dbm` integer (optional)
- `link_quality` integer (optional)
- `last_update_ms` integer
- `last_error` string (optional)

Example response:
```json
{"timestamp_ms":1700000000000,"enabled":true,"connected":true,"ssid":"MyWiFi","bssid":"aa:bb:cc:dd:ee:ff","ip":"192.168.1.100","rssi_dbm":-48,"last_update_ms":1700000000000}
```

---

### `GET /network/wifi/scan`
**Auth:** None (no headers required).

Response fields:
- `timestamp_ms` integer
- `networks` array of `{ssid,bssid,security,signal_dbm?,channel?,frequency_mhz?,known?}`

Example response:
```json
{"timestamp_ms":1700000000000,"networks":[{"ssid":"MyWiFi","bssid":"aa:bb:cc:dd:ee:ff","security":"wpa2","signal_dbm":-48,"channel":11,"frequency_mhz":2462,"known":true}]}
```

---

### `GET /network/bluetooth/state`
**Auth:** None (no headers required).

Response fields:
- `timestamp_ms` integer
- `enabled` boolean
- `scanning` boolean
- `paired_count` integer
- `connected_devices` array of `{addr,name,rssi_dbm?}`
- `last_update_ms` integer
- `last_error` string (optional)

Example response:
```json
{"timestamp_ms":1700000000000,"enabled":false,"scanning":false,"paired_count":0,"connected_devices":[],"last_update_ms":1700000000000}
```

---

### `GET /network/bluetooth/devices`
**Auth:** None (no headers required).

Response fields:
- `timestamp_ms` integer
- `devices` array of `{addr,name,rssi_dbm?,paired,connected}`

Example response:
```json
{"timestamp_ms":1700000000000,"devices":[{"addr":"00:11:22:33:44:55","name":"Headset","paired":true,"connected":false}]}
```

---

### `GET /audio`
**Auth:** None (no headers required).

Response fields:
- `timestamp_ms` integer
- `status` string (`ok|degraded|offline`)
- `volume_percent` integer
- `muted` boolean
- `last_error` string (optional)

Example response:
```json
{"timestamp_ms":1700000000000,"status":"ok","volume_percent":60,"muted":false}
```

---

### `GET /gps`
**Auth:** None (no headers required).

Response fields:
- `timestamp_ms` integer
- `fix` string (`NO_FIX|FIX_2D|FIX_3D`)
- `satellites` object `{in_view,in_use}`
- `hdop`/`vdop`/`pdop` numbers (optional)
- `latitude`/`longitude` numbers (optional)
- `altitude_m` number (optional)
- `speed_m_s` number (optional)
- `heading_deg` number (optional)
- `last_update_ms` integer
- `age_ms` integer (optional)
- `source` string (e.g. `gpsd`)
- `last_error` string (optional)

Example response:
```json
{"timestamp_ms":1700000000000,"fix":"NO_FIX","satellites":{"in_view":0,"in_use":0},"last_update_ms":1700000000000,"source":"gpsd","last_error":"no_fix"}
```

---

### `GET /esp32`
**Auth:** None (no headers required).

Response fields:
- `timestamp_ms` integer
- `connected` boolean
- `last_seen_ms` integer
- `rtt_ms` integer (optional)
- `fw_version` string (optional)
- `heartbeat` object `{ok, interval_ms, last_heartbeat_ms}`
- `capabilities` object `{buttons, leds, buzzer, vrx, video_switch, config}`
- `last_error` string (optional)

Example response:
```json
{"timestamp_ms":1700000000000,"connected":true,"last_seen_ms":1700000000000,"heartbeat":{"ok":true,"interval_ms":1000,"last_heartbeat_ms":1700000000000},"capabilities":{"leds":true,"vrx":true,"video_switch":true}}
```

---

### `GET /esp32/config`
**Auth:** None (no headers required).

Response fields:
- `timestamp_ms` integer
- `schema_version` string (optional)
- `config` object (device-specific)

Example response:
```json
{"timestamp_ms":1700000000000,"schema_version":"1","config":{"scan_step_hz":2000000}}
```

---

### `GET /antsdr`
**Auth:** None (no headers required).

Aggregated AntSDR summary.

Response fields:
- `timestamp_ms` integer
- `connected` boolean
- `uri` string (optional)
- `temperature_c` number (optional)
- `last_error` string (optional)

Example response:
```json
{"timestamp_ms":1700000000000,"connected":false,"last_error":"antsdr_unreachable"}
```

---

### `GET /antsdr/sweep/state`
**Auth:** None (no headers required).

Response fields:
- `timestamp_ms` integer
- `running` boolean
- `active_plan` string (optional)
- `plans` array
- `last_update_ms` integer
- `last_error` string (optional)

Example response:
```json
{"timestamp_ms":1700000000000,"running":false,"plans":[{"name":"analog_5g8","start_hz":5645000000,"end_hz":5865000000,"step_hz":2000000}],"last_update_ms":1700000000000}
```

---

### `GET /antsdr/gain`
**Auth:** None (no headers required).

Response fields:
- `timestamp_ms` integer
- `mode` string (`manual|auto`)
- `gain_db` number (optional)
- `limits` object `{min_db,max_db}` (optional)

Example response:
```json
{"timestamp_ms":1700000000000,"mode":"auto"}
```

---

### `GET /antsdr/stats`
**Auth:** None (no headers required).

Response fields:
- `timestamp_ms` integer
- `frames_processed` integer
- `events_emitted` integer
- `last_event_timestamp_ms` integer (optional)

Example response:
```json
{"timestamp_ms":1700000000000,"frames_processed":10,"events_emitted":5}
```

---

### `GET /remote_id`
**Auth:** None (no headers required).

Aggregated RemoteID summary.

Response fields:
- `timestamp_ms` integer
- `state` string (`ok|degraded|offline|replay`)
- `mode` string (`live|replay|off`)
- `capture_active` boolean
- `contacts_active` integer (optional)
- `last_update_ms` integer (optional)
- `last_error` string (optional)

Example response:
```json
{"timestamp_ms":1700000000000,"state":"degraded","mode":"live","capture_active":true,"last_error":"no_odid_frames"}
```

---

### `GET /remote_id/contacts`
**Auth:** None (no headers required).

Response fields:
- `timestamp_ms` integer
- `contacts` array (RemoteID contacts)

Example response:
```json
{"timestamp_ms":1700000000000,"contacts":[{"id":"rid:123","type":"REMOTE_ID","source":"remoteid","last_seen_ts":1700000000000,"severity":"unknown","lat":23.0,"lon":72.0}]}
```

---

### `GET /remote_id/stats`
**Auth:** None (no headers required).

Response fields:
- `timestamp_ms` integer
- `frames` integer
- `decoded` integer
- `dropped` integer (optional)
- `dedupe_hits` integer (optional)

Example response:
```json
{"timestamp_ms":1700000000000,"frames":10,"decoded":2,"dropped":0,"dedupe_hits":1}
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

Confirm gating & errors:
- Dangerous commands **require** `confirm=true`.
- If `confirm` is missing/false: `400 {"detail":"confirm_required"}`.
- If unsafe operations are disabled or local-only: `403 {"detail":"unsafe_disabled"}` or `{"detail":"local_only"}`.
- Invalid state: `409 {"detail":"invalid_state"}`.
- Rate limits: `429 {"detail":"rate_limited"}`.

#### `POST /vrx/tune`
**Auth:** None (no headers required).

Payload fields:
- `vrx_id` integer (1‑3)
- `freq_hz` integer

Example request:
```json
{"payload":{"vrx_id":1,"freq_hz":5740000000},"confirm":false}
```

Example response:
```json
{"command":"vrx/tune","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

Errors: `403`, `429`.

---

#### `POST /audio/mute`
Payload fields: `muted` boolean

Example request:
```json
{"payload":{"muted":true},"confirm":false}
```

Example response:
```json
{"command":"audio/mute","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

Errors: `400`, `409`, `429`.

---

#### `POST /audio/volume`
Payload fields: `volume_percent` integer (0‑100)

Example request:
```json
{"payload":{"volume_percent":50},"confirm":false}
```

Example response:
```json
{"command":"audio/volume","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

Errors: `400`, `409`, `429`.

---

#### `POST /network/wifi/enable`
Payload fields: `enabled` boolean

Example request:
```json
{"payload":{"enabled":true},"confirm":false}
```

Example response:
```json
{"command":"network/wifi/enable","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

Errors: `400`, `403`, `409`, `429`.

---

#### `POST /network/wifi/connect`
Payload fields: `ssid` string, `password` string, `hidden` boolean (optional)

Example request:
```json
{"payload":{"ssid":"MyWiFi","password":"secret","hidden":false},"confirm":false}
```

Example response:
```json
{"command":"network/wifi/connect","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

Errors: `400`, `403`, `409`, `429`.

---

#### `POST /network/wifi/disconnect`
Example request:
```json
{"payload":{},"confirm":false}
```

Example response:
```json
{"command":"network/wifi/disconnect","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

Errors: `400`, `409`, `429`.

---

#### `POST /network/bluetooth/enable`
Payload fields: `enabled` boolean

Example request:
```json
{"payload":{"enabled":true},"confirm":false}
```

Example response:
```json
{"command":"network/bluetooth/enable","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

Errors: `400`, `403`, `409`, `429`.

---

#### `POST /network/bluetooth/scan/start`
Example request:
```json
{"payload":{},"confirm":false}
```

Example response:
```json
{"command":"network/bluetooth/scan/start","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

Errors: `400`, `409`, `429`.

---

#### `POST /network/bluetooth/scan/stop`
Example request:
```json
{"payload":{},"confirm":false}
```

Example response:
```json
{"command":"network/bluetooth/scan/stop","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

Errors: `400`, `409`, `429`.

---

#### `POST /network/bluetooth/pair`
Payload fields: `addr` string, `pin` string (optional)

Example request:
```json
{"payload":{"addr":"00:11:22:33:44:55","pin":"0000"},"confirm":false}
```

Example response:
```json
{"command":"network/bluetooth/pair","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

Errors: `400`, `403`, `409`, `429`.

---

#### `POST /network/bluetooth/unpair`
Payload fields: `addr` string

Example request:
```json
{"payload":{"addr":"00:11:22:33:44:55"},"confirm":false}
```

Example response:
```json
{"command":"network/bluetooth/unpair","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

Errors: `400`, `403`, `409`, `429`.

---

#### `POST /gps/restart`
Example request:
```json
{"payload":{},"confirm":true}
```

Example response:
```json
{"command":"gps/restart","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

Errors: `400`, `403`, `409`, `429`.

---

#### `POST /esp32/buzzer`
Payload fields: `mode` (`on|off|beep`), `duration_ms` (optional), `pattern` (optional)

Example request:
```json
{"payload":{"mode":"beep","duration_ms":200},"confirm":false}
```

Example response:
```json
{"command":"esp32/buzzer","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

Errors: `400`, `409`, `429`.

---

#### `POST /esp32/leds`
Payload fields: `red`/`yellow`/`green` booleans, `pattern` (optional)

Example request:
```json
{"payload":{"red":false,"yellow":false,"green":true},"confirm":false}
```

Example response:
```json
{"command":"esp32/leds","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

Errors: `400`, `409`, `429`.

---

#### `POST /esp32/buttons/simulate` (local-only)
Payload fields: `button` string, `action` (`press|release`)

Example request:
```json
{"payload":{"button":"ack","action":"press"},"confirm":false}
```

Example response:
```json
{"command":"esp32/buttons/simulate","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

Errors: `400`, `403`, `409`, `429`.

---

#### `POST /esp32/config`
Payload fields: `config` object

Example request:
```json
{"payload":{"config":{"scan_step_hz":2000000}},"confirm":false}
```

Example response:
```json
{"command":"esp32/config","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

Errors: `400`, `409`, `429`.

---

#### `POST /antsdr/sweep/start`
Payload fields: `plan` string

Example request:
```json
{"payload":{"plan":"analog_5g8"},"confirm":false}
```

Example response:
```json
{"command":"antsdr/sweep/start","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

Errors: `400`, `403`, `409`, `429`.

---

#### `POST /antsdr/sweep/stop`
Example request:
```json
{"payload":{},"confirm":false}
```

Example response:
```json
{"command":"antsdr/sweep/stop","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

Errors: `400`, `409`, `429`.

---

#### `POST /antsdr/gain/set`
Payload fields: `mode` (`manual|auto`), `gain_db` (required for manual)

Example request:
```json
{"payload":{"mode":"manual","gain_db":10.0},"confirm":false}
```

Example response:
```json
{"command":"antsdr/gain/set","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

Errors: `400`, `409`, `429`.

---

#### `POST /antsdr/device/reset` (dangerous)
Example request:
```json
{"payload":{},"confirm":true}
```

Example response:
```json
{"command":"antsdr/device/reset","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

Errors: `400`, `403`, `429`.

---

#### `POST /remote_id/monitor/start`
Example request:
```json
{"payload":{},"confirm":false}
```

Example response:
```json
{"command":"remote_id/monitor/start","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

Errors: `400`, `409`, `429`.

---

#### `POST /remote_id/monitor/stop`
Example request:
```json
{"payload":{},"confirm":false}
```

Example response:
```json
{"command":"remote_id/monitor/stop","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

Errors: `400`, `409`, `429`.

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
{"payload":{"dwell_ms":200,"step_hz":2000000,"start_hz":5645000000,"stop_hz":5865000000},"confirm":false}
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
{"payload":{},"confirm":false}
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
{"payload":{"ch":2},"confirm":false}
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
{"payload":{},"confirm":true}
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
{"payload":{},"confirm":true}
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
Liveness requirement: clients should receive **>=3 messages within 10 seconds** (e.g., SYSTEM_UPDATE + HEARTBEATs).

Example envelope:
```json
{"type":"SYSTEM_UPDATE","timestamp_ms":1700000000000,"source":"aggregator","data":{"timestamp_ms":1700000000000,"contacts":[]}}
```

Event types (full catalog in `docs/WEBSOCKET_EVENTS.md`):
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
- `gps` object
- `audio` object

Example response:
```json
{
  "timestamp_ms": 1700000000000,
  "system": {"status":"ok","uptime_s":1234},
  "ups": {"status":"ok","soc_percent":78,"state":"DISCHARGING"},
  "services": [],
  "network": {"wifi":{"timestamp_ms":1700000000000,"enabled":true,"connected":true,"ssid":"MyWiFi","ip":"192.168.1.100"},"bluetooth":{"timestamp_ms":1700000000000,"enabled":false,"scanning":false,"paired_count":0,"connected_devices":[]}},
  "gps": {"timestamp_ms":1700000000000,"fix":"NO_FIX","satellites":{"in_view":0,"in_use":0},"last_update_ms":1700000000000,"source":"gpsd"},
  "audio": {"timestamp_ms":1700000000000,"status":"ok","volume_percent":60,"muted":false}
}
```


---

### `GET /system`
Response fields:
- `timestamp_ms` integer
- `status` string (`ok|degraded|offline`)
- `uptime_s` integer
- `version` object `{app, git_sha?, build_ts?}`
- `cpu` object `{temp_c, load1, load5, load15, usage_percent?}`
- `ram` object `{total_mb, used_mb, free_mb}`
- `storage` object `{root:{total_gb, used_gb, free_gb}, logs?:{total_gb, used_gb, free_gb}}`
- `last_error` string (optional)

Example response:
```json
{"timestamp_ms":1700000000000,"status":"ok","uptime_s":1234,"version":{"app":"ndefender-system-controller","git_sha":"dev","build_ts":1700000000000},"cpu":{"temp_c":45.2,"load1":0.2,"load5":0.3,"load15":0.4},"ram":{"total_mb":4096,"used_mb":512,"free_mb":3584},"storage":{"root":{"total_gb":117,"used_gb":70,"free_gb":47}}}
```

---

### `GET /ups`
Response fields:
- `pack_voltage_v`, `current_a`, `input_vbus_v`, `input_power_w`
- `soc_percent`, `time_to_empty_s`, `time_to_full_s`
- `per_cell_v`, `state`

Example response:
```json
{"timestamp_ms":1700000000000,"status":"ok","pack_voltage_v":12.4,"current_a":1.2,"soc_percent":78,"state":"DISCHARGING","per_cell_v":[4.1,4.1,4.1]}
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
{"payload":{},"confirm": true}
```

Response:
```json
{"type":"COMMAND_ACK","timestamp_ms":1700000000000,"data":{"command":"service_restart","name":"ndefender-system-controller","ok":true,"reason":null}}
```

Cooldown: **10s**.
Errors: `400`, `403`, `429`.

---

### `GET /network` (summary)
Response fields:
- `connected`, `ssid`, `ip_v4`, `ip_v6`

Example response:
```json
{"connected":true,"ssid":"MyWiFi","ip_v4":"192.168.1.100","ip_v6":"fe80::1"}
```

---

### `GET /network/wifi/state`
Response fields: `timestamp_ms`, `enabled`, `connected`, `ssid`, `bssid?`, `ip?`, `rssi_dbm?`, `link_quality?`, `last_update_ms`, `last_error?`

Example response:
```json
{"timestamp_ms":1700000000000,"enabled":true,"connected":true,"ssid":"MyWiFi","ip":"192.168.1.100","last_update_ms":1700000000000}
```

---

### `GET /network/wifi/scan`
Response fields: `timestamp_ms`, `networks` array

Example response:
```json
{"timestamp_ms":1700000000000,"networks":[{"ssid":"MyWiFi","bssid":"aa:bb:cc:dd:ee:ff","security":"wpa2","signal_dbm":-48,"channel":11,"frequency_mhz":2462,"known":true}]}
```

---

### `GET /network/bluetooth/state`
Response fields: `timestamp_ms`, `enabled`, `scanning`, `paired_count`, `connected_devices`, `last_update_ms`, `last_error?`

Example response:
```json
{"timestamp_ms":1700000000000,"enabled":false,"scanning":false,"paired_count":0,"connected_devices":[],"last_update_ms":1700000000000}
```

---

### `GET /network/bluetooth/devices`
Response fields: `timestamp_ms`, `devices` array

Example response:
```json
{"timestamp_ms":1700000000000,"devices":[{"addr":"00:11:22:33:44:55","name":"Headset","paired":true,"connected":false}]}
```

---

### `GET /gps`
Response fields: `timestamp_ms`, `fix`, `satellites`, `latitude`, `longitude`, `altitude_m`, `speed_m_s`, `heading_deg`, `last_update_ms`, `age_ms?`, `source`, `last_error?`

Example response:
```json
{"timestamp_ms":1700000000000,"fix":"NO_FIX","satellites":{"in_view":0,"in_use":0},"last_update_ms":1700000000000,"source":"gpsd"}
```

---

### `GET /audio`
Response fields: `timestamp_ms`, `status`, `volume_percent`, `muted`, `last_error?`

Example response:
```json
{"timestamp_ms":1700000000000,"status":"ok","volume_percent":60,"muted":false}
```

---

### `POST /audio/mute`
Request body:
```json
{"payload":{"muted":true},"confirm":false}
```

Response:
```json
{"type":"COMMAND_ACK","timestamp_ms":1700000000000,"data":{"command":"audio/mute","ok":true,"reason":null}}
```

Errors: `400`, `409`, `429`.

---

### `POST /audio/volume`
Request body:
```json
{"payload":{"volume_percent":50},"confirm":false}
```

Response:
```json
{"type":"COMMAND_ACK","timestamp_ms":1700000000000,"data":{"command":"audio/volume","ok":true,"reason":null}}
```

Errors: `400`, `409`, `429`.

---

### `POST /network/wifi/enable`
Request body:
```json
{"payload":{"enabled":true},"confirm":false}
```

Response:
```json
{"type":"COMMAND_ACK","timestamp_ms":1700000000000,"data":{"command":"network/wifi/enable","ok":true,"reason":null}}
```

Errors: `400`, `403`, `409`, `429`.

---

### `POST /network/wifi/connect`
Request body:
```json
{"payload":{"ssid":"MyWiFi","password":"secret","hidden":false},"confirm":false}
```

Response:
```json
{"type":"COMMAND_ACK","timestamp_ms":1700000000000,"data":{"command":"network/wifi/connect","ok":true,"reason":null}}
```

Errors: `400`, `403`, `409`, `429`.

---

### `POST /network/wifi/disconnect`
Request body:
```json
{"payload":{},"confirm":false}
```

Response:
```json
{"type":"COMMAND_ACK","timestamp_ms":1700000000000,"data":{"command":"network/wifi/disconnect","ok":true,"reason":null}}
```

Errors: `400`, `409`, `429`.

---

### `POST /network/bluetooth/enable`
Request body:
```json
{"payload":{"enabled":true},"confirm":false}
```

Response:
```json
{"type":"COMMAND_ACK","timestamp_ms":1700000000000,"data":{"command":"network/bluetooth/enable","ok":true,"reason":null}}
```

Errors: `400`, `403`, `409`, `429`.

---

### `POST /network/bluetooth/scan/start`
Request body:
```json
{"payload":{},"confirm":false}
```

Response:
```json
{"type":"COMMAND_ACK","timestamp_ms":1700000000000,"data":{"command":"network/bluetooth/scan/start","ok":true,"reason":null}}
```

Errors: `400`, `409`, `429`.

---

### `POST /network/bluetooth/scan/stop`
Request body:
```json
{"payload":{},"confirm":false}
```

Response:
```json
{"type":"COMMAND_ACK","timestamp_ms":1700000000000,"data":{"command":"network/bluetooth/scan/stop","ok":true,"reason":null}}
```

Errors: `400`, `409`, `429`.

---

### `POST /network/bluetooth/pair`
Request body:
```json
{"payload":{"addr":"00:11:22:33:44:55","pin":"0000"},"confirm":false}
```

Response:
```json
{"type":"COMMAND_ACK","timestamp_ms":1700000000000,"data":{"command":"network/bluetooth/pair","ok":true,"reason":null}}
```

Errors: `400`, `403`, `409`, `429`.

---

### `POST /network/bluetooth/unpair`
Request body:
```json
{"payload":{"addr":"00:11:22:33:44:55"},"confirm":false}
```

Response:
```json
{"type":"COMMAND_ACK","timestamp_ms":1700000000000,"data":{"command":"network/bluetooth/unpair","ok":true,"reason":null}}
```

Errors: `400`, `403`, `409`, `429`.

---

### `POST /gps/restart`
Request body:
```json
{"payload":{},"confirm":true}
```

Response:
```json
{"type":"COMMAND_ACK","timestamp_ms":1700000000000,"data":{"command":"gps/restart","ok":true,"reason":null}}
```

Errors: `400`, `403`, `409`, `429`.

---

### `POST /system/reboot`
Request body:
```json
{"payload":{},"confirm": true}
```

Response:
```json
{"type":"COMMAND_ACK","timestamp_ms":1700000000000,"data":{"command":"system/reboot","ok":true,"reason":null}}
```

Cooldown: **30s**.
Requires `NDEFENDER_ALLOW_UNSAFE=true`.
Errors: `400`, `403`, `429`.

---

### `POST /system/shutdown`
Same as reboot.

Example request:
```json
{"payload":{},"confirm": true}
```

Example response:
```json
{"type":"COMMAND_ACK","timestamp_ms":1700000000000,"data":{"command":"system/shutdown","ok":true,"reason":null}}
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
- `timestamp_ms` integer
- `frames_processed` integer
- `detections_processed` integer
- `events_emitted` integer
- `last_event_timestamp_ms` integer (optional)
- `noise_floor_db` number (optional)
- `peaks` integer (optional)
- `last_error` string (optional)

Example response:
```json
{"timestamp_ms":1700000000000,"frames_processed":10,"detections_processed":23,"events_emitted":5}
```

### `GET /device`
Response fields:
- `timestamp_ms` integer
- `connected` boolean
- `uri` string (optional)
- `temperature_c` number (optional)
- `last_error` string (optional)

Example response:
```json
{"timestamp_ms":1700000000000,"connected":false,"last_error":"antsdr_unreachable"}
```

### `GET /sweep/state`
Response fields:
- `timestamp_ms` integer
- `running` boolean
- `active_plan` string (optional)
- `plans` array of `{name,start_hz,end_hz,step_hz}`
- `last_update_ms` integer
- `last_error` string (optional)

Example response:
```json
{"timestamp_ms":1700000000000,"running":false,"plans":[{"name":"analog_5g8","start_hz":5645000000,"end_hz":5865000000,"step_hz":2000000}],"last_update_ms":1700000000000}
```

### `GET /gain`
Response fields:
- `timestamp_ms` integer
- `mode` string (`manual|auto`)
- `gain_db` number (optional)
- `limits` object `{min_db,max_db}` (optional)

Example response:
```json
{"timestamp_ms":1700000000000,"mode":"auto"}
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

### `POST /sweep/start`
Request:
```json
{"payload":{"plan":"analog_5g8"},"confirm":false}
```

Response:
```json
{"command":"sweep/start","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

Errors: `400`, `403`, `409`, `429`.

### `POST /sweep/stop`
Request:
```json
{"payload":{},"confirm":false}
```

Response:
```json
{"command":"sweep/stop","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

Errors: `400`, `409`, `429`.

### `POST /gain/set`
Request:
```json
{"payload":{"mode":"manual","gain_db":10.0},"confirm":false}
```

Response:
```json
{"command":"gain/set","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

Errors: `400`, `409`, `429`.

### `POST /device/reset` (dangerous)
Request:
```json
{"payload":{},"confirm":true}
```

Response:
```json
{"command":"device/reset","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

Errors: `400`, `403`, `429`.

### `POST /device/calibrate` (dangerous)
Request:
```json
{"payload":{"kind":"rf_dc"},"confirm":true}
```

Response:
```json
{"command":"device/calibrate","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

Errors: `400`, `403`, `429`.

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
{"events":[{"type":"RF_CONTACT_NEW","timestamp_ms":1700000000000,"source":"antsdr","data":{"id":"rf:5658000000","freq_hz":5658000000}}]}
```

### `WS /events`
- Enforces `api.max_clients` limit; returns `429` if exceeded.

Envelope:
```json
{"type":"RF_CONTACT_UPDATE","timestamp_ms":1700000000000,"source":"antsdr","data":{"id":"rf:5658000000","freq_hz":5658000000}}
```

---

## 🛰️ RemoteID Engine Local API
**Base URL:** `/api/v1`

Common errors:
- `404` Not found for unknown endpoints

### `GET /status`
Response fields:
- `timestamp_ms` integer
- `state` string (`ok|degraded|offline|replay`)
- `mode` string (`live|replay|off`)
- `capture_active` boolean
- `contacts_active` integer
- `last_update_ms` integer
- `health` object `{ok,last_error?}`
- `stats` object `{frames,decoded,dropped?,dedupe_hits?}` (optional)

Example response:
```json
{"timestamp_ms":1700000000000,"state":"ok","mode":"live","capture_active":true,"contacts_active":1,"last_update_ms":1700000000000,"health":{"ok":true},"stats":{"frames":10,"decoded":2}}
```

### `GET /health`
Same response as `/status`.

### `GET /contacts`
Response:
```json
{"timestamp_ms":1700000000000,"contacts":[{"id":"rid:123","type":"REMOTE_ID","source":"remoteid","last_seen_ts":1700000000000,"severity":"unknown","lat":23.0,"lon":72.0}]}
```

### `GET /stats`
Response:
```json
{"timestamp_ms":1700000000000,"frames":10,"decoded":2,"dropped":0,"dedupe_hits":1}
```

### `GET /replay/state`
Response:
```json
{"timestamp_ms":1700000000000,"active":false,"source":"none","state":"stopped"}
```

### `POST /replay/start`
Request:
```json
{"payload":{"source":"/opt/ndefender/logs/remoteid.jsonl","interval_ms":1000,"loop":true},"confirm":false}
```

Response:
```json
{"command":"replay/start","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

### `POST /replay/stop`
Request:
```json
{"payload":{},"confirm":false}
```

Response:
```json
{"command":"replay/stop","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

### `POST /monitor/start`
Request:
```json
{"payload":{},"confirm":false}
```

Response:
```json
{"command":"monitor/start","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

### `POST /monitor/stop`
Request:
```json
{"payload":{},"confirm":false}
```

Response:
```json
{"command":"monitor/stop","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

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
