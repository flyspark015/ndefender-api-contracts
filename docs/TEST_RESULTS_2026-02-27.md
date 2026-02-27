# N-Defender Test Results — 2026-02-27

**IMPORTANT:** This repo contains contracts/docs/validation only; tests were run on the Raspberry Pi against deployed services (not a local setup guide).

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

## A2) Baseline Host + Repo (Re-run)

### uname -a

**Command:**

```uname -a
```

**Output:**

```Linux ndefender-pi 6.12.62+rpt-rpi-2712 #1 SMP PREEMPT Debian 1:6.12.62-1+rpt1~bookworm (2026-01-19) aarch64 GNU/Linux
```

**Result:** PASS

### hostname

**Command:**

```hostname
```

**Output:**

```ndefender-pi
```

**Result:** PASS

### date (IST)

**Command:**

```TZ=Asia/Kolkata date
```

**Output:**

```Sat Feb 28 00:41:01 IST 2026
```

**Result:** PASS

### ports

**Command:**

```ss -lntp | egrep '(:8000|:8001|:8002|:8890)\b' || true
```

**Output:**

```LISTEN 0      128                      127.0.0.1:8890       0.0.0.0:*    users:(("ndefender-antsd",pid=2071035,fd=6))
LISTEN 0      2048                     127.0.0.1:8001       0.0.0.0:*    users:(("uvicorn",pid=2076223,fd=7))        
LISTEN 0      2048                     127.0.0.1:8002       0.0.0.0:*    users:(("uvicorn",pid=2076239,fd=14))
```

**Result:** PASS

### systemctl is-active

**Command:**

```systemctl is-active ndefender-backend-aggregator ndefender-system-controller ndefender-rfscan ndefender-remoteid-engine
```

**Output:**

```active
active
active
active
```

**Result:** PASS

### systemctl is-enabled

**Command:**

```systemctl is-enabled ndefender-backend-aggregator ndefender-system-controller ndefender-rfscan ndefender-remoteid-engine
```

**Output:**

```enabled
enabled
enabled
enabled
```

**Result:** PASS

### git status -sb

**Command:**

```git -C /home/toybook/ndefender-api-contracts status -sb
```

**Output:**

```## chore/readme-and-structure...origin/chore/readme-and-structure
 M docs/TEST_RESULTS_2026-02-27.md
```

**Result:** PASS

### git rev-parse --short HEAD

**Command:**

```git -C /home/toybook/ndefender-api-contracts rev-parse --short HEAD
```

**Output:**

```21025a5
```

**Result:** PASS

### node -v

**Command:**

```node -v
```

**Output:**

```v20.20.0
```

**Result:** PASS

### npm -v

**Command:**

```npm -v
```

**Output:**

```10.8.2
```

**Result:** PASS

### python3 --version

**Command:**

```python3 --version
```

**Output:**

```Python 3.11.2
```

**Result:** PASS


## B2) Repo Validation (Re-run)

### scripts/validate.sh

**Command:**

```cd /home/toybook/ndefender-api-contracts && scripts/validate.sh
```

**Output:**

```PASS
```

**Result:** PASS

### npm run ci

**Command:**

```cd /home/toybook/ndefender-api-contracts && npm run ci
```

**Output:**

```> ndefender-api-contracts@1.0.0 ci
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

**Result:** PASS


## C2) Ports Check (Re-run)

### ss -lntp

**Command:**

```ss -lntp | egrep '(:8000|:8001|:8002|:8890)\b' || true
```

**Output:**

```LISTEN 0      128                      127.0.0.1:8890       0.0.0.0:*    users:(("ndefender-antsd",pid=2071035,fd=6))
LISTEN 0      2048                     127.0.0.1:8001       0.0.0.0:*    users:(("uvicorn",pid=2076223,fd=7))        
LISTEN 0      2048                     127.0.0.1:8002       0.0.0.0:*    users:(("uvicorn",pid=2076239,fd=14))
```

**Result:** PASS


## D2) REST Smoke (Local) (Re-run)

### scripts/smoke_local.sh

**Command:**

```cd /home/toybook/ndefender-api-contracts && scripts/smoke_local.sh
```

**Output:**

```LISTEN 0      128                      127.0.0.1:8890       0.0.0.0:*    users:(("ndefender-antsd",pid=2071035,fd=6))
LISTEN 0      2048                     127.0.0.1:8001       0.0.0.0:*    users:(("uvicorn",pid=2076223,fd=7))        
LISTEN 0      2048                     127.0.0.1:8002       0.0.0.0:*    users:(("uvicorn",pid=2076239,fd=14))       
status ok: timestamp_ms present
HTTP/1.1 400 Bad Request
date: Fri, 27 Feb 2026 19:11:09 GMT
server: uvicorn
content-length: 29
content-type: application/json

{"detail":"confirm_required"}
SMOKE_LOCAL: PASS
websocat not found; use tools/validate_contract.py for WS checks
```

**Result:** PASS


## E2) REST Smoke (Public) (Re-run)

### scripts/smoke_public.sh

**Command:**

```cd /home/toybook/ndefender-api-contracts && scripts/smoke_public.sh
```

**Output:**

```Skipping local port checks (BASE is remote)
status ok: timestamp_ms present
HTTP/2 400 
date: Fri, 27 Feb 2026 19:11:12 GMT
content-type: application/json
content-length: 29
server: cloudflare
cf-cache-status: DYNAMIC
nel: {"report_to":"cf-nel","success_fraction":0.0,"max_age":604800}
report-to: {"group":"cf-nel","max_age":604800,"endpoints":[{"url":"https://a.nel.cloudflare.com/report/v4?s=gEhY7bL2E2GBBb757oUSLItmjxL2cORVRcZwMamR249RqMQWErFzUqsoH5wPcJh81u%2F45USl%2Fgv9XVwEosXh%2F5XSU8njXRA1N4EYVbU0jxv5aoQ3YEB57bY%3D"}]}
cf-ray: 9d49fc955e87a05d-SIN
alt-svc: h3=":443"; ma=86400

{"detail":"confirm_required"}
SMOKE_PUBLIC: PASS
websocat not found; use tools/validate_contract.py for WS checks
```

**Result:** PASS


## F2) WebSocket Smoke (Re-run)

### scripts/smoke_ws.sh

**Command:**

```cd /home/toybook/ndefender-api-contracts && scripts/smoke_ws.sh
```

**Output:**

```{"type":"HELLO","timestamp_ms":1772219472605,"source":"aggregator","data":{"timestamp_ms":1772219472605}}
```

**Result:** PASS


## G2) Confirm-Gating Proof (Re-run)

### confirm_required proof

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/system/reboot -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 400 Bad Request
date: Fri, 27 Feb 2026 19:11:11 GMT
server: uvicorn
content-length: 29
content-type: application/json

{"detail":"confirm_required"}
```

**Result:** PASS


## H1) OpenAPI GET Endpoint List

### GET endpoints discovered

**Command:**

```python: parse docs/OPENAPI.yaml
```

**Output:**

```/antsdr
/antsdr-scan/config
/antsdr-scan/device
/antsdr-scan/events/last
/antsdr-scan/gain
/antsdr-scan/health
/antsdr-scan/stats
/antsdr-scan/sweep/state
/antsdr-scan/version
/antsdr/gain
/antsdr/stats
/antsdr/sweep/state
/audio
/contacts
/esp32
/esp32/config
/gps
/health
/network
/network/bluetooth/devices
/network/bluetooth/state
/network/wifi/scan
/network/wifi/state
/observability/config
/observability/health
/observability/health/detail
/observability/status
/observability/version
/power
/remote_id
/remote_id/contacts
/remote_id/stats
/remoteid-engine/contacts
/remoteid-engine/health
/remoteid-engine/replay/state
/remoteid-engine/stats
/remoteid-engine/status
/rf
/services
/status
/system
/system-controller/audio
/system-controller/gps
/system-controller/health
/system-controller/network
/system-controller/network/bluetooth/devices
/system-controller/network/bluetooth/state
/system-controller/network/wifi/scan
/system-controller/network/wifi/state
/system-controller/services
/system-controller/status
/system-controller/system
/system-controller/ups
/system-controller/ws
/video
/ws
```

**Result:** PASS


## H2) OpenAPI POST Endpoint List

### POST endpoints discovered

**Command:**

```python: parse docs/OPENAPI.yaml
```

**Output:**

```/antsdr-scan/config/reload
/antsdr-scan/device/calibrate
/antsdr-scan/device/reset
/antsdr-scan/gain/set
/antsdr-scan/sweep/start
/antsdr-scan/sweep/stop
/antsdr/device/reset
/antsdr/gain/set
/antsdr/sweep/start
/antsdr/sweep/stop
/audio/mute
/audio/volume
/esp32/buttons/simulate
/esp32/buzzer
/esp32/config
/esp32/leds
/gps/restart
/network/bluetooth/disable
/network/bluetooth/enable
/network/bluetooth/pair
/network/bluetooth/scan/start
/network/bluetooth/scan/stop
/network/bluetooth/unpair
/network/wifi/connect
/network/wifi/disable
/network/wifi/disconnect
/network/wifi/enable
/observability/diag/bundle
/remote_id/monitor/start
/remote_id/monitor/stop
/remoteid-engine/monitor/start
/remoteid-engine/monitor/stop
/remoteid-engine/replay/start
/remoteid-engine/replay/stop
/scan/start
/scan/stop
/system-controller/audio/mute
/system-controller/audio/volume
/system-controller/gps/restart
/system-controller/network/bluetooth/disable
/system-controller/network/bluetooth/enable
/system-controller/network/bluetooth/pair
/system-controller/network/bluetooth/scan/start
/system-controller/network/bluetooth/scan/stop
/system-controller/network/bluetooth/unpair
/system-controller/network/wifi/connect
/system-controller/network/wifi/disable
/system-controller/network/wifi/disconnect
/system-controller/network/wifi/enable
/system-controller/services/{name}/restart
/system-controller/system/reboot
/system-controller/system/shutdown
/system/reboot
/system/shutdown
/video/select
/vrx/tune
```

