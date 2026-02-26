# WebSocket Endpoints

## Backend Aggregator
- `WS /api/v1/ws`
- Envelope: `{type,timestamp_ms,source,data}`
- Must send >=3 messages / 10 seconds (SYSTEM_UPDATE + HEARTBEAT).

## System Controller
- `WS /api/v1/ws`
- Envelope: `{type,timestamp_ms,source,data}`

## AntSDR Scan
- `WS /api/v1/events`
- Envelope: `{type,timestamp_ms,source,data}`

See `docs/WEBSOCKET_EVENTS.md` for full event catalogs and examples.
