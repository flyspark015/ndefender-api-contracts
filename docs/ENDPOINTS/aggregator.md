# Backend Aggregator API

Base: `/api/v1`

## Error Body
FastAPI errors use:
```json
{"detail":"<reason>"}
```

## GET /health
**Purpose**: liveness.
Request: none.

Response (200):
```json
{"status":"ok","timestamp_ms":1700000000000}
```

Errors: `500`

## GET /status
**Purpose**: full snapshot for UI.
Request: none.

Response (200):
```json
{
  "timestamp_ms": 1700000000000,
  "system": {"status":"degraded","cpu_temp_c":36.9,"cpu_usage_percent":15.8,"ram_used_mb":1931,"ram_total_mb":16215,"disk_used_gb":70,"disk_total_gb":117,"uptime_s":4671},
  "power": {"status":"ok","pack_voltage_v":16.62,"current_a":-0.01,"soc_percent":98,"state":"IDLE"},
  "rf": {"status":"offline","last_error":"antsdr_unreachable","scan_active":false,"last_event_type":"RF_SCAN_OFFLINE","last_timestamp_ms":1700000000000,"last_event":{"reason":"antsdr_unreachable"}},
  "remote_id": {"state":"DEGRADED","mode":"live","capture_active":true,"last_error":"no_odid_frames","last_event_type":"REMOTEID_STALE","last_timestamp_ms":1700000000000,"last_event":{"reason":"no_odid_frames"}},
  "vrx": {"selected":1,"scan_state":"idle","vrx":[{"id":1,"freq_hz":5740000000,"rssi_raw":632}]},
  "fpv": {"selected":1,"scan_state":"idle","freq_hz":5740000000,"rssi_raw":632},
  "video": {"selected":1,"status":"ok"},
  "services": [{"name":"ndefender-backend","active_state":"active","sub_state":"running","restart_count":0}],
  "network": {"status":"ok","connected":true,"ip_v4":"192.168.1.35","ssid":"example"},
  "audio": {"status":"ok","muted":false,"volume_percent":100},
  "contacts": [],
  "replay": {"active":false,"source":"none"},
  "overall_ok": false
}
```

Errors: `500`

## GET /contacts
**Purpose**: unified contacts list.
Request: none.

Response (200):
```json
{"contacts":[{"id":"rf:5658000000","type":"RF","source":"antsdr","last_seen_ts":1700000000000,"severity":"high","freq_hz":5658000000}]}
```

Errors: `500`

## GET /system
**Purpose**: system stats (mirrors System Controller).
Request: none.

Response (200):
```json
{"cpu_temp_c":45.2,"cpu_usage_percent":12.5,"ram_used_mb":410,"disk_used_gb":12,"status":"ok"}
```

Errors: `500`

## GET /power
**Purpose**: UPS telemetry.
Request: none.

Response (200):
```json
{"pack_voltage_v":12.4,"current_a":1.2,"soc_percent":78,"state":"DISCHARGING","status":"ok"}
```

Errors: `500`

## GET /rf
**Purpose**: RF ingest state.
Request: none.

Response (200):
```json
{"last_event_type":"RF_SCAN_OFFLINE","last_event":{"reason":"antsdr_unreachable"},"last_timestamp_ms":1700000000000,"scan_active":false,"status":"offline","last_error":"antsdr_unreachable"}
```

Errors: `500`

## GET /video
**Purpose**: video selection state.
Request: none.

Response (200):
```json
{"selected":2,"status":"ok"}
```

Errors: `500`

## GET /services
**Purpose**: systemd service status.
Request: none.

Response (200):
```json
[{"name":"ndefender-system-controller","active_state":"active","sub_state":"running","restart_count":1}]
```

Errors: `500`

## GET /network
**Purpose**: network state.
Request: none.

Response (200):
```json
{"connected":true,"ssid":"MyWiFi","ip_v4":"192.168.1.100","ip_v6":"fe80::1","status":"ok"}
```

Errors: `500`

## GET /audio
**Purpose**: audio state.
Request: none.

Response (200):
```json
{"volume_percent":60,"muted":false,"status":"ok"}
```

Errors: `500`

## Command Endpoints
All command endpoints accept:
```json
{"payload":{},"confirm":false}
```

Response (200):
```json
{"command":"vrx/tune","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```

Rate limits:
- `10/min` commands
- `2/min` dangerous

### POST /vrx/tune
**Purpose**: tune a VRX channel to a frequency.
Payload:
- `vrx_id` integer
- `freq_hz` integer (Hz)

Errors: `403`, `429`, `500`

### POST /scan/start
**Purpose**: start RF scan sweep.
Payload:
- `dwell_ms` integer
- `step_hz` integer
- `start_hz` integer
- `stop_hz` integer

Errors: `403`, `429`, `500`

### POST /scan/stop
**Purpose**: stop RF scan.
Payload:
- empty `{}`

Errors: `403`, `429`, `500`

### POST /video/select
**Purpose**: select active video channel.
Payload:
- `ch` integer

Errors: `403`, `429`, `500`

### POST /system/reboot
**Purpose**: reboot host (dangerous).
Requirements:
- `confirm=true`
- unsafe enabled

Errors: `400`, `403`, `429`, `500`

### POST /system/shutdown
**Purpose**: shutdown host (dangerous).
Same requirements as reboot.

Errors: `400`, `403`, `429`, `500`

## WS /api/v1/ws
See `docs/ENDPOINTS/websocket.md`.

## Curl Examples
```bash
export BASE_URL=http://127.0.0.1:8001/api/v1

curl -sS $BASE_URL/health
curl -sS $BASE_URL/status
curl -sS $BASE_URL/contacts
curl -sS $BASE_URL/system
curl -sS $BASE_URL/power
curl -sS $BASE_URL/rf
curl -sS $BASE_URL/video
curl -sS $BASE_URL/services
curl -sS $BASE_URL/network
curl -sS $BASE_URL/audio

curl -sS -X POST $BASE_URL/vrx/tune \
  -H "Content-Type: application/json" \
  -d '{"payload":{"vrx_id":1,"freq_hz":5740000000},"confirm":false}'

curl -sS -X POST $BASE_URL/scan/start \
  -H "Content-Type: application/json" \
  -d '{"payload":{"dwell_ms":50,"step_hz":2000000,"start_hz":5725000000,"stop_hz":5885000000},"confirm":false}'

curl -sS -X POST $BASE_URL/scan/stop \
  -H "Content-Type: application/json" \
  -d '{"payload":{},"confirm":false}'

curl -sS -X POST $BASE_URL/video/select \
  -H "Content-Type: application/json" \
  -d '{"payload":{"ch":1},"confirm":false}'

curl -sS -X POST $BASE_URL/system/reboot \
  -H "Content-Type: application/json" \
  -d '{"payload":{},"confirm":true}'

curl -sS -X POST $BASE_URL/system/shutdown \
  -H "Content-Type: application/json" \
  -d '{"payload":{},"confirm":true}'
```