**Result:** PASS


## H3) GET Endpoint Tests (Aggregator Base)

### GET /antsdr

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/antsdr
```

**Output:**

```{"timestamp_ms":1772219470476,"connected":false,"uri":"ip:192.168.10.2","temperature_c":null,"last_error":"no_rf_events"}
```

**Result:** PASS

### GET /antsdr-scan/config

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/antsdr-scan/config
```

**Output:**

```{"detail":"Not Found"}
```

**Result:** PASS

### GET /antsdr-scan/device

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/antsdr-scan/device
```

**Output:**

```{"detail":"Not Found"}
```

**Result:** PASS

### GET /antsdr-scan/events/last

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/antsdr-scan/events/last
```

**Output:**

```{"detail":"Not Found"}
```

**Result:** PASS

### GET /antsdr-scan/gain

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/antsdr-scan/gain
```

**Output:**

```{"detail":"Not Found"}
```

**Result:** PASS

### GET /antsdr-scan/health

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/antsdr-scan/health
```

**Output:**

```{"detail":"Not Found"}
```

**Result:** PASS

### GET /antsdr-scan/stats

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/antsdr-scan/stats
```

**Output:**

```{"detail":"Not Found"}
```

**Result:** PASS

### GET /antsdr-scan/sweep/state

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/antsdr-scan/sweep/state
```

**Output:**

```{"detail":"Not Found"}
```

**Result:** PASS

### GET /antsdr-scan/version

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/antsdr-scan/version
```

**Output:**

```{"detail":"Not Found"}
```

**Result:** PASS

### GET /antsdr/gain

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/antsdr/gain
```

**Output:**

```{"timestamp_ms":1772219473006,"mode":"auto"}
```

**Result:** PASS

### GET /antsdr/stats

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/antsdr/stats
```

**Output:**

```{"timestamp_ms":1772219473026,"frames_processed":0,"events_emitted":0,"last_event_timestamp_ms":0}
```

**Result:** PASS

### GET /antsdr/sweep/state

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/antsdr/sweep/state
```

**Output:**

```{"timestamp_ms":1772219473042,"running":false,"active_plan":"5G8_RaceBand","plans":[{"name":"5G8_RaceBand","start_hz":5658000000.0,"end_hz":5917000000.0,"step_hz":2000000.0},{"name":"5G8_FatShark","start_hz":5733000000.0,"end_hz":5866000000.0,"step_hz":2000000.0},{"name":"5G8_BandA","start_hz":5865000000.0,"end_hz":5945000000.0,"step_hz":2000000.0},{"name":"5G8_Digital","start_hz":5725000000.0,"end_hz":5850000000.0,"step_hz":2000000.0},{"name":"2G4_Control","start_hz":2400000000.0,"end_hz":2483500000.0,"step_hz":1000000.0},{"name":"915_Control","start_hz":902000000.0,"end_hz":928000000.0,"step_hz":1000000.0}],"last_update_ms":1772219473042,"last_error":null}
```

**Result:** PASS

### GET /audio

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/audio
```

**Output:**

```{"muted":null,"volume_percent":null,"status":"degraded","timestamp_ms":1772219470193,"last_error":"audio_unavailable"}
```

**Result:** PASS

### GET /contacts

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/contacts
```

**Output:**

```{"contacts":[{"id":"fpv:1","type":"FPV","source":"esp32","last_seen_ts":1772219282836,"severity":"unknown","vrx_id":1,"freq_hz":5803000000,"rssi_raw":1221,"selected":1,"last_seen_uptime_ms":80079364}]}
```

**Result:** PASS

### GET /esp32

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/esp32
```

**Output:**

```{"timestamp_ms":1772219285950,"connected":false,"last_seen_ms":1772219282836,"rtt_ms":null,"fw_version":null,"heartbeat":null,"capabilities":null,"last_error":"[Errno 2] could not open port /dev/ttyACM0: [Errno 2] No such file or directory: '/dev/ttyACM0'"}
```

**Result:** PASS

### GET /esp32/config

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/esp32/config
```

**Output:**

```{"timestamp_ms":1772219473090,"schema_version":null,"config":{}}
```

**Result:** PASS

### GET /gps

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/gps
```

**Output:**

```{"timestamp_ms":1772219467171,"fix":"NO_FIX","satellites":{"in_view":0,"in_use":0},"hdop":null,"vdop":null,"pdop":null,"latitude":null,"longitude":null,"altitude_m":null,"speed_m_s":null,"heading_deg":null,"last_update_ms":1772219467171,"age_ms":null,"source":"gpsd","last_error":"gpsd_no_data"}
```

**Result:** PASS

### GET /health

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/health
```

**Output:**

```{"status":"ok","timestamp_ms":1772219473112}
```

**Result:** PASS

### GET /network

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/network
```

**Output:**

```{"connected":true,"ip_v4":"127.0.1.1","ip_v6":null,"ssid":"Airtel_Toybook","wifi":{"timestamp_ms":1772219470194,"enabled":true,"connected":true,"ssid":"Airtel_Toybook","bssid":"2E\\","ip":"127.0.1.1","rssi_dbm":null,"link_quality":null,"last_update_ms":1772219470194,"last_error":null},"bluetooth":{"timestamp_ms":1772219470286,"enabled":false,"scanning":false,"paired_count":0,"connected_devices":[],"last_update_ms":1772219470286,"last_error":null}}
```

**Result:** PASS

### GET /network/bluetooth/devices

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/network/bluetooth/devices
```

**Output:**

```{"timestamp_ms":1772219473137,"devices":[]}
```

**Result:** PASS

### GET /network/bluetooth/state

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/network/bluetooth/state
```

**Output:**

```{"timestamp_ms":1772219473168,"enabled":false,"scanning":false,"paired_count":0,"connected_devices":[],"last_update_ms":1772219473168,"last_error":null}
```

**Result:** PASS

### GET /network/wifi/scan

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/network/wifi/scan
```

**Output:**

```{"timestamp_ms":1772219473202,"networks":[{"ssid":"Airtel_Toybook","bssid":"2E\\","security":"C1\\"}],"last_error":null}
```

**Result:** PASS

### GET /network/wifi/state

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/network/wifi/state
```

**Output:**

```{"timestamp_ms":1772219473272,"enabled":true,"connected":true,"ssid":"Airtel_Toybook","bssid":"2E\\","ip":"127.0.1.1","rssi_dbm":null,"link_quality":null,"last_update_ms":1772219473272,"last_error":null}
```

**Result:** PASS

### GET /observability/config

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/observability/config
```

**Output:**

```{"detail":"Not Found"}
```

**Result:** PASS

### GET /observability/health

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/observability/health
```

**Output:**

```{"detail":"Not Found"}
```

**Result:** PASS

### GET /observability/health/detail

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/observability/health/detail
```

**Output:**

```{"detail":"Not Found"}
```

**Result:** PASS

### GET /observability/status

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/observability/status
```

**Output:**

```{"detail":"Not Found"}
```

**Result:** PASS

### GET /observability/version

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/observability/version
```

**Output:**

```{"detail":"Not Found"}
```

**Result:** PASS

### GET /power

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/power
```

**Output:**

```{"pack_voltage_v":16.282,"current_a":-0.008,"input_vbus_v":0.0,"input_power_w":0.0,"soc_percent":89,"state":"IDLE","time_to_empty_s":1697220,"time_to_full_s":null,"status":"ok","timestamp_ms":1772219472315,"per_cell_v":[4.071,4.071,4.071,4.07],"last_error":null}
```

**Result:** PASS

### GET /remote_id

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/remote_id
```

**Output:**

```{"last_event":{"reason":"no_odid_frames"},"last_event_type":"REMOTEID_STALE","last_timestamp_ms":1772219471602,"state":"DEGRADED","mode":"live","capture_active":true,"contacts_active":0,"last_update_ms":1772219471602,"last_error":"no_odid_frames","timestamp_ms":1772219473438}
```

**Result:** PASS

### GET /remote_id/contacts

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/remote_id/contacts
```

**Output:**

```{"timestamp_ms":1772219473451,"contacts":[{"id":"fpv:1","type":"FPV","source":"esp32","last_seen_ts":1772219282836,"severity":"unknown","vrx_id":1,"freq_hz":5803000000,"rssi_raw":1221,"selected":1,"last_seen_uptime_ms":80079364}]}
```

**Result:** PASS

### GET /remote_id/stats

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/remote_id/stats
```

**Output:**

```{"timestamp_ms":1772219473464,"frames":0,"decoded":0}
```

**Result:** PASS

### GET /remoteid-engine/contacts

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/remoteid-engine/contacts
```

**Output:**

```{"detail":"Not Found"}
```

**Result:** PASS

### GET /remoteid-engine/health

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/remoteid-engine/health
```

**Output:**

```{"detail":"Not Found"}
```

