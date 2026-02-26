# AntSDR Scan Endpoints

Base: `/api/v1`

## Read Endpoints
- `GET /health`
- `GET /version`
- `GET /stats`
- `GET /device`
- `GET /sweep/state`
- `GET /gain`
- `GET /config`
- `GET /events/last?limit=N`

## Write/Command Endpoints
- `POST /config/reload`
- `POST /sweep/start`
- `POST /sweep/stop`
- `POST /gain/set`
- `POST /device/reset` (dangerous)
- `POST /device/calibrate` (dangerous)
- Legacy: `POST /run/start`, `/run/stop`, `/run/replay`

## WebSocket
- `WS /events`
- Envelope: `{type,timestamp_ms,source,data}`

See `docs/ALL_IN_ONE_API.md` for full schemas and examples.
