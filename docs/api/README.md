# API Reference (Deep Dive)

This document is a **deep‑dive guide** for integration teams. The single source of truth remains `README.md`.

## Canonical Entry Points
- Contract: `../ALL_IN_ONE_API.md`
- OpenAPI: `../OPENAPI.yaml`
- API index: `../../README.md` (API Index section)
- WS catalog: `../WEBSOCKET_EVENTS.md`

## Usage Pattern (RX → TX)
1) `GET /api/v1/status`
2) `WS /api/v1/ws`
3) Apply incremental updates (`SYSTEM_UPDATE`, `CONTACT_*`, `TELEMETRY_UPDATE`, `REPLAY_STATE`)
4) Issue commands with `{payload, confirm}` and wait for `COMMAND_ACK`

## Error Model (FastAPI)
```json
{"detail":"<reason>"}
```
Common reasons:
- `confirm_required`
- `validation_error`
- `service_unavailable`
- `upstream_timeout`
- `invalid_state`

## Confirm‑Gating
Dangerous commands require a two‑step flow:
1) First request with `confirm=false` → HTTP 400 `{"detail":"confirm_required"}`
2) Second request with `confirm=true` → success

## WebSocket Guidance
- Envelope: `{type,timestamp_ms,source,data}`
- Liveness: >=3 messages in 10 seconds
- Reconnect: exponential backoff; refresh `/api/v1/status` after reconnect

## UI/AI Integration
- Always render `/api/v1/status` first.
- Never assume WS completeness; WS is incremental.
- Use `timestamp_ms` and `last_update_ms` for stale detection.

## Endpoint Coverage
The endpoint list is intentionally **only** in `README.md` to avoid drift.
Refer to the API Index and per‑endpoint examples there.
