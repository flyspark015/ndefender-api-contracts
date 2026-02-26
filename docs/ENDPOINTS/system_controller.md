# System Controller API

Base: `/api/v1`

## Error Body
```json
{"detail":"<reason>"}
```

## GET /health
**Purpose**: liveness.
Request: none.
Response (200):
```json
{"ok":true,"timestamp_ms":1700000000000,"version":"0.1.0"}
```

Errors: `500`

## GET /status
**Purpose**: full system snapshot (system + UPS + services + network + audio).
Request: none.
Response (200):
```json
{
  "timestamp_ms":1700000000000,
  "system":{"cpu_temp_c":45.2},
  "ups":{"soc_percent":78,"state":"DISCHARGING"},
  "services":[],
  "network":{"connected":true,"ip_v4":"192.168.1.100","ssid":"MyWiFi","status":"ok"},
  "audio":{"muted":false,"volume_percent":60,"status":"ok"}
}
```

Errors: `500`

## GET /system
**Purpose**: system stats.
Request: none.
Response (200): system stats.

Errors: `500`

## GET /ups
**Purpose**: UPS telemetry.
Request: none.
Response (200): UPS telemetry.

Errors: `500`

## GET /services
**Purpose**: systemd service list.
Request: none.
Response (200): service list.

Errors: `500`

## GET /network
**Purpose**: network status.
Request: none.
Response (200): network status.

Errors: `500`

## GET /audio
**Purpose**: audio status.
Request: none.
Response (200): audio status.

Errors: `500`

## POST /services/{name}/restart
**Purpose**: restart a named service (dangerous, rate-limited).
Request:
```json
{"confirm":true}
```

Response (200): `COMMAND_ACK` envelope.

Errors: `400`, `403`, `429`, `500`

Rate limits:
- Commands: `10/min`
- Dangerous commands: `2/min`

## POST /system/reboot
**Purpose**: reboot host (dangerous).
Requires `confirm=true` and unsafe enabled.
Request:
```json
{"confirm":true}
```

Errors: `400`, `403`, `429`, `500`

## POST /system/shutdown
**Purpose**: shutdown host (dangerous).
Requires `confirm=true` and unsafe enabled.
Request:
```json
{"confirm":true}
```

Errors: `400`, `403`, `429`, `500`

## Curl Examples
```bash
export BASE_URL=http://127.0.0.1:8002/api/v1

curl -sS $BASE_URL/health
curl -sS $BASE_URL/status
curl -sS $BASE_URL/system
curl -sS $BASE_URL/ups
curl -sS $BASE_URL/services
curl -sS $BASE_URL/network
curl -sS $BASE_URL/audio

curl -sS -X POST $BASE_URL/services/ndefender-backend/restart \
  -H "Content-Type: application/json" \
  -d '{"confirm":true}'

curl -sS -X POST $BASE_URL/system/reboot \
  -H "Content-Type: application/json" \
  -d '{"confirm":true}'

curl -sS -X POST $BASE_URL/system/shutdown \
  -H "Content-Type: application/json" \
  -d '{"confirm":true}'
```
