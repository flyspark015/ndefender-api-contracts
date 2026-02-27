# N-Defender Test Results — 2026-02-27

Canonical base: `/api/v1`
Ports: 8001 (Aggregator), 8002 (System Controller), 8890 (RFScan). Legacy 8000 must be absent.

## A) Baseline Host + Repo

```
Linux ndefender-pi 6.12.62+rpt-rpi-2712 #1 SMP PREEMPT Debian 1:6.12.62-1+rpt1~bookworm (2026-01-19) aarch64 GNU/Linux
ndefender-pi
Sat Feb 28 00:26:31 IST 2026
## chore/readme-and-structure...origin/chore/readme-and-structure
?? docs/TEST_RESULTS_2026-02-27.md
d70e181
v20.20.0
10.8.2
Python 3.11.2
```

## B) Repo Validation

### scripts/validate.sh
```
PASS
```

### npm run ci
```

> ndefender-api-contracts@1.0.0 ci
> npm run ci:links && npm run ci:schemas && npm run ci:openapi && npm run ci:readme-openapi && npm run ci:readme-examples && npm run typecheck && npm run ci:validate


> ndefender-api-contracts@1.0.0 ci:links
> python3 ci/check_markdown_links.py

markdown links ok: 53 files

> ndefender-api-contracts@1.0.0 ci:schemas
> python3 ci/check_schemas.py

schemas ok: 26

> ndefender-api-contracts@1.0.0 ci:openapi
> python3 ci/check_openapi.py

openapi ok

> ndefender-api-contracts@1.0.0 ci:readme-openapi
> python3 ci/check_readme_openapi_sync.py

README endpoint index matches OpenAPI paths (canonical base /api/v1)

> ndefender-api-contracts@1.0.0 ci:readme-examples
> python3 ci/readme_examples_lint.py

README examples lint ok

> ndefender-api-contracts@1.0.0 typecheck
> tsc -p tsconfig.json


> ndefender-api-contracts@1.0.0 ci:validate
> bash scripts/validate.sh

PASS
```

## C) Ports

```
LISTEN 0      128                      127.0.0.1:8890       0.0.0.0:*    users:(("ndefender-antsd",pid=2071035,fd=6))
LISTEN 0      2048                     127.0.0.1:8001       0.0.0.0:*    users:(("uvicorn",pid=2076223,fd=7))        
LISTEN 0      2048                     127.0.0.1:8002       0.0.0.0:*    users:(("uvicorn",pid=2076239,fd=14))       
```

## D) REST Smoke (Local)

```
LISTEN 0      128                      127.0.0.1:8890       0.0.0.0:*    users:(("ndefender-antsd",pid=2071035,fd=6))
LISTEN 0      2048                     127.0.0.1:8001       0.0.0.0:*    users:(("uvicorn",pid=2076223,fd=7))        
LISTEN 0      2048                     127.0.0.1:8002       0.0.0.0:*    users:(("uvicorn",pid=2076239,fd=14))       
status ok: timestamp_ms present
HTTP/1.1 400 Bad Request
date: Fri, 27 Feb 2026 18:57:44 GMT
server: uvicorn
content-length: 29
content-type: application/json

{"detail":"confirm_required"}
websocat not found; use tools/validate_contract.py for WS checks
SMOKE_LOCAL: PASS
```

## E) REST Smoke (Public)

```
Skipping local port checks (BASE is remote)
status ok: timestamp_ms present
HTTP/2 400 
date: Fri, 27 Feb 2026 18:57:52 GMT
content-type: application/json
content-length: 29
server: cloudflare
cf-cache-status: DYNAMIC
nel: {"report_to":"cf-nel","success_fraction":0.0,"max_age":604800}
report-to: {"group":"cf-nel","max_age":604800,"endpoints":[{"url":"https://a.nel.cloudflare.com/report/v4?s=AwHXnADDORgukSihKnAmBkv9TnQ1QlWPJzY%2FKcQ6GB%2BVyiks%2F4vLcdV8Mygu%2BAAEgvwh4xadZrO0yZCJCaTB8dhY0JDFZGNeY36bmiA7J6L6wswKfGye%2FN8%3D"}]}
cf-ray: 9d49e90cc8c00517-SIN
alt-svc: h3=":443"; ma=86400

{"detail":"confirm_required"}
websocat not found; use tools/validate_contract.py for WS checks
SMOKE_PUBLIC: PASS
```

## F) WebSocket Smoke

```
{"type":"HELLO","timestamp_ms":1772218728197,"source":"aggregator","data":{"timestamp_ms":1772218728197}}
```

## G) Confirm-Gating Proof

```
curl -sS -i -X POST http://127.0.0.1:8001/api/v1/system/reboot -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```
```
HTTP/1.1 400 Bad Request
date: Fri, 27 Feb 2026 18:58:53 GMT
server: uvicorn
content-length: 29
content-type: application/json

{"detail":"confirm_required"}
```

## H) Summary Table

| Test | Result |
|------|--------|
| scripts/validate.sh | PASS |
| npm run ci | PASS |
| scripts/smoke_local.sh | PASS |
| scripts/smoke_public.sh | PASS |
| scripts/smoke_ws.sh | PASS |
| confirm-gating proof | PASS |

- Tested commit: `5425c4a`
- Branch: `chore/readme-and-structure`
- Timestamp: Sat Feb 28 00:31:13 IST 2026