# CONTRACT GAPS

This file documents runtime behaviors that are **not yet formalized** in the canonical contract. Each entry includes a backward-compatible fix plan.

## 1) HELLO WS Event
**Where it appears**:
- Backend Aggregator WS (`/api/v1/ws`) may emit `HELLO` immediately on connect.

**Why needed**:
- Lightweight connection acknowledgment for clients and diagnostics.

**Fix plan (backward-compatible)**:
1. Add `HELLO` to `docs/WEBSOCKET_EVENTS.md` catalog.
2. Add example in `docs/ALL_IN_ONE_API.md` WS section.
3. No schema change required (EventEnvelope already allows any `type`).

## 2) HEARTBEAT WS Event
**Where it appears**:
- Backend Aggregator WS (`/api/v1/ws`) emits periodic `HEARTBEAT` messages to keep UI live.

**Why needed**:
- Ensures clients receive at least 3 messages per 10 seconds even when state is static.

**Fix plan (backward-compatible)**:
1. Add `HEARTBEAT` to `docs/WEBSOCKET_EVENTS.md` catalog (already noted as gap).
2. Add example in `docs/ALL_IN_ONE_API.md` WS section.
3. No schema change required (EventEnvelope already allows any `type`).

## 3) StatusSnapshot Runtime Extras
**Where it appears**:
- Backend Aggregator `/api/v1/status` returns additional fields used by UI:
  - `fpv`
  - `overall_ok`
  - `system.status`, `power.status`, `network.status`, `audio.status`
  - `rf.status`, `rf.last_error`, `rf.scan_active`
  - `remote_id.last_error`, `remote_id.capture_active`
  - `video.status`

**Why needed**:
- UI must display explicit offline/degraded states; no empty blocks.

**Fix plan (backward-compatible)**:
1. Update `schemas/StatusSnapshot.json` to include these fields as optional (additive).
2. Update OpenAPI to reference the new schema.
3. Update ALL_IN_ONE_API.md examples and field lists (done in this repo).

## 4) Contact `last_seen_uptime_ms`
**Where it appears**:
- ESP32 telemetry uses uptime-based timestamps; backend preserves them in contacts.

**Why needed**:
- Distinguishes epoch timestamps from device uptime and avoids ambiguity.

**Fix plan (backward-compatible)**:
1. Add optional `last_seen_uptime_ms` to `schemas/Contact.json`.
2. Document in ALL_IN_ONE_API.md and Contact model.
3. Keep `last_seen_ts` as epoch ms for UI display.

## 5) Legacy `timestamp` in JSONL Producers
**Where it appears**:
- Some JSONL producers may emit `timestamp` instead of `timestamp_ms` (legacy).

**Why needed**:
- Public contract requires `timestamp_ms` everywhere; legacy producers must be normalized before exposure.

**Fix plan (backward-compatible)**:
1. Normalize JSONL `timestamp` to `timestamp_ms` at ingestion time.
2. Reject or flag any public REST/WS payload that still contains `timestamp`.
