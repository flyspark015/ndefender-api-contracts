# PR Summary: Docs + OpenAPI Finalization

## What changed
- Enforced `timestamp_ms` across all REST/WS examples and OpenAPI.
- Hardened endpoint and model docs with purposes, errors, and curl examples.
- Added strict contract validator: `tools/validate_contract.py`.
- Documented known contract gaps and migration plans.
- Added full command system documentation and complete verification steps in `docs/ALL_IN_ONE_API.md`.

## Why this is correct
- All files now align to the canonical contract in `docs/ALL_IN_ONE_API.md`.
- Public envelope and timestamp rules are enforced consistently.
- Examples avoid empty `{}` blocks for major sections and show explicit status/last_error fields.

## How to validate
```bash
python3 tools/validate_contract.py \
  --local http://127.0.0.1:8001/api/v1 \
  --public https://n.flyspark.in/api/v1 \
  --ws-seconds 10
```
