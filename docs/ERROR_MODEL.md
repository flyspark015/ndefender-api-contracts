# Error Model

## FastAPI Services
Applies to:
- Backend Aggregator
- System Controller
- Observability

Error body:
```json
{"detail":"<reason>"}
```

Common status codes:
- `400` invalid input / missing confirm
- `403` unsafe operations disabled or local-only
- `404` not found (default FastAPI)
- `409` invalid state (start/stop conflicts)
- `429` rate limit / cooldown
- `500` internal error

Retry guidance:
- `429` MAY include `Retry-After` header (seconds). Clients should back off accordingly.

## AntSDR Scan (aiohttp)
Error body:
```json
{"error":{"code":"<code>","message":"<message>"}}
```

## RemoteID Engine (embedded HTTP)
- Unknown endpoints return `404` with no JSON body.

## CONTRACT GAP
Correlation IDs are not defined. If needed, add optional `X-Request-Id` response header.