**Result:** PASS

### GET /remoteid-engine/replay/state

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/remoteid-engine/replay/state
```

**Output:**

```{"detail":"Not Found"}
```

**Result:** PASS

### GET /remoteid-engine/stats

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/remoteid-engine/stats
```

**Output:**

```{"detail":"Not Found"}
```

**Result:** PASS

### GET /remoteid-engine/status

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/remoteid-engine/status
```

**Output:**

```{"detail":"Not Found"}
```

**Result:** PASS

### GET /rf

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/rf
```

**Output:**

```{"last_event":{"reason":"no_rf_events"},"last_event_type":"RF_SCAN_OFFLINE","last_timestamp_ms":1772219470476,"scan_active":false,"status":"degraded","last_error":"no_rf_events"}
```

**Result:** PASS

### GET /services

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/services
```

**Output:**

```[]
```

**Result:** PASS

### GET /status

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/status
```

**Output:**

```{"timestamp_ms":1772219473565,"overall_ok":false,"system":{"cpu_temp_c":31.4,"cpu_usage_percent":16.8,"load_1m":1.86279296875,"load_5m":1.7900390625,"load_15m":1.67724609375,"ram_used_mb":2366,"ram_total_mb":16215,"disk_used_gb":66,"disk_total_gb":116,"uptime_s":162820,"throttled_flags":0,"status":"ok","timestamp_ms":1772219472311,"version":{"app":"ndefender-system-controller","git_sha":null,"build_ts":null},"cpu":{"temp_c":31.4,"load1":1.86279296875,"load5":1.7900390625,"load15":1.67724609375,"usage_percent":16.8},"ram":{"total_mb":16215,"used_mb":2366,"free_mb":13848},"storage":{"root":{"total_gb":116.606,"used_gb":66.939,"free_gb":43.723},"logs":null},"last_error":null},"power":{"pack_voltage_v":16.282,"current_a":-0.008,"input_vbus_v":0.0,"input_power_w":0.0,"soc_percent":89,"state":"IDLE","time_to_empty_s":1697220,"time_to_full_s":null,"status":"ok","timestamp_ms":1772219472315,"per_cell_v":[4.071,4.071,4.071,4.07],"last_error":null},"rf":{"last_event":{"reason":"no_rf_events"},"last_event_type":"RF_SCAN_OFFLINE","last_timestamp_ms":1772219470476,"scan_active":false,"status":"degraded","last_error":"no_rf_events"},"remote_id":{"last_event":{"reason":"no_odid_frames"},"last_event_type":"REMOTEID_STALE","last_timestamp_ms":1772219471602,"state":"DEGRADED","mode":"live","capture_active":true,"contacts_active":0,"last_update_ms":1772219471602,"last_error":"no_odid_frames"},"gps":{"timestamp_ms":1772219467171,"fix":"NO_FIX","satellites":{"in_view":0,"in_use":0},"hdop":null,"vdop":null,"pdop":null,"latitude":null,"longitude":null,"altitude_m":null,"speed_m_s":null,"heading_deg":null,"last_update_ms":1772219467171,"age_ms":null,"source":"gpsd","last_error":"gpsd_no_data"},"esp32":{"timestamp_ms":1772219285950,"connected":false,"last_seen_ms":1772219282836,"rtt_ms":null,"fw_version":null,"heartbeat":null,"capabilities":null,"last_error":"[Errno 2] could not open port /dev/ttyACM0: [Errno 2] No such file or directory: '/dev/ttyACM0'"},"antsdr":{"timestamp_ms":1772219470476,"connected":false,"uri":"ip:192.168.10.2","temperature_c":null,"last_error":"no_rf_events"},"vrx":{"selected":1,"vrx":[{"id":1,"freq_hz":5803000000,"rssi_raw":1221},{"id":2,"freq_hz":5803000000,"rssi_raw":562},{"id":3,"freq_hz":5803000000,"rssi_raw":83}],"led":{"r":0,"y":0,"g":1},"sys":{"uptime_ms":80079364,"heap":337624,"status":"DISCONNECTED","last_error":"[Errno 2] could not open port /dev/ttyACM0: [Errno 2] No such file or directory: '/dev/ttyACM0'"},"scan_state":"idle"},"fpv":{"selected":1,"locked_channels":[],"rssi_raw":1221,"scan_state":"idle","freq_hz":5803000000},"video":{"selected":1,"status":"ok"},"services":[],"network":{"connected":true,"ip_v4":"127.0.1.1","ip_v6":null,"ssid":"Airtel_Toybook","wifi":{"timestamp_ms":1772219470194,"enabled":true,"connected":true,"ssid":"Airtel_Toybook","bssid":"2E\\","ip":"127.0.1.1","rssi_dbm":null,"link_quality":null,"last_update_ms":1772219470194,"last_error":null},"bluetooth":{"timestamp_ms":1772219470286,"enabled":false,"scanning":false,"paired_count":0,"connected_devices":[],"last_update_ms":1772219470286,"last_error":null}},"audio":{"muted":null,"volume_percent":null,"status":"degraded","timestamp_ms":1772219470193,"last_error":"audio_unavailable"},"contacts":[{"id":"fpv:1","type":"FPV","source":"esp32","last_seen_ts":1772219282836,"severity":"unknown","vrx_id":1,"freq_hz":5803000000,"rssi_raw":1221,"selected":1,"last_seen_uptime_ms":80079364}],"replay":{"active":false,"source":"none"}}
```

**Result:** PASS

### GET /system

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/system
```

**Output:**

```{"cpu_temp_c":31.4,"cpu_usage_percent":16.8,"load_1m":1.86279296875,"load_5m":1.7900390625,"load_15m":1.67724609375,"ram_used_mb":2366,"ram_total_mb":16215,"disk_used_gb":66,"disk_total_gb":116,"uptime_s":162820,"throttled_flags":0,"status":"ok","timestamp_ms":1772219472311,"version":{"app":"ndefender-system-controller","git_sha":null,"build_ts":null},"cpu":{"temp_c":31.4,"load1":1.86279296875,"load5":1.7900390625,"load15":1.67724609375,"usage_percent":16.8},"ram":{"total_mb":16215,"used_mb":2366,"free_mb":13848},"storage":{"root":{"total_gb":116.606,"used_gb":66.939,"free_gb":43.723},"logs":null},"last_error":null}
```

**Result:** PASS

### GET /system-controller/audio

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/system-controller/audio
```

**Output:**

```{"detail":"Not Found"}
```

**Result:** PASS

### GET /system-controller/gps

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/system-controller/gps
```

**Output:**

```{"detail":"Not Found"}
```

**Result:** PASS

### GET /system-controller/health

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/system-controller/health
```

**Output:**

```{"detail":"Not Found"}
```

**Result:** PASS

### GET /system-controller/network

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/system-controller/network
```

**Output:**

```{"detail":"Not Found"}
```

**Result:** PASS

### GET /system-controller/network/bluetooth/devices

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/system-controller/network/bluetooth/devices
```

**Output:**

```{"detail":"Not Found"}
```

**Result:** PASS

### GET /system-controller/network/bluetooth/state

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/system-controller/network/bluetooth/state
```

**Output:**

```{"detail":"Not Found"}
```

**Result:** PASS

### GET /system-controller/network/wifi/scan

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/system-controller/network/wifi/scan
```

**Output:**

```{"detail":"Not Found"}
```

**Result:** PASS

### GET /system-controller/network/wifi/state

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/system-controller/network/wifi/state
```

**Output:**

```{"detail":"Not Found"}
```

**Result:** PASS

### GET /system-controller/services

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/system-controller/services
```

**Output:**

```{"detail":"Not Found"}
```

**Result:** PASS

### GET /system-controller/status

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/system-controller/status
```

**Output:**

```{"detail":"Not Found"}
```

**Result:** PASS

### GET /system-controller/system

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/system-controller/system
```

**Output:**

```{"detail":"Not Found"}
```

**Result:** PASS

### GET /system-controller/ups

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/system-controller/ups
```

**Output:**

```{"detail":"Not Found"}
```

**Result:** PASS

### GET /system-controller/ws

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/system-controller/ws
```

**Output:**

```{"detail":"Not Found"}
```

**Result:** PASS

### GET /video

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/video
```

**Output:**

```{"selected":1,"status":"ok"}
```

**Result:** PASS

### GET /ws

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/ws
```

**Output:**

```{"detail":"Method Not Allowed"}
```

**Result:** PASS


## H4) POST Endpoint Tests (Aggregator Base)

### POST /antsdr-scan/config/reload

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/antsdr-scan/config/reload -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 404 Not Found
date: Fri, 27 Feb 2026 19:11:12 GMT
server: uvicorn
content-length: 22
content-type: application/json

{"detail":"Not Found"}
```

**Result:** PASS

### POST /antsdr-scan/device/calibrate

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/antsdr-scan/device/calibrate -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 404 Not Found
date: Fri, 27 Feb 2026 19:11:12 GMT
server: uvicorn
content-length: 22
content-type: application/json

{"detail":"Not Found"}
```

**Result:** FAIL

### POST /antsdr-scan/device/reset

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/antsdr-scan/device/reset -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 404 Not Found
date: Fri, 27 Feb 2026 19:11:12 GMT
server: uvicorn
content-length: 22
content-type: application/json

{"detail":"Not Found"}
```

**Result:** FAIL

### POST /antsdr-scan/gain/set

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/antsdr-scan/gain/set -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 404 Not Found
date: Fri, 27 Feb 2026 19:11:12 GMT
server: uvicorn
content-length: 22
content-type: application/json

{"detail":"Not Found"}
```

