#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

LOCAL_BASE="${LOCAL_BASE:-http://127.0.0.1:8001/api/v1}"
PUBLIC_BASE="${PUBLIC_BASE:-}"
WS_SECONDS="${WS_SECONDS:-10}"

if [[ "${SKIP_VALIDATE:-0}" == "1" ]]; then
  echo "SKIP_VALIDATE=1 set; skipping runtime validation"
  exit 0
fi

python3 tools/validate_contract.py --local "$LOCAL_BASE" --ws-seconds "$WS_SECONDS"

if [[ -n "$PUBLIC_BASE" ]]; then
  python3 tools/validate_contract.py --local "$LOCAL_BASE" --public "$PUBLIC_BASE" --ws-seconds "$WS_SECONDS"
fi
