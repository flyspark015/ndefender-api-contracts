# Observability API

Base: `/api/v1`

## Error Body
```json
{"detail":"<reason>"}
```

## GET /health
**Purpose**: liveness for observability service.
Request: none.
Response (200):
```json
{"status":"ok"}
```

Errors: `500`

## GET /health/detail
**Purpose**: detailed health summary.
Request: none.
Response (200):
```json
{"generated_ts":1700000000000,"subsystems":[],"status":"ok"}
```

Errors: `500`

## GET /status
**Purpose**: aggregated subsystem status.
Request: none.
Response (200):
```json
{"generated_ts":1700000000000,"overall_state":"OK","state_counts":{"OK":1},"subsystems":[]}
```

Errors: `500`

## GET /version
**Purpose**: build/version info.
Request: none.
Response (200):
```json
{"version":"1.0.0","git_sha":"deadbeef"}
```

Errors: `500`

## GET /config
**Purpose**: sanitized runtime config.
Request: none.
Response (200): sanitized config.

Errors: `403`, `500`

## GET /metrics
**Purpose**: Prometheus metrics.
Request: none.
Prometheus exposition.

Response: `text/plain` (Prometheus format).

Errors: `500`

## POST /diag/bundle
**Purpose**: generate diagnostics bundle (local-only).
Request: none.
Local-only diagnostics bundle.

Errors: `403`, `429`, `500`

## Curl Examples
```bash
export BASE_URL=http://127.0.0.1:8100/api/v1

curl -sS $BASE_URL/health
curl -sS $BASE_URL/health/detail
curl -sS $BASE_URL/status
curl -sS $BASE_URL/version
curl -sS $BASE_URL/config
curl -sS $BASE_URL/metrics

curl -sS -X POST $BASE_URL/diag/bundle
```