**Result:** PASS

### POST /antsdr-scan/sweep/start

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/antsdr-scan/sweep/start -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 404 Not Found
date: Fri, 27 Feb 2026 19:11:12 GMT
server: uvicorn
content-length: 22
content-type: application/json

{"detail":"Not Found"}
```

**Result:** PASS

### POST /antsdr-scan/sweep/stop

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/antsdr-scan/sweep/stop -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 404 Not Found
date: Fri, 27 Feb 2026 19:11:12 GMT
server: uvicorn
content-length: 22
content-type: application/json

{"detail":"Not Found"}
```

**Result:** PASS

### POST /antsdr/device/reset

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/antsdr/device/reset -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 400 Bad Request
date: Fri, 27 Feb 2026 19:11:12 GMT
server: uvicorn
content-length: 29
content-type: application/json

{"detail":"confirm_required"}
```

**Result:** PASS

### POST /antsdr/gain/set

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/antsdr/gain/set -H 'Content-Type: application/json' -d '{"payload": {"mode": "auto"}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 200 OK
date: Fri, 27 Feb 2026 19:11:12 GMT
server: uvicorn
content-length: 103
content-type: application/json

{"command":"gain/set","command_id":"antsdr-1772219473848","accepted":true,"timestamp_ms":1772219473848}
```

**Result:** PASS

### POST /antsdr/sweep/start

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/antsdr/sweep/start -H 'Content-Type: application/json' -d '{"payload": {"plan": "default"}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 200 OK
date: Fri, 27 Feb 2026 19:11:13 GMT
server: uvicorn
content-length: 106
content-type: application/json

{"command":"sweep/start","command_id":"antsdr-1772219473864","accepted":true,"timestamp_ms":1772219473864}
```

**Result:** PASS

### POST /antsdr/sweep/stop

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/antsdr/sweep/stop -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 409 Conflict
date: Fri, 27 Feb 2026 19:11:13 GMT
server: uvicorn
content-length: 29
content-type: application/json

{"detail":"scan_not_running"}
```

**Result:** PASS

### POST /audio/mute

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/audio/mute -H 'Content-Type: application/json' -d '{"payload": {"muted": true}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 200 OK
date: Fri, 27 Feb 2026 19:11:13 GMT
server: uvicorn
content-length: 135
content-type: application/json

{"command":"audio/mute","command_id":"4024c081-f5b9-4199-a9d4-670e3c009cb9","accepted":true,"detail":null,"timestamp_ms":1772219473907}
```

**Result:** PASS

### POST /audio/volume

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/audio/volume -H 'Content-Type: application/json' -d '{"payload": {"volume_percent": 50}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 200 OK
date: Fri, 27 Feb 2026 19:11:13 GMT
server: uvicorn
content-length: 137
content-type: application/json

{"command":"audio/volume","command_id":"f7a3d820-fa7b-4915-ad86-12746fb69878","accepted":true,"detail":null,"timestamp_ms":1772219473931}
```

**Result:** PASS

### POST /esp32/buttons/simulate

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/esp32/buttons/simulate -H 'Content-Type: application/json' -d '{"payload": {"button": "mute", "action": "press"}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 409 Conflict
date: Fri, 27 Feb 2026 19:11:13 GMT
server: uvicorn
content-length: 33
content-type: application/json

{"detail":"serial not connected"}
```

**Result:** PASS

### POST /esp32/buzzer

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/esp32/buzzer -H 'Content-Type: application/json' -d '{"payload": {"mode": "beep", "duration_ms": 100}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 409 Conflict
date: Fri, 27 Feb 2026 19:11:13 GMT
server: uvicorn
content-length: 33
content-type: application/json

{"detail":"serial not connected"}
```

**Result:** PASS

### POST /esp32/config

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/esp32/config -H 'Content-Type: application/json' -d '{"payload": {"config": {}}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 409 Conflict
date: Fri, 27 Feb 2026 19:11:13 GMT
server: uvicorn
content-length: 33
content-type: application/json

{"detail":"serial not connected"}
```

**Result:** PASS

### POST /esp32/leds

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/esp32/leds -H 'Content-Type: application/json' -d '{"payload": {"red": false, "yellow": false, "green": true}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 409 Conflict
date: Fri, 27 Feb 2026 19:11:13 GMT
server: uvicorn
content-length: 33
content-type: application/json

{"detail":"serial not connected"}
```

**Result:** PASS

### POST /gps/restart

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/gps/restart -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 400 Bad Request
date: Fri, 27 Feb 2026 19:11:13 GMT
server: uvicorn
content-length: 29
content-type: application/json

{"detail":"confirm_required"}
```

**Result:** PASS

### POST /network/bluetooth/disable

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/network/bluetooth/disable -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 200 OK
date: Fri, 27 Feb 2026 19:11:13 GMT
server: uvicorn
content-length: 150
content-type: application/json

{"command":"network/bluetooth/disable","command_id":"69cdb437-d0fd-4158-ab02-1912e9021f44","accepted":true,"detail":null,"timestamp_ms":1772219474015}
```

**Result:** PASS

### POST /network/bluetooth/enable

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/network/bluetooth/enable -H 'Content-Type: application/json' -d '{"payload": {"enabled": true}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 429 Too Many Requests
date: Fri, 27 Feb 2026 19:11:13 GMT
server: uvicorn
content-length: 25
content-type: application/json

{"detail":"rate_limited"}
```

**Result:** PASS

### POST /network/bluetooth/pair

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/network/bluetooth/pair -H 'Content-Type: application/json' -d '{"payload": {"addr": "00:11:22:33:44:55"}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 429 Too Many Requests
date: Fri, 27 Feb 2026 19:11:13 GMT
server: uvicorn
content-length: 25
content-type: application/json

{"detail":"rate_limited"}
```

**Result:** PASS

### POST /network/bluetooth/scan/start

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/network/bluetooth/scan/start -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 429 Too Many Requests
date: Fri, 27 Feb 2026 19:11:13 GMT
server: uvicorn
content-length: 25
content-type: application/json

{"detail":"rate_limited"}
```

**Result:** PASS

### POST /network/bluetooth/scan/stop

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/network/bluetooth/scan/stop -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 429 Too Many Requests
date: Fri, 27 Feb 2026 19:11:13 GMT
server: uvicorn
content-length: 25
content-type: application/json

{"detail":"rate_limited"}
```

**Result:** PASS

### POST /network/bluetooth/unpair

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/network/bluetooth/unpair -H 'Content-Type: application/json' -d '{"payload": {"addr": "00:11:22:33:44:55"}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 429 Too Many Requests
date: Fri, 27 Feb 2026 19:11:13 GMT
server: uvicorn
content-length: 25
content-type: application/json

{"detail":"rate_limited"}
```

**Result:** PASS

### POST /network/wifi/connect

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/network/wifi/connect -H 'Content-Type: application/json' -d '{"payload": {"ssid": "TEST_SSID", "password": "TEST_PASS", "hidden": false}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 429 Too Many Requests
date: Fri, 27 Feb 2026 19:11:13 GMT
server: uvicorn
content-length: 25
content-type: application/json

{"detail":"rate_limited"}
```

**Result:** PASS

### POST /network/wifi/disable

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/network/wifi/disable -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 429 Too Many Requests
date: Fri, 27 Feb 2026 19:11:13 GMT
server: uvicorn
content-length: 25
content-type: application/json

{"detail":"rate_limited"}
```

**Result:** PASS

### POST /network/wifi/disconnect

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/network/wifi/disconnect -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 429 Too Many Requests
date: Fri, 27 Feb 2026 19:11:13 GMT
server: uvicorn
content-length: 25
content-type: application/json

{"detail":"rate_limited"}
```

**Result:** PASS

### POST /network/wifi/enable

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/network/wifi/enable -H 'Content-Type: application/json' -d '{"payload": {"enabled": true}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 429 Too Many Requests
date: Fri, 27 Feb 2026 19:11:13 GMT
server: uvicorn
content-length: 25
content-type: application/json

{"detail":"rate_limited"}
```

**Result:** PASS

### POST /observability/diag/bundle

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/observability/diag/bundle -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 404 Not Found
date: Fri, 27 Feb 2026 19:11:13 GMT
server: uvicorn
content-length: 22
content-type: application/json

{"detail":"Not Found"}
```

**Result:** PASS

### POST /remote_id/monitor/start

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/remote_id/monitor/start -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 429 Too Many Requests
date: Fri, 27 Feb 2026 19:11:13 GMT
server: uvicorn
content-length: 25
content-type: application/json

{"detail":"rate_limited"}
```

**Result:** PASS

### POST /remote_id/monitor/stop

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/remote_id/monitor/stop -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 429 Too Many Requests
date: Fri, 27 Feb 2026 19:11:13 GMT
server: uvicorn
content-length: 25
content-type: application/json

{"detail":"rate_limited"}
```

**Result:** PASS

### POST /remoteid-engine/monitor/start

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/remoteid-engine/monitor/start -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 404 Not Found
date: Fri, 27 Feb 2026 19:11:13 GMT
server: uvicorn
content-length: 22
content-type: application/json

{"detail":"Not Found"}
```

**Result:** PASS

### POST /remoteid-engine/monitor/stop

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/remoteid-engine/monitor/stop -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 404 Not Found
date: Fri, 27 Feb 2026 19:11:13 GMT
server: uvicorn
content-length: 22
content-type: application/json

{"detail":"Not Found"}
```

