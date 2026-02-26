# Contract Gaps (Active)

This file lists **known runtime behaviors** that are not yet fully formalized in the canonical contract and provides a backward-compatible path to align them.

## 1) ESP32 telemetry `timestamp_ms` is uptime-based
- **Where observed:** ESP32 serial telemetry payloads.
- **Why:** Device clocks are uptime-based; not synced to epoch.
- **Plan:** Keep `timestamp_ms` as uptime in ESP32 telemetry only; aggregator converts to epoch for `contacts.last_seen_ts` and keeps `last_seen_uptime_ms`.

## 2) System Controller HELLO log event
- **Where observed:** System Controller WS sends `LOG_EVENT` with `{ "message": "HELLO" }` on connect.
- **Why:** Operator visibility for WS init.
- **Plan:** Keep as optional `LOG_EVENT` payload; no client should depend on it.

## 3) HEARTBEAT event adoption (in progress)
- **Where observed:** Backend Aggregator WS uses `HEARTBEAT` for liveness.
- **Why:** Clients require >=3 WS messages/10s.
- **Plan:** Standardize `HEARTBEAT` in `WEBSOCKET_EVENTS.md` and keep it backward compatible (clients should ignore unknown types).

If additional gaps are discovered, add them here with a migration plan.
