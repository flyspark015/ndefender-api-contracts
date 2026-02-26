# N-Defender API Contracts

Single source of truth for N-Defender REST + WebSocket contracts, schemas, OpenAPI, and integration docs.

## Canonical Contract
- `docs/ALL_IN_ONE_API.md`

## Entry Points
- Start here: `docs/ALL_IN_ONE_API.md`
- Quickstart: `docs/QUICKSTART.md`
- Endpoints: `docs/ENDPOINTS/`
- Models: `docs/MODELS/`

## Docs Map
- `docs/QUICKSTART.md`
- `docs/ERROR_MODEL.md`
- `docs/FLOWS_TX_RX.md`
- `docs/ENDPOINTS/` (per-service endpoint reference)
- `docs/MODELS/` (model definitions)
- `docs/CONTRACT_GAPS.md`

## Schemas + OpenAPI
- JSON Schemas: `schemas/`
- OpenAPI 3.1: `openapi/ndefender.openapi.yaml` (mirrors `docs/OPENAPI.yaml`)

## Changelog (Docs)
- 2026-02-26: Enforced `timestamp_ms` everywhere, added strict contract validation, and hardened endpoint/model docs.