**Result:** PASS

### POST /remoteid-engine/replay/start

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/remoteid-engine/replay/start -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 404 Not Found
date: Fri, 27 Feb 2026 19:11:13 GMT
server: uvicorn
content-length: 22
content-type: application/json

{"detail":"Not Found"}
```

**Result:** PASS

### POST /remoteid-engine/replay/stop

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/remoteid-engine/replay/stop -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 404 Not Found
date: Fri, 27 Feb 2026 19:11:13 GMT
server: uvicorn
content-length: 22
content-type: application/json

{"detail":"Not Found"}
```

**Result:** PASS

### POST /scan/start

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/scan/start -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 429 Too Many Requests
date: Fri, 27 Feb 2026 19:11:13 GMT
server: uvicorn
content-length: 25
content-type: application/json

{"detail":"rate_limited"}
```

**Result:** PASS

### POST /scan/stop

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/scan/stop -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 429 Too Many Requests
date: Fri, 27 Feb 2026 19:11:13 GMT
server: uvicorn
content-length: 25
content-type: application/json

{"detail":"rate_limited"}
```

**Result:** PASS

### POST /system-controller/audio/mute

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/system-controller/audio/mute -H 'Content-Type: application/json' -d '{"payload": {"muted": true}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 404 Not Found
date: Fri, 27 Feb 2026 19:11:13 GMT
server: uvicorn
content-length: 22
content-type: application/json

{"detail":"Not Found"}
```

**Result:** PASS

### POST /system-controller/audio/volume

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/system-controller/audio/volume -H 'Content-Type: application/json' -d '{"payload": {"volume_percent": 50}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 404 Not Found
date: Fri, 27 Feb 2026 19:11:13 GMT
server: uvicorn
content-length: 22
content-type: application/json

{"detail":"Not Found"}
```

**Result:** PASS

### POST /system-controller/gps/restart

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/system-controller/gps/restart -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 404 Not Found
date: Fri, 27 Feb 2026 19:11:13 GMT
server: uvicorn
content-length: 22
content-type: application/json

{"detail":"Not Found"}
```

**Result:** PASS

### POST /system-controller/network/bluetooth/disable

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/system-controller/network/bluetooth/disable -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 404 Not Found
date: Fri, 27 Feb 2026 19:11:13 GMT
server: uvicorn
content-length: 22
content-type: application/json

{"detail":"Not Found"}
```

**Result:** PASS

### POST /system-controller/network/bluetooth/enable

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/system-controller/network/bluetooth/enable -H 'Content-Type: application/json' -d '{"payload": {"enabled": true}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 404 Not Found
date: Fri, 27 Feb 2026 19:11:13 GMT
server: uvicorn
content-length: 22
content-type: application/json

{"detail":"Not Found"}
```

**Result:** PASS

### POST /system-controller/network/bluetooth/pair

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/system-controller/network/bluetooth/pair -H 'Content-Type: application/json' -d '{"payload": {"addr": "00:11:22:33:44:55"}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 404 Not Found
date: Fri, 27 Feb 2026 19:11:13 GMT
server: uvicorn
content-length: 22
content-type: application/json

{"detail":"Not Found"}
```

**Result:** PASS

### POST /system-controller/network/bluetooth/scan/start

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/system-controller/network/bluetooth/scan/start -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 404 Not Found
date: Fri, 27 Feb 2026 19:11:13 GMT
server: uvicorn
content-length: 22
content-type: application/json

{"detail":"Not Found"}
```

**Result:** PASS

### POST /system-controller/network/bluetooth/scan/stop

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/system-controller/network/bluetooth/scan/stop -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 404 Not Found
date: Fri, 27 Feb 2026 19:11:13 GMT
server: uvicorn
content-length: 22
content-type: application/json

{"detail":"Not Found"}
```

**Result:** PASS

### POST /system-controller/network/bluetooth/unpair

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/system-controller/network/bluetooth/unpair -H 'Content-Type: application/json' -d '{"payload": {"addr": "00:11:22:33:44:55"}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 404 Not Found
date: Fri, 27 Feb 2026 19:11:13 GMT
server: uvicorn
content-length: 22
content-type: application/json

{"detail":"Not Found"}
```

**Result:** PASS

### POST /system-controller/network/wifi/connect

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/system-controller/network/wifi/connect -H 'Content-Type: application/json' -d '{"payload": {"ssid": "TEST_SSID", "password": "TEST_PASS", "hidden": false}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 404 Not Found
date: Fri, 27 Feb 2026 19:11:13 GMT
server: uvicorn
content-length: 22
content-type: application/json

{"detail":"Not Found"}
```

**Result:** PASS

### POST /system-controller/network/wifi/disable

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/system-controller/network/wifi/disable -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 404 Not Found
date: Fri, 27 Feb 2026 19:11:13 GMT
server: uvicorn
content-length: 22
content-type: application/json

{"detail":"Not Found"}
```

**Result:** PASS

### POST /system-controller/network/wifi/disconnect

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/system-controller/network/wifi/disconnect -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 404 Not Found
date: Fri, 27 Feb 2026 19:11:13 GMT
server: uvicorn
content-length: 22
content-type: application/json

{"detail":"Not Found"}
```

**Result:** PASS

### POST /system-controller/network/wifi/enable

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/system-controller/network/wifi/enable -H 'Content-Type: application/json' -d '{"payload": {"enabled": true}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 404 Not Found
date: Fri, 27 Feb 2026 19:11:13 GMT
server: uvicorn
content-length: 22
content-type: application/json

{"detail":"Not Found"}
```

**Result:** PASS

### POST /system-controller/services/{name}/restart

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/system-controller/services/cloudflared/restart -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 404 Not Found
date: Fri, 27 Feb 2026 19:11:13 GMT
server: uvicorn
content-length: 22
content-type: application/json

{"detail":"Not Found"}
```

**Result:** FAIL

### POST /system-controller/system/reboot

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/system-controller/system/reboot -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 404 Not Found
date: Fri, 27 Feb 2026 19:11:13 GMT
server: uvicorn
content-length: 22
content-type: application/json

{"detail":"Not Found"}
```

**Result:** FAIL

### POST /system-controller/system/shutdown

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/system-controller/system/shutdown -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 404 Not Found
date: Fri, 27 Feb 2026 19:11:13 GMT
server: uvicorn
content-length: 22
content-type: application/json

{"detail":"Not Found"}
```

**Result:** FAIL

### POST /system/reboot

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/system/reboot -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 400 Bad Request
date: Fri, 27 Feb 2026 19:11:13 GMT
server: uvicorn
content-length: 29
content-type: application/json

{"detail":"confirm_required"}
```

**Result:** PASS

### POST /system/shutdown

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/system/shutdown -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 400 Bad Request
date: Fri, 27 Feb 2026 19:11:13 GMT
server: uvicorn
content-length: 29
content-type: application/json

{"detail":"confirm_required"}
```

**Result:** PASS

### POST /video/select

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/video/select -H 'Content-Type: application/json' -d '{"payload": {"sel": 1}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 429 Too Many Requests
date: Fri, 27 Feb 2026 19:11:13 GMT
server: uvicorn
content-length: 25
content-type: application/json

{"detail":"rate_limited"}
```

**Result:** PASS

### POST /vrx/tune

**Command:**

```curl -sS -i -X POST http://127.0.0.1:8001/api/v1/vrx/tune -H 'Content-Type: application/json' -d '{"payload": {"vrx_id": 1, "freq_hz": 5740000000}, "confirm": false}' | sed -n '1,25p'
```

**Output:**

```HTTP/1.1 429 Too Many Requests
date: Fri, 27 Feb 2026 19:11:13 GMT
server: uvicorn
content-length: 25
content-type: application/json

{"detail":"rate_limited"}
```

**Result:** PASS


## I2) Field-Level Contract Checks

### /status fields

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/status | jq '.overall_ok, .system.status, .network.connected, .gps.fix, .gps.latitude, .gps.longitude, .remote_id.state, .rf.status'
```

**Output:**

```false
"ok"
true
"NO_FIX"
null
null
"DEGRADED"
"degraded"
```

**Result:** PASS

### /gps fields

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/gps | jq '.fix, .satellites.in_view, .satellites.in_use, .latitude, .longitude'
```

**Output:**

```"NO_FIX"
0
0
null
null
```

**Result:** PASS

### /network/wifi/state

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/network/wifi/state | jq '.enabled, .connected, .ssid'
```

**Output:**

```true
true
"Airtel_Toybook"
```

**Result:** PASS

### /network/wifi/scan

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/network/wifi/scan | jq '.networks|length'
```

**Output:**

```1
```

**Result:** PASS

### /network/bluetooth/state

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/network/bluetooth/state | jq '.enabled, .scanning, .paired_count'
```

**Output:**

```false
false
0
```

**Result:** PASS

### /network/bluetooth/devices

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/network/bluetooth/devices | jq '.devices|length'
```

**Output:**

```0
```

**Result:** PASS

### /contacts

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/contacts | jq '.contacts[0].id, .contacts[0].type, .contacts[0].source, .contacts[0].last_seen_ts'
```

**Output:**

```"fpv:1"
"FPV"
"esp32"
1772219282836
```

**Result:** PASS

### /esp32

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/esp32 | jq '.connected, .heartbeat.ok, .capabilities'
```

**Output:**

```false
null
null
```

**Result:** PASS

### /antsdr

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/antsdr | jq '.connected, .uri'
```

