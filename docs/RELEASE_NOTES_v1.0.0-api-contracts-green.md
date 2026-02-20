# Release Notes — v1.0.0-api-contracts-green

## Summary
This release establishes the N-Defender API Contracts repository as the single source of truth for REST + WebSocket APIs, schemas, examples, OpenAPI, and TypeScript types.

## Highlights
- ✅ Unified API specification: `docs/ALL_IN_ONE_API.md`
- ✅ WebSocket event catalog: `docs/WEBSOCKET_EVENTS.md`
- ✅ OpenAPI 3.0.3 spec: `docs/OPENAPI.yaml`
- ✅ JSON Schemas in `schemas/` (StatusSnapshot, Contact, EventEnvelope, COMMAND_ACK, TELEMETRY_UPDATE, CONTACT_* events, REPLAY_STATE, UPS telemetry)
- ✅ TypeScript contracts: `types/contracts.ts`
- ✅ Examples + Postman collections: `examples/`, `postman/`
- ✅ CI checks: markdown link check, schema validation, OpenAPI validation, TS typecheck

## Validation
- Markdown links check passed.
- JSON Schema validation passed (Draft 2020-12).
- OpenAPI validation passed.
- TypeScript typecheck passed.

## Notes
- WebSocket endpoints are documented in `docs/WEBSOCKET_EVENTS.md` and referenced in OpenAPI as non-HTTP operations.

