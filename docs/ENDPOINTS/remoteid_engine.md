# RemoteID Engine Local API

Base: `/api/v1`

Common errors:
- `404` Not found (unknown endpoints)

## GET /status
**Purpose**: capture/decoder health and counters.
Request: none.
Response (200):
```json
{"state":"ok","last_ts":1700000000000,"contacts_active":1,"mode":"live","updated_ts":1700000000000}
```

Errors: `404`

Notes:
- `last_ts` and `updated_ts` are epoch ms.

## GET /health
**Purpose**: same as `/status`.
Request: none.
Same response as `/status`.
Errors: `404`

## Curl Examples
```bash
export BASE_URL=http://127.0.0.1:9010/api/v1

curl -sS $BASE_URL/status
curl -sS $BASE_URL/health
```