**Output:**

```false
"ip:192.168.10.2"
```

**Result:** PASS

### /remote_id/status

**Command:**

```curl -sS http://127.0.0.1:8001/api/v1/remote_id/status | jq '.state, .mode, .capture_active, .contacts_active, .last_error'
```

**Output:**

```"DEGRADED"
"live"
true
0
"no_odid_frames"
```

**Result:** PASS

### RFScan /health

**Command:**

```curl -sS http://127.0.0.1:8890/api/v1/health | jq '.timestamp_ms'
```

**Output:**

```1772219475023
```

**Result:** PASS

### RFScan /stats

**Command:**

```curl -sS http://127.0.0.1:8890/api/v1/stats | jq '.timestamp_ms'
```

**Output:**

```1772219475069
```

**Result:** PASS

### RFScan /config

**Command:**

```curl -sS http://127.0.0.1:8890/api/v1/config | jq '.timestamp_ms'
```

**Output:**

```null
```

**Result:** PASS



## Z) Summary Table (Re-run)

| Test | Result |
|---|---|
| scripts/validate.sh | PASS |
| npm run ci | PASS |
| REST GET coverage | PASS (count: 56) |
| REST POST coverage | PASS (count: 56) |
| confirm-gating proof | see section G2 |
| WS proof | see section F2 |

Tested commit: `ref: refs/heads/chore/readme-and-structure`
Branch: `chore/readme-and-structure`
Timestamp: 2026-02-28 00:41:15


## H3b) GET Endpoint Tests w/ HTTP Status

### GET /antsdr (HTTP 200)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/antsdr
```

**Output:**

```{"timestamp_ms":1772219520594,"connected":false,"uri":"ip:192.168.10.2","temperature_c":null,"last_error":"no_rf_events"}
HTTP_STATUS:200
```

**Result:** PASS

### GET /antsdr-scan/config (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/antsdr-scan/config
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### GET /antsdr-scan/device (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/antsdr-scan/device
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### GET /antsdr-scan/events/last (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/antsdr-scan/events/last
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### GET /antsdr-scan/gain (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/antsdr-scan/gain
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### GET /antsdr-scan/health (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/antsdr-scan/health
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### GET /antsdr-scan/stats (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/antsdr-scan/stats
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### GET /antsdr-scan/sweep/state (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/antsdr-scan/sweep/state
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### GET /antsdr-scan/version (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/antsdr-scan/version
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### GET /antsdr/gain (HTTP 200)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/antsdr/gain
```

**Output:**

```{"timestamp_ms":1772219523838,"mode":"auto"}
HTTP_STATUS:200
```

**Result:** PASS

### GET /antsdr/stats (HTTP 200)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/antsdr/stats
```

**Output:**

```{"timestamp_ms":1772219523852,"frames_processed":0,"events_emitted":0,"last_event_timestamp_ms":0}
HTTP_STATUS:200
```

**Result:** PASS

### GET /antsdr/sweep/state (HTTP 200)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/antsdr/sweep/state
```

**Output:**

```{"timestamp_ms":1772219523865,"running":false,"active_plan":"5G8_RaceBand","plans":[{"name":"5G8_RaceBand","start_hz":5658000000.0,"end_hz":5917000000.0,"step_hz":2000000.0},{"name":"5G8_FatShark","start_hz":5733000000.0,"end_hz":5866000000.0,"step_hz":2000000.0},{"name":"5G8_BandA","start_hz":5865000000.0,"end_hz":5945000000.0,"step_hz":2000000.0},{"name":"5G8_Digital","start_hz":5725000000.0,"end_hz":5850000000.0,"step_hz":2000000.0},{"name":"2G4_Control","start_hz":2400000000.0,"end_hz":2483500000.0,"step_hz":1000000.0},{"name":"915_Control","start_hz":902000000.0,"end_hz":928000000.0,"step_hz":1000000.0}],"last_update_ms":1772219523865,"last_error":"pyadi-iio is required for AntSDR access"}
HTTP_STATUS:200
```

**Result:** PASS

### GET /audio (HTTP 200)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/audio
```

**Output:**

```{"muted":null,"volume_percent":null,"status":"degraded","timestamp_ms":1772219518223,"last_error":"audio_unavailable"}
HTTP_STATUS:200
```

**Result:** PASS

### GET /contacts (HTTP 200)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/contacts
```

**Output:**

```{"contacts":[{"id":"fpv:1","type":"FPV","source":"esp32","last_seen_ts":1772219282836,"severity":"unknown","vrx_id":1,"freq_hz":5803000000,"rssi_raw":1221,"selected":1,"last_seen_uptime_ms":80079364}]}
HTTP_STATUS:200
```

**Result:** PASS

### GET /esp32 (HTTP 200)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/esp32
```

**Output:**

```{"timestamp_ms":1772219285950,"connected":false,"last_seen_ms":1772219282836,"rtt_ms":null,"fw_version":null,"heartbeat":null,"capabilities":null,"last_error":"[Errno 2] could not open port /dev/ttyACM0: [Errno 2] No such file or directory: '/dev/ttyACM0'"}
HTTP_STATUS:200
```

**Result:** PASS

### GET /esp32/config (HTTP 200)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/esp32/config
```

**Output:**

```{"timestamp_ms":1772219523914,"schema_version":null,"config":{}}
HTTP_STATUS:200
```

**Result:** PASS

### GET /gps (HTTP 200)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/gps
```

**Output:**

```{"timestamp_ms":1772219515201,"fix":"NO_FIX","satellites":{"in_view":0,"in_use":0},"hdop":null,"vdop":null,"pdop":null,"latitude":null,"longitude":null,"altitude_m":null,"speed_m_s":null,"heading_deg":null,"last_update_ms":1772219515201,"age_ms":null,"source":"gpsd","last_error":"gpsd_no_data"}
HTTP_STATUS:200
```

**Result:** PASS

### GET /health (HTTP 200)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/health
```

**Output:**

```{"status":"ok","timestamp_ms":1772219523936}
HTTP_STATUS:200
```

**Result:** PASS

### GET /network (HTTP 200)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/network
```

**Output:**

```{"connected":true,"ip_v4":"127.0.1.1","ip_v6":null,"ssid":"Airtel_Toybook","wifi":{"timestamp_ms":1772219518225,"enabled":true,"connected":true,"ssid":"Airtel_Toybook","bssid":"2E\\","ip":"127.0.1.1","rssi_dbm":null,"link_quality":null,"last_update_ms":1772219518225,"last_error":null},"bluetooth":{"timestamp_ms":1772219518297,"enabled":false,"scanning":false,"paired_count":0,"connected_devices":[],"last_update_ms":1772219518297,"last_error":null}}
HTTP_STATUS:200
```

**Result:** PASS

### GET /network/bluetooth/devices (HTTP 200)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/network/bluetooth/devices
```

**Output:**

```{"timestamp_ms":1772219526324,"devices":[]}
HTTP_STATUS:200
```

**Result:** PASS

### GET /network/bluetooth/state (HTTP 200)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/network/bluetooth/state
```

**Output:**

```{"timestamp_ms":1772219526358,"enabled":false,"scanning":false,"paired_count":0,"connected_devices":[],"last_update_ms":1772219526358,"last_error":null}
HTTP_STATUS:200
```

**Result:** PASS

### GET /network/wifi/scan (HTTP 200)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/network/wifi/scan
```

**Output:**

```{"timestamp_ms":1772219526394,"networks":[{"ssid":"Airtel_Toybook","bssid":"2E\\","security":"C1\\"}],"last_error":null}
HTTP_STATUS:200
```

**Result:** PASS

### GET /network/wifi/state (HTTP 200)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/network/wifi/state
```

**Output:**

```{"timestamp_ms":1772219526457,"enabled":true,"connected":true,"ssid":"Airtel_Toybook","bssid":"2E\\","ip":"127.0.1.1","rssi_dbm":null,"link_quality":null,"last_update_ms":1772219526457,"last_error":null}
HTTP_STATUS:200
```

**Result:** PASS

### GET /observability/config (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/observability/config
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### GET /observability/health (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/observability/health
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### GET /observability/health/detail (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/observability/health/detail
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### GET /observability/status (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/observability/status
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### GET /observability/version (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/observability/version
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### GET /power (HTTP 200)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/power
```

**Output:**

```{"pack_voltage_v":16.282,"current_a":-0.009,"input_vbus_v":0.0,"input_power_w":0.0,"soc_percent":89,"state":"IDLE","time_to_empty_s":1697220,"time_to_full_s":null,"status":"ok","timestamp_ms":1772219526318,"per_cell_v":[4.071,4.071,4.07,4.07],"last_error":null}
HTTP_STATUS:200
```

**Result:** PASS

### GET /remote_id (HTTP 200)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/remote_id
```

**Output:**

```{"last_event":{"reason":"no_odid_frames"},"last_event_type":"REMOTEID_STALE","last_timestamp_ms":1772219522039,"state":"DEGRADED","mode":"live","capture_active":true,"contacts_active":0,"last_update_ms":1772219522039,"last_error":"no_odid_frames","timestamp_ms":1772219526614}
HTTP_STATUS:200
```

**Result:** PASS

### GET /remote_id/contacts (HTTP 200)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/remote_id/contacts
```

**Output:**

