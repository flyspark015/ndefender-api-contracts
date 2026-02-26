# TX/RX Flows (Snapshot + WS)

## Recommended Client Flow
1. Fetch snapshot: `GET /api/v1/status` (authoritative).
2. Connect WS: `WS /api/v1/ws`.
3. Apply incremental updates.
4. On disconnect, re-fetch snapshot and reconnect.

## Merge Rules
- `SYSTEM_UPDATE`: full overwrite of cached state.
- `CONTACT_*` and `RF_CONTACT_*`: incremental updates.
- `COMMAND_ACK`: render action feedback.

## Reconnect Strategy
- Exponential backoff (1s, 2s, 5s, 10s).
- Always re-fetch snapshot after reconnect.

## Liveness Requirement
- WS streams should emit **≥3 messages within 10 seconds**.
- Backend Aggregator should send `HELLO` (contract gap) + `SYSTEM_UPDATE` immediately, then periodic liveness events.
- `HEARTBEAT` is currently a **CONTRACT GAP** if used; see `docs/CONTRACT_GAPS.md`.

## ID Stability Rules
- Contact `id` must remain stable across updates.
- `last_seen_ts` is epoch ms.

## CONTRACT GAP
- Runtime may emit WS `HEARTBEAT` events for liveness. See `docs/CONTRACT_GAPS.md`.
