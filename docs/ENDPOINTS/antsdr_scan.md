# AntSDR Scan API

Base: `/api/v1`

## Error Body (aiohttp)
```json
{"error":{"code":"<code>","message":"<message>"}}
```

Common errors:
- `404` Not found
- `409` Conflict
- `429` Too many clients (WebSocket)

## GET /health
**Purpose**: liveness and scan state.
Request: none.
Response (200):
```json
{"status":"ok","engine_running":true,"ws_backend_connected":false,"last_event_timestamp_ms":1700000000000,"timestamp_ms":1700000000000}
```

Errors: `404`

## GET /version
**Purpose**: build/version info.
Request: none.
Response (200):
```json
{"version":"1.0.0"}
```
Errors: `404`

## GET /stats
**Purpose**: processing counters.
Request: none.
Response (200):
```json
{"frames_processed":10,"detections_processed":23,"events_emitted":5}
```
Errors: `404`

## GET /config
**Purpose**: read current config.
Request: none.
Response (200): radio/tracker/detector/sweep/ws/classification/api.
Errors: `404`

## POST /config/reload
**Purpose**: reload config from disk.
Request: none.
Response (200):
```json
{"status":"ok"}
```

Errors: `404`, `409` if scan running.

## POST /run/start
**Purpose**: start scan.
Request: none.
Errors: `404`, `409` if already running.

## POST /run/stop
**Purpose**: stop scan.
Request: none.
Errors: `404`, `409` if not running.

## POST /run/replay
**Purpose**: replay JSONL log.
Request:
```json
{"log_path":"/opt/ndefender/logs/antsdr_scan.jsonl","output_path":"/tmp/replay.jsonl","max_events":100}
```
Errors: `400`, `404`, `409`.

## GET /events/last?limit=N
**Purpose**: fetch recent RF events.
Request: none.
Response (200):
```json
{"events":[{"type":"RF_CONTACT_NEW","timestamp_ms":1700000000000,"source":"antsdr","data":{"id":"rf:5658000000","freq_hz":5658000000}}]}
```
Errors: `404`

Notes:
- `timestamp_ms` is epoch ms.

## WS /events
**Purpose**: live RF event stream.
Request: WS upgrade (no request body).
RF event stream; enforces `api.max_clients` and returns `429` if exceeded.
Errors: `429`

## Curl Examples
```bash
export BASE_URL=http://127.0.0.1:8890/api/v1

curl -sS $BASE_URL/health
curl -sS $BASE_URL/version
curl -sS $BASE_URL/stats
curl -sS $BASE_URL/config
curl -sS -X POST $BASE_URL/config/reload
curl -sS -X POST $BASE_URL/run/start
curl -sS -X POST $BASE_URL/run/stop
curl -sS -X POST $BASE_URL/run/replay \
  -H "Content-Type: application/json" \
  -d '{"log_path":"/opt/ndefender/logs/antsdr_scan.jsonl","output_path":"/tmp/replay.jsonl","max_events":100}'
curl -sS "$BASE_URL/events/last?limit=50"
```