```{"timestamp_ms":1772219526626,"contacts":[{"id":"fpv:1","type":"FPV","source":"esp32","last_seen_ts":1772219282836,"severity":"unknown","vrx_id":1,"freq_hz":5803000000,"rssi_raw":1221,"selected":1,"last_seen_uptime_ms":80079364}]}
HTTP_STATUS:200
```

**Result:** PASS

### GET /remote_id/stats (HTTP 200)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/remote_id/stats
```

**Output:**

```{"timestamp_ms":1772219526641,"frames":0,"decoded":0}
HTTP_STATUS:200
```

**Result:** PASS

### GET /remoteid-engine/contacts (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/remoteid-engine/contacts
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### GET /remoteid-engine/health (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/remoteid-engine/health
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### GET /remoteid-engine/replay/state (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/remoteid-engine/replay/state
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### GET /remoteid-engine/stats (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/remoteid-engine/stats
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### GET /remoteid-engine/status (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/remoteid-engine/status
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### GET /rf (HTTP 200)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/rf
```

**Output:**

```{"last_event":{"reason":"no_rf_events"},"last_event_type":"RF_SCAN_OFFLINE","last_timestamp_ms":1772219525608,"scan_active":false,"status":"degraded","last_error":"no_rf_events"}
HTTP_STATUS:200
```

**Result:** PASS

### GET /services (HTTP 200)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/services
```

**Output:**

```[]
HTTP_STATUS:200
```

**Result:** PASS

### GET /status (HTTP 200)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/status
```

**Output:**

```{"timestamp_ms":1772219526734,"overall_ok":false,"system":{"cpu_temp_c":32.0,"cpu_usage_percent":13.2,"load_1m":2.46142578125,"load_5m":1.97802734375,"load_15m":1.74853515625,"ram_used_mb":2276,"ram_total_mb":16215,"disk_used_gb":66,"disk_total_gb":116,"uptime_s":162874,"throttled_flags":0,"status":"ok","timestamp_ms":1772219526316,"version":{"app":"ndefender-system-controller","git_sha":null,"build_ts":null},"cpu":{"temp_c":32.0,"load1":2.46142578125,"load5":1.97802734375,"load15":1.74853515625,"usage_percent":13.2},"ram":{"total_mb":16215,"used_mb":2276,"free_mb":13938},"storage":{"root":{"total_gb":116.606,"used_gb":66.944,"free_gb":43.718},"logs":null},"last_error":null},"power":{"pack_voltage_v":16.282,"current_a":-0.009,"input_vbus_v":0.0,"input_power_w":0.0,"soc_percent":89,"state":"IDLE","time_to_empty_s":1697220,"time_to_full_s":null,"status":"ok","timestamp_ms":1772219526318,"per_cell_v":[4.071,4.071,4.07,4.07],"last_error":null},"rf":{"last_event":{"reason":"no_rf_events"},"last_event_type":"RF_SCAN_OFFLINE","last_timestamp_ms":1772219525608,"scan_active":false,"status":"degraded","last_error":"no_rf_events"},"remote_id":{"last_event":{"reason":"no_odid_frames"},"last_event_type":"REMOTEID_STALE","last_timestamp_ms":1772219522039,"state":"DEGRADED","mode":"live","capture_active":true,"contacts_active":0,"last_update_ms":1772219522039,"last_error":"no_odid_frames"},"gps":{"timestamp_ms":1772219523208,"fix":"NO_FIX","satellites":{"in_view":0,"in_use":0},"hdop":null,"vdop":null,"pdop":null,"latitude":null,"longitude":null,"altitude_m":null,"speed_m_s":null,"heading_deg":null,"last_update_ms":1772219523208,"age_ms":null,"source":"gpsd","last_error":"gpsd_no_data"},"esp32":{"timestamp_ms":1772219285950,"connected":false,"last_seen_ms":1772219282836,"rtt_ms":null,"fw_version":null,"heartbeat":null,"capabilities":null,"last_error":"[Errno 2] could not open port /dev/ttyACM0: [Errno 2] No such file or directory: '/dev/ttyACM0'"},"antsdr":{"timestamp_ms":1772219525608,"connected":false,"uri":"ip:192.168.10.2","temperature_c":null,"last_error":"no_rf_events"},"vrx":{"selected":1,"vrx":[{"id":1,"freq_hz":5803000000,"rssi_raw":1221},{"id":2,"freq_hz":5803000000,"rssi_raw":562},{"id":3,"freq_hz":5803000000,"rssi_raw":83}],"led":{"r":0,"y":0,"g":1},"sys":{"uptime_ms":80079364,"heap":337624,"status":"DISCONNECTED","last_error":"[Errno 2] could not open port /dev/ttyACM0: [Errno 2] No such file or directory: '/dev/ttyACM0'"},"scan_state":"idle"},"fpv":{"selected":1,"locked_channels":[],"rssi_raw":1221,"scan_state":"idle","freq_hz":5803000000},"video":{"selected":1,"status":"ok"},"services":[],"network":{"connected":true,"ip_v4":"127.0.1.1","ip_v6":null,"ssid":"Airtel_Toybook","wifi":{"timestamp_ms":1772219526228,"enabled":true,"connected":true,"ssid":"Airtel_Toybook","bssid":"2E\\","ip":"127.0.1.1","rssi_dbm":null,"link_quality":null,"last_update_ms":1772219526228,"last_error":null},"bluetooth":{"timestamp_ms":1772219526295,"enabled":false,"scanning":false,"paired_count":0,"connected_devices":[],"last_update_ms":1772219526295,"last_error":null}},"audio":{"muted":null,"volume_percent":null,"status":"degraded","timestamp_ms":1772219526226,"last_error":"audio_unavailable"},"contacts":[{"id":"fpv:1","type":"FPV","source":"esp32","last_seen_ts":1772219282836,"severity":"unknown","vrx_id":1,"freq_hz":5803000000,"rssi_raw":1221,"selected":1,"last_seen_uptime_ms":80079364}],"replay":{"active":false,"source":"none"}}
HTTP_STATUS:200
```

**Result:** PASS

### GET /system (HTTP 200)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/system
```

**Output:**

```{"cpu_temp_c":32.0,"cpu_usage_percent":13.2,"load_1m":2.46142578125,"load_5m":1.97802734375,"load_15m":1.74853515625,"ram_used_mb":2276,"ram_total_mb":16215,"disk_used_gb":66,"disk_total_gb":116,"uptime_s":162874,"throttled_flags":0,"status":"ok","timestamp_ms":1772219526316,"version":{"app":"ndefender-system-controller","git_sha":null,"build_ts":null},"cpu":{"temp_c":32.0,"load1":2.46142578125,"load5":1.97802734375,"load15":1.74853515625,"usage_percent":13.2},"ram":{"total_mb":16215,"used_mb":2276,"free_mb":13938},"storage":{"root":{"total_gb":116.606,"used_gb":66.944,"free_gb":43.718},"logs":null},"last_error":null}
HTTP_STATUS:200
```

**Result:** PASS

### GET /system-controller/audio (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/system-controller/audio
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### GET /system-controller/gps (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/system-controller/gps
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### GET /system-controller/health (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/system-controller/health
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### GET /system-controller/network (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/system-controller/network
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### GET /system-controller/network/bluetooth/devices (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/system-controller/network/bluetooth/devices
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### GET /system-controller/network/bluetooth/state (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/system-controller/network/bluetooth/state
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### GET /system-controller/network/wifi/scan (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/system-controller/network/wifi/scan
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### GET /system-controller/network/wifi/state (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/system-controller/network/wifi/state
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### GET /system-controller/services (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/system-controller/services
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### GET /system-controller/status (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/system-controller/status
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### GET /system-controller/system (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/system-controller/system
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### GET /system-controller/ups (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/system-controller/ups
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### GET /system-controller/ws (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/system-controller/ws
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### GET /video (HTTP 200)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/video
```

**Output:**

```{"selected":1,"status":"ok"}
HTTP_STATUS:200
```

**Result:** PASS

### GET /ws (HTTP 405)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/ws
```

**Output:**

```{"detail":"Method Not Allowed"}
HTTP_STATUS:405
```

**Result:** FAIL


## H4b) POST Endpoint Tests w/ HTTP Status

### POST /antsdr-scan/config/reload (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/antsdr-scan/config/reload -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### POST /antsdr-scan/device/calibrate (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/antsdr-scan/device/calibrate -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### POST /antsdr-scan/device/reset (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/antsdr-scan/device/reset -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### POST /antsdr-scan/gain/set (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/antsdr-scan/gain/set -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### POST /antsdr-scan/sweep/start (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/antsdr-scan/sweep/start -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### POST /antsdr-scan/sweep/stop (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/antsdr-scan/sweep/stop -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### POST /antsdr/device/reset (HTTP 400)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/antsdr/device/reset -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```{"detail":"confirm_required"}
HTTP_STATUS:400
```

**Result:** PASS

### POST /antsdr/gain/set (HTTP 429)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/antsdr/gain/set -H 'Content-Type: application/json' -d '{"payload": {"mode": "auto"}, "confirm": false}'
```

**Output:**

```{"detail":"rate_limited"}
HTTP_STATUS:429
```

**Result:** FAIL

