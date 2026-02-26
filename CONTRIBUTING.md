# Contributing to N-Defender API Contracts

Thank you for helping keep the N-Defender API contracts precise and production-ready.

## Branching Strategy
- Use feature branches: `chore/<topic>`, `fix/<topic>`, or `feat/<topic>`.
- Do not commit directly to `main`.
- Keep commits small and focused.

## Contract Rules (Non‑Negotiable)
- **Timestamps:** `timestamp_ms` only (epoch milliseconds).
- **GPS:** use `latitude` / `longitude` (no `lat`/`lng`).
- **Frequencies:** `freq_hz` (Hz), not MHz.
- **Signal:** `*_dbm` values are in dBm.
- **Errors (FastAPI):** `{"detail":"..."}`.
- **Commands:** body must be `{"payload":{...},"confirm":false}`.
- **Confirm gating:** dangerous commands require `confirm=true`.
- **Rate limits:** 10/min commands, 2/min dangerous.
- **WS envelope:** `{type,timestamp_ms,source,data}`.

## How to Add or Modify Endpoints (Checklist)
1) Update `docs/ALL_IN_ONE_API.md` (canonical).
2) Update `docs/ENDPOINTS/<service>.md`.
3) Update or add model docs in `docs/MODELS/`.
4) Update JSON schemas in `schemas/`.
5) Update OpenAPI in `docs/OPENAPI.yaml`.
6) Update TypeScript types in `types/`.
7) Update examples in `examples/` if behavior changes.
8) Update `tools/validate_contract.py` if validation rules change.
9) Run validation (see below).

## Validation
Run all checks:
```bash
scripts/validate.sh
```

Local API smoke:
```bash
scripts/smoke_local.sh
```

Public API smoke:
```bash
scripts/smoke_public.sh
```

## Security Rules
- **Never** commit tokens, passwords, or credentialed URLs.
- Before pushing, run a secret scan and verify no credentialed URLs are present.

## Docs Structure
- Canonical: `docs/ALL_IN_ONE_API.md`
- Index: `docs/INDEX.md`
- Endpoints: `docs/ENDPOINTS/`
- Models: `docs/MODELS/`
- Schemas: `schemas/`
- OpenAPI: `docs/OPENAPI.yaml`

## Pull Request Checklist
- [ ] Contract rules followed (timestamp_ms, freq_hz, latitude/longitude).
- [ ] OpenAPI and schemas updated.
- [ ] Examples updated.
- [ ] Validation passed.
