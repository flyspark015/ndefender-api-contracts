# WebSocket (Aggregator)

Endpoint: `WS /api/v1/ws`
**Purpose**: live event stream (SYSTEM_UPDATE + incremental updates).
Request: WS upgrade (no request body).

Envelope:
```json
{"type":"SYSTEM_UPDATE","timestamp_ms":1700000000000,"source":"aggregator","data":{}}
```

Event types:
- `HELLO` *(CONTRACT GAP)*
- `HEARTBEAT` *(CONTRACT GAP)*
- `SYSTEM_UPDATE`
- `COMMAND_ACK`
- `ESP32_TELEMETRY`
- `LOG_EVENT`
- `CONTACT_NEW`, `CONTACT_UPDATE`, `CONTACT_LOST`
- `RF_CONTACT_NEW`, `RF_CONTACT_UPDATE`, `RF_CONTACT_LOST`
- `TELEMETRY_UPDATE`, `REPLAY_STATE`

## Liveness Requirement
- Clients/tests expect **≥3 messages within 10 seconds**.
- `HELLO` + `SYSTEM_UPDATE` should be sent on connect.
- `HEARTBEAT` is allowed only as a documented **CONTRACT GAP**.

## CONTRACT GAP
- `HEARTBEAT` is emitted by runtime for liveness but not yet formalized. See `docs/CONTRACT_GAPS.md`.
- `HELLO` may be emitted on connect for acknowledgement. See `docs/CONTRACT_GAPS.md`.

## WS Client Example
```bash
python3 examples/ws_client.py --url ws://127.0.0.1:8001/api/v1/ws
```
