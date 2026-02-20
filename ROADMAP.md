# N-Defender API Contracts Roadmap

Goal: Build a single-source-of-truth contracts repository for the unified N-Defender system API (REST + WebSocket), with schemas, examples, types, OpenAPI, and validation.

## Steps
1. ✅ Step 1 — Bootstrap repo structure + ROADMAP.md + progress.md
2. 🟡 Step 2 — Extract contracts from each source repo; list sources + file paths; create unified model map
3. 🟡 Step 3 — Write `docs/ALL_IN_ONE_API.md` fully
4. 🟡 Step 4 — Write `docs/WEBSOCKET_EVENTS.md` fully
5. 🟡 Step 5 — Generate `schemas/` JSON Schema and validate
6. 🟡 Step 6 — Generate `types/contracts.ts` matching schemas
7. 🟡 Step 7 — Generate `docs/OPENAPI.yaml` and validate best-effort
8. 🟡 Step 8 — Add `examples/` + `postman/` collection
9. 🟡 Step 9 — Add CI checks (markdown link check, schema validation, OpenAPI lint if possible, TS typecheck)
10. 🟡 Step 10 — Final GREEN lock: tag `v1.0.0-api-contracts-green` + GitHub Release notes

## Principles
- No placeholders. Every doc is complete, concrete, and copy/paste friendly.
- Explicit fields only. Never use “etc.” in contract specs.
- JSONL is ground truth; WebSocket is fast path.
- Auth, RBAC, rate limits, and dangerous-command confirmation are fully documented.