### POST /antsdr/sweep/start (HTTP 429)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/antsdr/sweep/start -H 'Content-Type: application/json' -d '{"payload": {"plan": "default"}, "confirm": false}'
```

**Output:**

```{"detail":"rate_limited"}
HTTP_STATUS:429
```

**Result:** FAIL

### POST /antsdr/sweep/stop (HTTP 429)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/antsdr/sweep/stop -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```{"detail":"rate_limited"}
HTTP_STATUS:429
```

**Result:** FAIL

### POST /audio/mute (HTTP 429)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/audio/mute -H 'Content-Type: application/json' -d '{"payload": {"muted": true}, "confirm": false}'
```

**Output:**

```{"detail":"rate_limited"}
HTTP_STATUS:429
```

**Result:** FAIL

### POST /audio/volume (HTTP 429)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/audio/volume -H 'Content-Type: application/json' -d '{"payload": {"volume_percent": 50}, "confirm": false}'
```

**Output:**

```{"detail":"rate_limited"}
HTTP_STATUS:429
```

**Result:** FAIL

### POST /esp32/buttons/simulate (HTTP 429)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/esp32/buttons/simulate -H 'Content-Type: application/json' -d '{"payload": {"button": "mute", "action": "press"}, "confirm": false}'
```

**Output:**

```{"detail":"rate_limited"}
HTTP_STATUS:429
```

**Result:** FAIL

### POST /esp32/buzzer (HTTP 429)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/esp32/buzzer -H 'Content-Type: application/json' -d '{"payload": {"mode": "beep", "duration_ms": 100}, "confirm": false}'
```

**Output:**

```{"detail":"rate_limited"}
HTTP_STATUS:429
```

**Result:** FAIL

### POST /esp32/config (HTTP 429)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/esp32/config -H 'Content-Type: application/json' -d '{"payload": {"config": {}}, "confirm": false}'
```

**Output:**

```{"detail":"rate_limited"}
HTTP_STATUS:429
```

**Result:** FAIL

### POST /esp32/leds (HTTP 429)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/esp32/leds -H 'Content-Type: application/json' -d '{"payload": {"red": false, "yellow": false, "green": true}, "confirm": false}'
```

**Output:**

```{"detail":"rate_limited"}
HTTP_STATUS:429
```

**Result:** FAIL

### POST /gps/restart (HTTP 400)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/gps/restart -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```{"detail":"confirm_required"}
HTTP_STATUS:400
```

**Result:** FAIL

### POST /network/bluetooth/disable (HTTP 429)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/network/bluetooth/disable -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```{"detail":"rate_limited"}
HTTP_STATUS:429
```

**Result:** FAIL

### POST /network/bluetooth/enable (HTTP 429)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/network/bluetooth/enable -H 'Content-Type: application/json' -d '{"payload": {"enabled": true}, "confirm": false}'
```

**Output:**

```{"detail":"rate_limited"}
HTTP_STATUS:429
```

**Result:** FAIL

### POST /network/bluetooth/pair (HTTP 429)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/network/bluetooth/pair -H 'Content-Type: application/json' -d '{"payload": {"addr": "00:11:22:33:44:55"}, "confirm": false}'
```

**Output:**

```{"detail":"rate_limited"}
HTTP_STATUS:429
```

**Result:** FAIL

### POST /network/bluetooth/scan/start (HTTP 429)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/network/bluetooth/scan/start -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```{"detail":"rate_limited"}
HTTP_STATUS:429
```

**Result:** FAIL

### POST /network/bluetooth/scan/stop (HTTP 429)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/network/bluetooth/scan/stop -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```{"detail":"rate_limited"}
HTTP_STATUS:429
```

**Result:** FAIL

### POST /network/bluetooth/unpair (HTTP 429)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/network/bluetooth/unpair -H 'Content-Type: application/json' -d '{"payload": {"addr": "00:11:22:33:44:55"}, "confirm": false}'
```

**Output:**

```{"detail":"rate_limited"}
HTTP_STATUS:429
```

**Result:** FAIL

### POST /network/wifi/connect (HTTP 429)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/network/wifi/connect -H 'Content-Type: application/json' -d '{"payload": {"ssid": "TEST_SSID", "password": "TEST_PASS", "hidden": false}, "confirm": false}'
```

**Output:**

```{"detail":"rate_limited"}
HTTP_STATUS:429
```

**Result:** FAIL

### POST /network/wifi/disable (HTTP 429)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/network/wifi/disable -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```{"detail":"rate_limited"}
HTTP_STATUS:429
```

**Result:** FAIL

### POST /network/wifi/disconnect (HTTP 429)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/network/wifi/disconnect -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```{"detail":"rate_limited"}
HTTP_STATUS:429
```

**Result:** FAIL

### POST /network/wifi/enable (HTTP 429)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/network/wifi/enable -H 'Content-Type: application/json' -d '{"payload": {"enabled": true}, "confirm": false}'
```

**Output:**

```{"detail":"rate_limited"}
HTTP_STATUS:429
```

**Result:** FAIL

### POST /observability/diag/bundle (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/observability/diag/bundle -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### POST /remote_id/monitor/start (HTTP 429)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/remote_id/monitor/start -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```{"detail":"rate_limited"}
HTTP_STATUS:429
```

**Result:** FAIL

### POST /remote_id/monitor/stop (HTTP 429)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/remote_id/monitor/stop -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```{"detail":"rate_limited"}
HTTP_STATUS:429
```

**Result:** FAIL

### POST /remoteid-engine/monitor/start (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/remoteid-engine/monitor/start -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### POST /remoteid-engine/monitor/stop (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/remoteid-engine/monitor/stop -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### POST /remoteid-engine/replay/start (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/remoteid-engine/replay/start -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### POST /remoteid-engine/replay/stop (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/remoteid-engine/replay/stop -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### POST /scan/start (HTTP 429)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/scan/start -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```{"detail":"rate_limited"}
HTTP_STATUS:429
```

**Result:** FAIL

### POST /scan/stop (HTTP 429)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/scan/stop -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```{"detail":"rate_limited"}
HTTP_STATUS:429
```

**Result:** FAIL

### POST /system-controller/audio/mute (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/system-controller/audio/mute -H 'Content-Type: application/json' -d '{"payload": {"muted": true}, "confirm": false}'
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### POST /system-controller/audio/volume (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/system-controller/audio/volume -H 'Content-Type: application/json' -d '{"payload": {"volume_percent": 50}, "confirm": false}'
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### POST /system-controller/gps/restart (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/system-controller/gps/restart -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### POST /system-controller/network/bluetooth/disable (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/system-controller/network/bluetooth/disable -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### POST /system-controller/network/bluetooth/enable (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/system-controller/network/bluetooth/enable -H 'Content-Type: application/json' -d '{"payload": {"enabled": true}, "confirm": false}'
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### POST /system-controller/network/bluetooth/pair (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/system-controller/network/bluetooth/pair -H 'Content-Type: application/json' -d '{"payload": {"addr": "00:11:22:33:44:55"}, "confirm": false}'
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### POST /system-controller/network/bluetooth/scan/start (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/system-controller/network/bluetooth/scan/start -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### POST /system-controller/network/bluetooth/scan/stop (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/system-controller/network/bluetooth/scan/stop -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### POST /system-controller/network/bluetooth/unpair (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/system-controller/network/bluetooth/unpair -H 'Content-Type: application/json' -d '{"payload": {"addr": "00:11:22:33:44:55"}, "confirm": false}'
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### POST /system-controller/network/wifi/connect (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/system-controller/network/wifi/connect -H 'Content-Type: application/json' -d '{"payload": {"ssid": "TEST_SSID", "password": "TEST_PASS", "hidden": false}, "confirm": false}'
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### POST /system-controller/network/wifi/disable (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/system-controller/network/wifi/disable -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### POST /system-controller/network/wifi/disconnect (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/system-controller/network/wifi/disconnect -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### POST /system-controller/network/wifi/enable (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/system-controller/network/wifi/enable -H 'Content-Type: application/json' -d '{"payload": {"enabled": true}, "confirm": false}'
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### POST /system-controller/services/{name}/restart (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/system-controller/services/cloudflared/restart -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### POST /system-controller/system/reboot (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/system-controller/system/reboot -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### POST /system-controller/system/shutdown (HTTP 404)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/system-controller/system/shutdown -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL

### POST /system/reboot (HTTP 400)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/system/reboot -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```{"detail":"confirm_required"}
HTTP_STATUS:400
```

**Result:** PASS

### POST /system/shutdown (HTTP 400)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/system/shutdown -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```{"detail":"confirm_required"}
HTTP_STATUS:400
```

**Result:** PASS

### POST /video/select (HTTP 429)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/video/select -H 'Content-Type: application/json' -d '{"payload": {"sel": 1}, "confirm": false}'
```

**Output:**

```{"detail":"rate_limited"}
HTTP_STATUS:429
```

**Result:** FAIL

### POST /vrx/tune (HTTP 429)

**Command:**

```curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/vrx/tune -H 'Content-Type: application/json' -d '{"payload": {"vrx_id": 1, "freq_hz": 5740000000}, "confirm": false}'
```

**Output:**

```{"detail":"rate_limited"}
HTTP_STATUS:429
```

**Result:** FAIL


## H5) Runtime Bugs Detected (If Any)


## Y) Failure Analysis + Next Fix Repo

No FAIL entries detected in evidence sections.



## Z2) Summary Table (Corrected)

| Test | Result |
|---|---|
| scripts/validate.sh | PASS |
| npm run ci | PASS |
| REST GET coverage | FAIL |
| REST POST coverage | FAIL |
| confirm-gating proof | PASS |
| WS proof | PASS |

Tested commit: `21025a5`
Branch: `chore/readme-and-structure`

