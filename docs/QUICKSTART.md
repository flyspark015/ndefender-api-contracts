# Quickstart

This repository defines the canonical contract. Use it to validate live deployments.

## Prerequisites
- Python 3.10+
- `curl`
- `jq` (optional)
- `pip install websockets` (required for WS validation)

## Local vs Public Bases
- Local: `http://127.0.0.1:8001/api/v1`
- Public: `https://n.flyspark.in/api/v1`
- WS: `/api/v1/ws` (ws:// or wss://)

## REST Smoke Tests
```bash
curl -sS http://127.0.0.1:8001/api/v1/health
curl -sS http://127.0.0.1:8001/api/v1/status
curl -sS https://n.flyspark.in/api/v1/status
```

Expected (example):
```json
{"status":"ok","timestamp_ms":1700000000000}
```

## WS Smoke Test
```bash
python3 tools/validate_contract.py --public https://n.flyspark.in/api/v1 --ws-seconds 10
```

Expected (example):
```
PASS: contract checks ok
```

## Contract Validation Script
```bash
python3 tools/validate_contract.py \
  --local http://127.0.0.1:8001/api/v1 \
  --public https://n.flyspark.in/api/v1 \
  --ws-seconds 10
```

Exits non-zero if required fields are missing or WS has <3 messages.

## Rate Limits
- Commands: `10/min`
- Dangerous commands (reboot/shutdown): `2/min` with `confirm=true`

## CONTRACT GAP
- WS `HEARTBEAT` is emitted by runtime but not yet formalized. See `docs/CONTRACT_GAPS.md`.

## See Also (Canonical)
- `docs/ALL_IN_ONE_API.md` → **Command System (WRITE APIs)** and **Complete Verification (copy/paste)** sections.

## Diagnostics (Operational)
```bash
systemctl status ndefender-backend-aggregator --no-pager | sed -n '1,25p'
journalctl -u ndefender-backend-aggregator -n 120 --no-pager
curl -sS https://n.flyspark.in/api/v1/status | jq '.overall_ok,.rf,.remote_id'
python3 examples/ws_client.py --url wss://n.flyspark.in/api/v1/ws
```
