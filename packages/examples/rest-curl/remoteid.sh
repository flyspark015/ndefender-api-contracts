#!/usr/bin/env bash
set -euo pipefail

# Usage (Aggregator):
#   BASE_URL=http://127.0.0.1:8001/api/v1 ./remoteid.sh
# Usage (RemoteID Engine):
#   BASE_URL=http://127.0.0.1:<port>/api/v1 ./remoteid.sh
# Public:
#   BASE_URL=https://<host>/api/v1 ./remoteid.sh

BASE_URL="${BASE_URL:-http://127.0.0.1:8001/api/v1}"

curl -sS "$BASE_URL/remote_id" || true
curl -sS "$BASE_URL/remote_id/contacts" || true
curl -sS "$BASE_URL/remote_id/stats" || true

# Direct engine endpoints (if using engine base):
curl -sS "$BASE_URL/remoteid-engine/status" || true
curl -sS "$BASE_URL/remoteid-engine/contacts" || true
curl -sS "$BASE_URL/remoteid-engine/stats" || true
