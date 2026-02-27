# N-Defender Test Results — 2026-02-27 (Revision 2)

Generated: 2026-02-28 00:53:00 

**IMPORTANT:** This repo contains contracts/docs/validation only; tests were run on the Raspberry Pi against deployed services (not a local setup guide).

Canonical base: `/api/v1`
Ports: 8001 (Aggregator), 8002 (System Controller), 8890 (RFScan). Legacy 8000 must be absent.


## 0) What Was Wrong With the Previous Report

The previous report was incomplete because it executed many endpoints only via the Aggregator base, which produced 404s for upstream-owned routes. It also lacked direct-owner comparisons and field-level contract checks for UI readiness, and did not clearly classify gaps as upstream vs proxy.

## 1) Baseline Snapshot

### uname -a

**Command:**

```
uname -a
```

**Output:**

```
Linux ndefender-pi 6.12.62+rpt-rpi-2712 #1 SMP PREEMPT Debian 1:6.12.62-1+rpt1~bookworm (2026-01-19) aarch64 GNU/Linux
```

**Result:** PASS

### hostname

**Command:**

```
hostname
```

**Output:**

```
ndefender-pi
```

**Result:** PASS

### date (IST)

**Command:**

```
TZ=Asia/Kolkata date
```

**Output:**

```
Sat Feb 28 00:53:00 IST 2026
```

**Result:** PASS

### ports

**Command:**

```
ss -lntp | egrep '(:8000|:8001|:8002|:8890)\b' || true
```

**Output:**

```
LISTEN 0      128                      127.0.0.1:8890       0.0.0.0:*    users:(("ndefender-antsd",pid=2071035,fd=6))
LISTEN 0      2048                     127.0.0.1:8001       0.0.0.0:*    users:(("uvicorn",pid=2076223,fd=7))        
LISTEN 0      2048                     127.0.0.1:8002       0.0.0.0:*    users:(("uvicorn",pid=2076239,fd=14))
```

**Result:** PASS

### systemctl is-active

**Command:**

```
systemctl is-active ndefender-backend-aggregator ndefender-system-controller ndefender-rfscan ndefender-remoteid-engine
```

**Output:**

```
active
active
active
active
```

**Result:** PASS

### systemctl is-enabled

**Command:**

```
systemctl is-enabled ndefender-backend-aggregator ndefender-system-controller ndefender-rfscan ndefender-remoteid-engine
```

**Output:**

```
enabled
enabled
enabled
enabled
```

**Result:** PASS

### git status -sb

**Command:**

```
git -C /home/toybook/ndefender-api-contracts status -sb
```

**Output:**

```
## chore/readme-and-structure...origin/chore/readme-and-structure
 M docs/TEST_RESULTS_2026-02-27.md
?? scripts/run_full_evidence.py
```

**Result:** PASS

### git rev-parse --short HEAD

**Command:**

```
git -C /home/toybook/ndefender-api-contracts rev-parse --short HEAD
```

**Output:**

```
3de7786
```

**Result:** PASS

### node -v

**Command:**

```
node -v
```

**Output:**

```
v20.20.0
```

**Result:** PASS

### npm -v

**Command:**

```
npm -v
```

**Output:**

```
10.8.2
```

**Result:** PASS

### python3 --version

**Command:**

```
python3 --version
```

**Output:**

```
Python 3.11.2
```

**Result:** PASS


## 2) Repo Validation

### scripts/validate.sh

**Command:**

```
cd /home/toybook/ndefender-api-contracts && scripts/validate.sh
```

**Output:**

```
PASS
```

**Result:** PASS

### npm run ci

**Command:**

```
cd /home/toybook/ndefender-api-contracts && npm run ci
```

**Output:**

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

**Result:** PASS


## 3) Endpoint Coverage — GET /health

### GET /health
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/health
```

**Output:**

```
{"status":"ok","timestamp_ms":1772220187630}
HTTP_STATUS:200
```

**Result:** PASS


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** PASS


## 3) Endpoint Coverage — GET /status

### GET /status
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/status
```

**Output:**

```
{"timestamp_ms":1772220187644,"overall_ok":false,"system":{"cpu_temp_c":32.0,"cpu_usage_percent":47.5,"load_1m":2.50927734375,"load_5m":1.8994140625,"load_15m":1.77783203125,"ram_used_mb":2464,"ram_total_mb":16215,"disk_used_gb":66,"disk_total_gb":116,"uptime_s":163534,"throttled_flags":0,"status":"ok","timestamp_ms":1772220186761,"version":{"app":"ndefender-system-controller","git_sha":null,"build_ts":null},"cpu":{"temp_c":32.0,"load1":2.50927734375,"load5":1.8994140625,"load15":1.77783203125,"usage_percent":47.5},"ram":{"total_mb":16215,"used_mb":2464,"free_mb":13750},"storage":{"root":{"total_gb":116.606,"used_gb":66.995,"free_gb":43.667},"logs":null},"last_error":null},"power":{"pack_voltage_v":16.28,"current_a":-0.008,"input_vbus_v":0.0,"input_power_w":0.0,"soc_percent":89,"state":"IDLE","time_to_empty_s":1908480,"time_to_full_s":null,"status":"ok","timestamp_ms":1772220186765,"per_cell_v":[4.07,4.07,4.069,4.07],"last_error":null},"rf":{"last_event":{"reason":"no_rf_events"},"last_event_type":"RF_SCAN_OFFLINE","last_timestamp_ms":1772220187144,"scan_active":false,"status":"degraded","last_error":"no_rf_events"},"remote_id":{"last_event":{"reason":"no_odid_frames"},"last_event_type":"REMOTEID_STALE","last_timestamp_ms":1772220182836,"state":"DEGRADED","mode":"live","capture_active":true,"contacts_active":0,"last_update_ms":1772220182836,"last_error":"no_odid_frames"},"gps":{"timestamp_ms":1772220179627,"fix":"NO_FIX","satellites":{"in_view":0,"in_use":0},"hdop":null,"vdop":null,"pdop":null,"latitude":null,"longitude":null,"altitude_m":null,"speed_m_s":null,"heading_deg":null,"last_update_ms":1772220179627,"age_ms":null,"source":"gpsd","last_error":"gpsd_no_data"},"esp32":{"timestamp_ms":1772219285950,"connected":false,"last_seen_ms":1772219282836,"rtt_ms":null,"fw_version":null,"heartbeat":null,"capabilities":null,"last_error":"[Errno 2] could not open port /dev/ttyACM0: [Errno 2] No such file or directory: '/dev/ttyACM0'"},"antsdr":{"timestamp_ms":1772220187144,"connected":false,"uri":"ip:192.168.10.2","temperature_c":null,"last_error":"no_rf_events"},"vrx":{"selected":1,"vrx":[{"id":1,"freq_hz":5803000000,"rssi_raw":1221},{"id":2,"freq_hz":5803000000,"rssi_raw":562},{"id":3,"freq_hz":5803000000,"rssi_raw":83}],"led":{"r":0,"y":0,"g":1},"sys":{"uptime_ms":80079364,"heap":337624,"status":"DISCONNECTED","last_error":"[Errno 2] could not open port /dev/ttyACM0: [Errno 2] No such file or directory: '/dev/ttyACM0'"},"scan_state":"idle"},"fpv":{"selected":1,"locked_channels":[],"rssi_raw":1221,"scan_state":"idle","freq_hz":5803000000},"video":{"selected":1,"status":"ok"},"services":[],"network":{"connected":true,"ip_v4":"127.0.1.1","ip_v6":null,"ssid":"Airtel_Toybook","wifi":{"timestamp_ms":1772220182647,"enabled":true,"connected":true,"ssid":"Airtel_Toybook","bssid":"2E\\","ip":"127.0.1.1","rssi_dbm":null,"link_quality":null,"last_update_ms":1772220182647,"last_error":null},"bluetooth":{"timestamp_ms":1772220182732,"enabled":false,"scanning":false,"paired_count":0,"connected_devices":[],"last_update_ms":1772220182732,"last_error":null}},"audio":{"muted":null,"volume_percent":null,"status":"degraded","timestamp_ms":1772220182646,"last_error":"audio_unavailable"},"contacts":[{"id":"fpv:1","type":"FPV","source":"esp32","last_seen_ts":1772219282836,"severity":"unknown","vrx_id":1,"freq_hz":5803000000,"rssi_raw":1221,"selected":1,"last_seen_uptime_ms":80079364}],"replay":{"active":false,"source":"none"}}
HTTP_STATUS:200
```

**Result:** PASS


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** PASS


## 3) Endpoint Coverage — GET /contacts

### GET /contacts
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/contacts
```

**Output:**

```
{"contacts":[{"id":"fpv:1","type":"FPV","source":"esp32","last_seen_ts":1772219282836,"severity":"unknown","vrx_id":1,"freq_hz":5803000000,"rssi_raw":1221,"selected":1,"last_seen_uptime_ms":80079364}]}
HTTP_STATUS:200
```

**Result:** PASS


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** PASS


## 3) Endpoint Coverage — GET /system

### GET /system
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8002/api/v1/system
```

**Output:**

```
{"timestamp_ms":1772220190781,"status":"ok","uptime_s":163538,"version":{"app":"ndefender-system-controller","git_sha":null,"build_ts":null},"cpu":{"temp_c":31.4,"load1":2.38818359375,"load5":1.88427734375,"load15":1.7734375,"usage_percent":16.3},"ram":{"total_mb":16215,"used_mb":2359,"free_mb":13855},"storage":{"root":{"total_gb":116.606,"used_gb":66.995,"free_gb":43.667},"logs":null},"last_error":null,"cpu_temp_c":31.4,"cpu_usage_percent":16.3,"load_1m":2.38818359375,"load_5m":1.88427734375,"load_15m":1.7734375,"ram_used_mb":2359,"ram_total_mb":16215,"disk_used_gb":66,"disk_total_gb":116,"throttled_flags":0}
HTTP_STATUS:200
```

**Result:** PASS


**Aggregator proxy check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/system
```

**Output:**

```
{"cpu_temp_c":31.4,"cpu_usage_percent":16.3,"load_1m":2.38818359375,"load_5m":1.88427734375,"load_15m":1.7734375,"ram_used_mb":2359,"ram_total_mb":16215,"disk_used_gb":66,"disk_total_gb":116,"uptime_s":163538,"throttled_flags":0,"status":"ok","timestamp_ms":1772220190781,"version":{"app":"ndefender-system-controller","git_sha":null,"build_ts":null},"cpu":{"temp_c":31.4,"load1":2.38818359375,"load5":1.88427734375,"load15":1.7734375,"usage_percent":16.3},"ram":{"total_mb":16215,"used_mb":2359,"free_mb":13855},"storage":{"root":{"total_gb":116.606,"used_gb":66.995,"free_gb":43.667},"logs":null},"last_error":null}
HTTP_STATUS:200
```

**Result:** PASS


**Classification:** PASS


## 3) Endpoint Coverage — GET /power

### GET /power
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8002/api/v1/power
```

**Output:**

```
{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL


**Aggregator proxy check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/power
```

**Output:**

```
{"pack_voltage_v":16.28,"current_a":-0.009,"input_vbus_v":0.0,"input_power_w":0.0,"soc_percent":89,"state":"IDLE","time_to_empty_s":1696380,"time_to_full_s":null,"status":"ok","timestamp_ms":1772220190783,"per_cell_v":[4.07,4.07,4.07,4.07],"last_error":null}
HTTP_STATUS:200
```

**Result:** PASS


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — GET /rf

### GET /rf
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8890/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8890/api/v1/rf
```

**Output:**

```
404: Not Found
HTTP_STATUS:404
```

**Result:** FAIL


**Aggregator proxy check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/rf
```

**Output:**

```
{"last_event":{"reason":"no_rf_events"},"last_event_type":"RF_SCAN_OFFLINE","last_timestamp_ms":1772220187144,"scan_active":false,"status":"degraded","last_error":"no_rf_events"}
HTTP_STATUS:200
```

**Result:** PASS


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — GET /video

### GET /video
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/video
```

**Output:**

```
{"selected":1,"status":"ok"}
HTTP_STATUS:200
```

**Result:** PASS


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** PASS


## 3) Endpoint Coverage — GET /services

### GET /services
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8002/api/v1/services
```

**Output:**

```
[]
HTTP_STATUS:200
```

**Result:** PASS


**Aggregator proxy check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/services
```

**Output:**

```
[]
HTTP_STATUS:200
```

**Result:** PASS


**Classification:** PASS


## 3) Endpoint Coverage — GET /network

### GET /network
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8002/api/v1/network
```

**Output:**

```
{"connected":true,"ssid":"Airtel_Toybook","ip_v4":"127.0.1.1","ip_v6":null,"wifi":{"timestamp_ms":1772220190656,"enabled":true,"connected":true,"ssid":"Airtel_Toybook","bssid":"2E\\","ip":"127.0.1.1","rssi_dbm":null,"link_quality":null,"last_update_ms":1772220190656,"last_error":null},"bluetooth":{"timestamp_ms":1772220190753,"enabled":false,"scanning":false,"paired_count":0,"connected_devices":[],"last_update_ms":1772220190753,"last_error":null}}
HTTP_STATUS:200
```

**Result:** PASS


**Aggregator proxy check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/network
```

**Output:**

```
{"connected":true,"ip_v4":"127.0.1.1","ip_v6":null,"ssid":"Airtel_Toybook","wifi":{"timestamp_ms":1772220190656,"enabled":true,"connected":true,"ssid":"Airtel_Toybook","bssid":"2E\\","ip":"127.0.1.1","rssi_dbm":null,"link_quality":null,"last_update_ms":1772220190656,"last_error":null},"bluetooth":{"timestamp_ms":1772220190753,"enabled":false,"scanning":false,"paired_count":0,"connected_devices":[],"last_update_ms":1772220190753,"last_error":null}}
HTTP_STATUS:200
```

**Result:** PASS


**Classification:** PASS


## 3) Endpoint Coverage — GET /audio

### GET /audio
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8002/api/v1/audio
```

**Output:**

```
{"timestamp_ms":1772220190655,"status":"degraded","volume_percent":null,"muted":null,"last_error":"audio_unavailable"}
HTTP_STATUS:200
```

**Result:** PASS


**Aggregator proxy check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/audio
```

**Output:**

```
{"muted":null,"volume_percent":null,"status":"degraded","timestamp_ms":1772220190655,"last_error":"audio_unavailable"}
HTTP_STATUS:200
```

**Result:** PASS


**Classification:** PASS


## 3) Endpoint Coverage — GET /network/wifi/state

### GET /network/wifi/state
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8002/api/v1/network/wifi/state
```

**Output:**

```
{"timestamp_ms":1772220190955,"enabled":true,"connected":true,"ssid":"Airtel_Toybook","bssid":"2E\\","ip":"127.0.1.1","rssi_dbm":null,"link_quality":null,"last_update_ms":1772220190955,"last_error":null}
HTTP_STATUS:200
```

**Result:** PASS


**Aggregator proxy check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/network/wifi/state
```

**Output:**

```
{"timestamp_ms":1772220191031,"enabled":true,"connected":true,"ssid":"Airtel_Toybook","bssid":"2E\\","ip":"127.0.1.1","rssi_dbm":null,"link_quality":null,"last_update_ms":1772220191031,"last_error":null}
HTTP_STATUS:200
```

**Result:** PASS


**Classification:** PASS


## 3) Endpoint Coverage — GET /network/wifi/scan

### GET /network/wifi/scan
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8002/api/v1/network/wifi/scan
```

**Output:**

```
{"timestamp_ms":1772220191123,"networks":[{"ssid":"Airtel_Toybook","bssid":"2E\\","security":"C1\\"}],"last_error":null}
HTTP_STATUS:200
```

**Result:** PASS


**Aggregator proxy check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/network/wifi/scan
```

**Output:**

```
{"timestamp_ms":1772220191214,"networks":[{"ssid":"Airtel_Toybook","bssid":"2E\\","security":"C1\\"}],"last_error":null}
HTTP_STATUS:200
```

**Result:** PASS


**Classification:** PASS


## 3) Endpoint Coverage — GET /network/bluetooth/state

### GET /network/bluetooth/state
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8002/api/v1/network/bluetooth/state
```

**Output:**

```
{"timestamp_ms":1772220191287,"enabled":false,"scanning":false,"paired_count":0,"connected_devices":[],"last_update_ms":1772220191287,"last_error":null}
HTTP_STATUS:200
```

**Result:** PASS


**Aggregator proxy check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/network/bluetooth/state
```

**Output:**

```
{"timestamp_ms":1772220191323,"enabled":false,"scanning":false,"paired_count":0,"connected_devices":[],"last_update_ms":1772220191323,"last_error":null}
HTTP_STATUS:200
```

**Result:** PASS


**Classification:** PASS


## 3) Endpoint Coverage — GET /network/bluetooth/devices

### GET /network/bluetooth/devices
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8002/api/v1/network/bluetooth/devices
```

**Output:**

```
{"timestamp_ms":1772220191361,"devices":[]}
HTTP_STATUS:200
```

**Result:** PASS


**Aggregator proxy check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/network/bluetooth/devices
```

**Output:**

```
{"timestamp_ms":1772220191390,"devices":[]}
HTTP_STATUS:200
```

**Result:** PASS


**Classification:** PASS


## 3) Endpoint Coverage — GET /gps

### GET /gps
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8002/api/v1/gps
```

**Output:**

```
{"timestamp_ms":1772220191418,"fix":"NO_FIX","satellites":{"in_view":0,"in_use":0},"hdop":null,"vdop":null,"pdop":null,"latitude":null,"longitude":null,"altitude_m":null,"speed_m_s":null,"heading_deg":null,"last_update_ms":1772220191418,"age_ms":null,"source":"gpsd","last_error":"gpsd_no_data"}
HTTP_STATUS:200
```

**Result:** PASS


**Aggregator proxy check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/gps
```

**Output:**

```
{"timestamp_ms":1772220187631,"fix":"NO_FIX","satellites":{"in_view":0,"in_use":0},"hdop":null,"vdop":null,"pdop":null,"latitude":null,"longitude":null,"altitude_m":null,"speed_m_s":null,"heading_deg":null,"last_update_ms":1772220187631,"age_ms":null,"source":"gpsd","last_error":"gpsd_no_data"}
HTTP_STATUS:200
```

**Result:** PASS


**Classification:** PASS


## 3) Endpoint Coverage — GET /esp32

### GET /esp32
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/esp32
```

**Output:**

```
{"timestamp_ms":1772219285950,"connected":false,"last_seen_ms":1772219282836,"rtt_ms":null,"fw_version":null,"heartbeat":null,"capabilities":null,"last_error":"[Errno 2] could not open port /dev/ttyACM0: [Errno 2] No such file or directory: '/dev/ttyACM0'"}
HTTP_STATUS:200
```

**Result:** PASS


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** PASS


## 3) Endpoint Coverage — GET /esp32/config

### GET /esp32/config
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/esp32/config
```

**Output:**

```
{"timestamp_ms":1772220194459,"schema_version":null,"config":{}}
HTTP_STATUS:200
```

**Result:** PASS


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** PASS


## 3) Endpoint Coverage — POST /esp32/config

### POST /esp32/config
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -X POST http://127.0.0.1:8001/api/v1/esp32/config -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```

**Output:**

```
SKIPPED (NEEDS REAL INPUT / OPERATOR APPROVAL)
```

**Result:** SKIP


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** SKIP (NEEDS REAL INPUT/OWNER NOT EXPOSED)


## 3) Endpoint Coverage — GET /antsdr

### GET /antsdr
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8890/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8890/api/v1/antsdr
```

**Output:**

```
404: Not Found
HTTP_STATUS:404
```

**Result:** FAIL


**Aggregator proxy check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/antsdr
```

**Output:**

```
{"timestamp_ms":1772220192151,"connected":false,"uri":"ip:192.168.10.2","temperature_c":null,"last_error":"no_rf_events"}
HTTP_STATUS:200
```

**Result:** PASS


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — GET /antsdr/sweep/state

### GET /antsdr/sweep/state
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8890/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8890/api/v1/antsdr/sweep/state
```

**Output:**

```
404: Not Found
HTTP_STATUS:404
```

**Result:** FAIL


**Aggregator proxy check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/antsdr/sweep/state
```

**Output:**

```
{"timestamp_ms":1772220194506,"running":false,"active_plan":"5G8_RaceBand","plans":[{"name":"5G8_RaceBand","start_hz":5658000000.0,"end_hz":5917000000.0,"step_hz":2000000.0},{"name":"5G8_FatShark","start_hz":5733000000.0,"end_hz":5866000000.0,"step_hz":2000000.0},{"name":"5G8_BandA","start_hz":5865000000.0,"end_hz":5945000000.0,"step_hz":2000000.0},{"name":"5G8_Digital","start_hz":5725000000.0,"end_hz":5850000000.0,"step_hz":2000000.0},{"name":"2G4_Control","start_hz":2400000000.0,"end_hz":2483500000.0,"step_hz":1000000.0},{"name":"915_Control","start_hz":902000000.0,"end_hz":928000000.0,"step_hz":1000000.0}],"last_update_ms":1772220194506,"last_error":"pyadi-iio is required for AntSDR access"}
HTTP_STATUS:200
```

**Result:** PASS


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — GET /antsdr/gain

### GET /antsdr/gain
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8890/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8890/api/v1/antsdr/gain
```

**Output:**

```
404: Not Found
HTTP_STATUS:404
```

**Result:** FAIL


**Aggregator proxy check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/antsdr/gain
```

**Output:**

```
{"timestamp_ms":1772220194532,"mode":"auto"}
HTTP_STATUS:200
```

**Result:** PASS


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — GET /antsdr/stats

### GET /antsdr/stats
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8890/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8890/api/v1/antsdr/stats
```

**Output:**

```
404: Not Found
HTTP_STATUS:404
```

**Result:** FAIL


**Aggregator proxy check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/antsdr/stats
```

**Output:**

```
{"timestamp_ms":1772220194555,"frames_processed":0,"events_emitted":0,"last_event_timestamp_ms":0}
HTTP_STATUS:200
```

**Result:** PASS


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — GET /remote_id

### GET /remote_id
**Owner tag:** Aggregator
**Owner base:** N/A (owner not exposed)

**Direct-owner check:**

SKIPPED (DIRECT OWNER NOT EXPOSED IN PORT LIST)


**Aggregator proxy check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/remote_id
```

**Output:**

```
{"last_event":{"reason":"no_odid_frames"},"last_event_type":"REMOTEID_STALE","last_timestamp_ms":1772220192941,"state":"DEGRADED","mode":"live","capture_active":true,"contacts_active":0,"last_update_ms":1772220192941,"last_error":"no_odid_frames","timestamp_ms":1772220194570}
HTTP_STATUS:200
```

**Result:** PASS


**Classification:** PASS


## 3) Endpoint Coverage — GET /remote_id/contacts

### GET /remote_id/contacts
**Owner tag:** Aggregator
**Owner base:** N/A (owner not exposed)

**Direct-owner check:**

SKIPPED (DIRECT OWNER NOT EXPOSED IN PORT LIST)


**Aggregator proxy check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/remote_id/contacts
```

**Output:**

```
{"timestamp_ms":1772220194581,"contacts":[{"id":"fpv:1","type":"FPV","source":"esp32","last_seen_ts":1772219282836,"severity":"unknown","vrx_id":1,"freq_hz":5803000000,"rssi_raw":1221,"selected":1,"last_seen_uptime_ms":80079364}]}
HTTP_STATUS:200
```

**Result:** PASS


**Classification:** PASS


## 3) Endpoint Coverage — GET /remote_id/stats

### GET /remote_id/stats
**Owner tag:** Aggregator
**Owner base:** N/A (owner not exposed)

**Direct-owner check:**

SKIPPED (DIRECT OWNER NOT EXPOSED IN PORT LIST)


**Aggregator proxy check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/remote_id/stats
```

**Output:**

```
{"timestamp_ms":1772220194594,"frames":0,"decoded":0}
HTTP_STATUS:200
```

**Result:** PASS


**Classification:** PASS


## 3) Endpoint Coverage — POST /audio/mute

### POST /audio/mute
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -X POST http://127.0.0.1:8002/api/v1/audio/mute -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```

**Output:**

```
SKIPPED (NEEDS REAL INPUT / OPERATOR APPROVAL)
```

**Result:** SKIP


**Aggregator proxy check:**

**Command:**

```
curl -sS -X POST http://127.0.0.1:8001/api/v1/audio/mute -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```

**Output:**

```
SKIPPED (NEEDS REAL INPUT / OPERATOR APPROVAL)
```

**Result:** SKIP


**Classification:** SKIP (NEEDS REAL INPUT/OWNER NOT EXPOSED)


## 3) Endpoint Coverage — POST /audio/volume

### POST /audio/volume
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -X POST http://127.0.0.1:8002/api/v1/audio/volume -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```

**Output:**

```
SKIPPED (NEEDS REAL INPUT / OPERATOR APPROVAL)
```

**Result:** SKIP


**Aggregator proxy check:**

**Command:**

```
curl -sS -X POST http://127.0.0.1:8001/api/v1/audio/volume -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```

**Output:**

```
SKIPPED (NEEDS REAL INPUT / OPERATOR APPROVAL)
```

**Result:** SKIP


**Classification:** SKIP (NEEDS REAL INPUT/OWNER NOT EXPOSED)


## 3) Endpoint Coverage — POST /network/wifi/enable

### POST /network/wifi/enable
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -X POST http://127.0.0.1:8002/api/v1/network/wifi/enable -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```

**Output:**

```
SKIPPED (NEEDS REAL INPUT / OPERATOR APPROVAL)
```

**Result:** SKIP


**Aggregator proxy check:**

**Command:**

```
curl -sS -X POST http://127.0.0.1:8001/api/v1/network/wifi/enable -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```

**Output:**

```
SKIPPED (NEEDS REAL INPUT / OPERATOR APPROVAL)
```

**Result:** SKIP


**Classification:** SKIP (NEEDS REAL INPUT/OWNER NOT EXPOSED)


## 3) Endpoint Coverage — POST /network/wifi/disable

### POST /network/wifi/disable
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -X POST http://127.0.0.1:8002/api/v1/network/wifi/disable -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```

**Output:**

```
SKIPPED (NEEDS REAL INPUT / OPERATOR APPROVAL)
```

**Result:** SKIP


**Aggregator proxy check:**

**Command:**

```
curl -sS -X POST http://127.0.0.1:8001/api/v1/network/wifi/disable -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```

**Output:**

```
SKIPPED (NEEDS REAL INPUT / OPERATOR APPROVAL)
```

**Result:** SKIP


**Classification:** SKIP (NEEDS REAL INPUT/OWNER NOT EXPOSED)


## 3) Endpoint Coverage — POST /network/wifi/connect

### POST /network/wifi/connect
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -X POST http://127.0.0.1:8002/api/v1/network/wifi/connect -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```

**Output:**

```
SKIPPED (NEEDS REAL INPUT / OPERATOR APPROVAL)
```

**Result:** SKIP


**Aggregator proxy check:**

**Command:**

```
curl -sS -X POST http://127.0.0.1:8001/api/v1/network/wifi/connect -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```

**Output:**

```
SKIPPED (NEEDS REAL INPUT / OPERATOR APPROVAL)
```

**Result:** SKIP


**Classification:** SKIP (NEEDS REAL INPUT/OWNER NOT EXPOSED)


## 3) Endpoint Coverage — POST /network/wifi/disconnect

### POST /network/wifi/disconnect
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -X POST http://127.0.0.1:8002/api/v1/network/wifi/disconnect -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```

**Output:**

```
SKIPPED (NEEDS REAL INPUT / OPERATOR APPROVAL)
```

**Result:** SKIP


**Aggregator proxy check:**

**Command:**

```
curl -sS -X POST http://127.0.0.1:8001/api/v1/network/wifi/disconnect -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```

**Output:**

```
SKIPPED (NEEDS REAL INPUT / OPERATOR APPROVAL)
```

**Result:** SKIP


**Classification:** SKIP (NEEDS REAL INPUT/OWNER NOT EXPOSED)


## 3) Endpoint Coverage — POST /network/bluetooth/enable

### POST /network/bluetooth/enable
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -X POST http://127.0.0.1:8002/api/v1/network/bluetooth/enable -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```

**Output:**

```
SKIPPED (NEEDS REAL INPUT / OPERATOR APPROVAL)
```

**Result:** SKIP


**Aggregator proxy check:**

**Command:**

```
curl -sS -X POST http://127.0.0.1:8001/api/v1/network/bluetooth/enable -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```

**Output:**

```
SKIPPED (NEEDS REAL INPUT / OPERATOR APPROVAL)
```

**Result:** SKIP


**Classification:** SKIP (NEEDS REAL INPUT/OWNER NOT EXPOSED)


## 3) Endpoint Coverage — POST /network/bluetooth/disable

### POST /network/bluetooth/disable
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -X POST http://127.0.0.1:8002/api/v1/network/bluetooth/disable -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```

**Output:**

```
SKIPPED (NEEDS REAL INPUT / OPERATOR APPROVAL)
```

**Result:** SKIP


**Aggregator proxy check:**

**Command:**

```
curl -sS -X POST http://127.0.0.1:8001/api/v1/network/bluetooth/disable -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```

**Output:**

```
SKIPPED (NEEDS REAL INPUT / OPERATOR APPROVAL)
```

**Result:** SKIP


**Classification:** SKIP (NEEDS REAL INPUT/OWNER NOT EXPOSED)


## 3) Endpoint Coverage — POST /network/bluetooth/scan/start

### POST /network/bluetooth/scan/start
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -X POST http://127.0.0.1:8002/api/v1/network/bluetooth/scan/start -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```

**Output:**

```
SKIPPED (NEEDS REAL INPUT / OPERATOR APPROVAL)
```

**Result:** SKIP


**Aggregator proxy check:**

**Command:**

```
curl -sS -X POST http://127.0.0.1:8001/api/v1/network/bluetooth/scan/start -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```

**Output:**

```
SKIPPED (NEEDS REAL INPUT / OPERATOR APPROVAL)
```

**Result:** SKIP


**Classification:** SKIP (NEEDS REAL INPUT/OWNER NOT EXPOSED)


## 3) Endpoint Coverage — POST /network/bluetooth/scan/stop

### POST /network/bluetooth/scan/stop
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -X POST http://127.0.0.1:8002/api/v1/network/bluetooth/scan/stop -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```

**Output:**

```
SKIPPED (NEEDS REAL INPUT / OPERATOR APPROVAL)
```

**Result:** SKIP


**Aggregator proxy check:**

**Command:**

```
curl -sS -X POST http://127.0.0.1:8001/api/v1/network/bluetooth/scan/stop -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```

**Output:**

```
SKIPPED (NEEDS REAL INPUT / OPERATOR APPROVAL)
```

**Result:** SKIP


**Classification:** SKIP (NEEDS REAL INPUT/OWNER NOT EXPOSED)


## 3) Endpoint Coverage — POST /network/bluetooth/pair

### POST /network/bluetooth/pair
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -X POST http://127.0.0.1:8002/api/v1/network/bluetooth/pair -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```

**Output:**

```
SKIPPED (NEEDS REAL INPUT / OPERATOR APPROVAL)
```

**Result:** SKIP


**Aggregator proxy check:**

**Command:**

```
curl -sS -X POST http://127.0.0.1:8001/api/v1/network/bluetooth/pair -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```

**Output:**

```
SKIPPED (NEEDS REAL INPUT / OPERATOR APPROVAL)
```

**Result:** SKIP


**Classification:** SKIP (NEEDS REAL INPUT/OWNER NOT EXPOSED)


## 3) Endpoint Coverage — POST /network/bluetooth/unpair

### POST /network/bluetooth/unpair
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -X POST http://127.0.0.1:8002/api/v1/network/bluetooth/unpair -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```

**Output:**

```
SKIPPED (NEEDS REAL INPUT / OPERATOR APPROVAL)
```

**Result:** SKIP


**Aggregator proxy check:**

**Command:**

```
curl -sS -X POST http://127.0.0.1:8001/api/v1/network/bluetooth/unpair -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```

**Output:**

```
SKIPPED (NEEDS REAL INPUT / OPERATOR APPROVAL)
```

**Result:** SKIP


**Classification:** SKIP (NEEDS REAL INPUT/OWNER NOT EXPOSED)


## 3) Endpoint Coverage — POST /gps/restart

### POST /gps/restart
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8002/api/v1/gps/restart -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```
{"detail":"confirm_required"}
HTTP_STATUS:400
```

**Result:** FAIL


**Aggregator proxy check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/gps/restart -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```
{"detail":"confirm_required"}
HTTP_STATUS:400
```

**Result:** FAIL


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — POST /esp32/buzzer

### POST /esp32/buzzer
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -X POST http://127.0.0.1:8001/api/v1/esp32/buzzer -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```

**Output:**

```
SKIPPED (NEEDS REAL INPUT / OPERATOR APPROVAL)
```

**Result:** SKIP


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** SKIP (NEEDS REAL INPUT/OWNER NOT EXPOSED)


## 3) Endpoint Coverage — POST /esp32/leds

### POST /esp32/leds
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -X POST http://127.0.0.1:8001/api/v1/esp32/leds -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```

**Output:**

```
SKIPPED (NEEDS REAL INPUT / OPERATOR APPROVAL)
```

**Result:** SKIP


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** SKIP (NEEDS REAL INPUT/OWNER NOT EXPOSED)


## 3) Endpoint Coverage — POST /esp32/buttons/simulate

### POST /esp32/buttons/simulate
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -X POST http://127.0.0.1:8001/api/v1/esp32/buttons/simulate -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```

**Output:**

```
SKIPPED (NEEDS REAL INPUT / OPERATOR APPROVAL)
```

**Result:** SKIP


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** SKIP (NEEDS REAL INPUT/OWNER NOT EXPOSED)


## 3) Endpoint Coverage — POST /antsdr/sweep/start

### POST /antsdr/sweep/start
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8890/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8890/api/v1/antsdr/sweep/start -H 'Content-Type: application/json' -d '{"payload": {"plan": "default"}, "confirm": false}'
```

**Output:**

```
404: Not Found
HTTP_STATUS:404
```

**Result:** FAIL


**Aggregator proxy check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/antsdr/sweep/start -H 'Content-Type: application/json' -d '{"payload": {"plan": "default"}, "confirm": false}'
```

**Output:**

```
{"command":"sweep/start","command_id":"antsdr-1772220194647","accepted":true,"timestamp_ms":1772220194647}
HTTP_STATUS:200
```

**Result:** PASS


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — POST /antsdr/sweep/stop

### POST /antsdr/sweep/stop
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8890/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8890/api/v1/antsdr/sweep/stop -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```
404: Not Found
HTTP_STATUS:404
```

**Result:** FAIL


**Aggregator proxy check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/antsdr/sweep/stop -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```
{"detail":"scan_not_running"}
HTTP_STATUS:409
```

**Result:** FAIL


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — POST /antsdr/gain/set

### POST /antsdr/gain/set
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8890/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8890/api/v1/antsdr/gain/set -H 'Content-Type: application/json' -d '{"payload": {"mode": "auto"}, "confirm": false}'
```

**Output:**

```
404: Not Found
HTTP_STATUS:404
```

**Result:** FAIL


**Aggregator proxy check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/antsdr/gain/set -H 'Content-Type: application/json' -d '{"payload": {"mode": "auto"}, "confirm": false}'
```

**Output:**

```
{"command":"gain/set","command_id":"antsdr-1772220194695","accepted":true,"timestamp_ms":1772220194695}
HTTP_STATUS:200
```

**Result:** PASS


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — POST /antsdr/device/reset

### POST /antsdr/device/reset
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8890/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8890/api/v1/antsdr/device/reset -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```
404: Not Found
HTTP_STATUS:404
```

**Result:** FAIL


**Aggregator proxy check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/antsdr/device/reset -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```
{"detail":"confirm_required"}
HTTP_STATUS:400
```

**Result:** PASS


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — POST /remote_id/monitor/start

### POST /remote_id/monitor/start
**Owner tag:** Aggregator
**Owner base:** N/A (owner not exposed)

**Direct-owner check:**

SKIPPED (DIRECT OWNER NOT EXPOSED IN PORT LIST)


**Aggregator proxy check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/remote_id/monitor/start -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```
Internal Server Error
HTTP_STATUS:500
```

**Result:** FAIL


**Classification:** FAIL (AGGREGATOR PROXY GAP)


## 3) Endpoint Coverage — POST /remote_id/monitor/stop

### POST /remote_id/monitor/stop
**Owner tag:** Aggregator
**Owner base:** N/A (owner not exposed)

**Direct-owner check:**

SKIPPED (DIRECT OWNER NOT EXPOSED IN PORT LIST)


**Aggregator proxy check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/remote_id/monitor/stop -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```
Internal Server Error
HTTP_STATUS:500
```

**Result:** FAIL


**Classification:** FAIL (AGGREGATOR PROXY GAP)


## 3) Endpoint Coverage — POST /vrx/tune

### POST /vrx/tune
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/vrx/tune -H 'Content-Type: application/json' -d '{"payload": {"vrx_id": 1, "freq_hz": 5740000000}, "confirm": false}'
```

**Output:**

```
{"detail":"serial not connected"}
HTTP_STATUS:409
```

**Result:** FAIL


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — POST /scan/start

### POST /scan/start
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/scan/start -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```
{"detail":"serial not connected"}
HTTP_STATUS:409
```

**Result:** FAIL


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — POST /scan/stop

### POST /scan/stop
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/scan/stop -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```
{"detail":"serial not connected"}
HTTP_STATUS:409
```

**Result:** FAIL


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — POST /video/select

### POST /video/select
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/video/select -H 'Content-Type: application/json' -d '{"payload": {"sel": 1}, "confirm": false}'
```

**Output:**

```
{"detail":"serial not connected"}
HTTP_STATUS:409
```

**Result:** FAIL


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — POST /system/reboot

### POST /system/reboot
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8002/api/v1/system/reboot -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```
{"detail":"confirm_required"}
HTTP_STATUS:400
```

**Result:** PASS


**Aggregator proxy check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/system/reboot -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```
{"detail":"confirm_required"}
HTTP_STATUS:400
```

**Result:** PASS


**Classification:** PASS


## 3) Endpoint Coverage — POST /system/shutdown

### POST /system/shutdown
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8002/api/v1/system/shutdown -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```
{"detail":"confirm_required"}
HTTP_STATUS:400
```

**Result:** PASS


**Aggregator proxy check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/system/shutdown -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```
{"detail":"confirm_required"}
HTTP_STATUS:400
```

**Result:** PASS


**Classification:** PASS


## 3) Endpoint Coverage — GET /ws

### GET /ws
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/ws
```

**Output:**

```
{"detail":"Method Not Allowed"}
HTTP_STATUS:405
```

**Result:** FAIL


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — GET /system-controller/health

### GET /system-controller/health
**Owner tag:** System Controller
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8002/api/v1/system-controller/health
```

**Output:**

```
{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — GET /system-controller/status

### GET /system-controller/status
**Owner tag:** System Controller
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8002/api/v1/system-controller/status
```

**Output:**

```
{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — GET /system-controller/system

### GET /system-controller/system
**Owner tag:** System Controller
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8002/api/v1/system-controller/system
```

**Output:**

```
{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — GET /system-controller/ups

### GET /system-controller/ups
**Owner tag:** System Controller
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8002/api/v1/system-controller/ups
```

**Output:**

```
{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — GET /system-controller/services

### GET /system-controller/services
**Owner tag:** System Controller
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8002/api/v1/system-controller/services
```

**Output:**

```
{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — POST /system-controller/services/{name}/restart

### POST /system-controller/services/{name}/restart
**Owner tag:** System Controller
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8002/api/v1/system-controller/services/dummy/restart -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```
{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — GET /system-controller/network

### GET /system-controller/network
**Owner tag:** System Controller
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8002/api/v1/system-controller/network
```

**Output:**

```
{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — GET /system-controller/network/wifi/state

### GET /system-controller/network/wifi/state
**Owner tag:** System Controller
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8002/api/v1/system-controller/network/wifi/state
```

**Output:**

```
{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — GET /system-controller/network/wifi/scan

### GET /system-controller/network/wifi/scan
**Owner tag:** System Controller
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8002/api/v1/system-controller/network/wifi/scan
```

**Output:**

```
{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — GET /system-controller/network/bluetooth/state

### GET /system-controller/network/bluetooth/state
**Owner tag:** System Controller
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8002/api/v1/system-controller/network/bluetooth/state
```

**Output:**

```
{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — GET /system-controller/network/bluetooth/devices

### GET /system-controller/network/bluetooth/devices
**Owner tag:** System Controller
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8002/api/v1/system-controller/network/bluetooth/devices
```

**Output:**

```
{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — POST /system-controller/network/wifi/enable

### POST /system-controller/network/wifi/enable
**Owner tag:** System Controller
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8002/api/v1/system-controller/network/wifi/enable -H 'Content-Type: application/json' -d '{"payload": {"enabled": true}, "confirm": false}'
```

**Output:**

```
{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — POST /system-controller/network/wifi/disable

### POST /system-controller/network/wifi/disable
**Owner tag:** System Controller
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8002/api/v1/system-controller/network/wifi/disable -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```
{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — POST /system-controller/network/wifi/connect

### POST /system-controller/network/wifi/connect
**Owner tag:** System Controller
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8002/api/v1/system-controller/network/wifi/connect -H 'Content-Type: application/json' -d '{"payload": {"ssid": "TEST_SSID", "password": "TEST_PASS", "hidden": false}, "confirm": false}'
```

**Output:**

```
{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — POST /system-controller/network/wifi/disconnect

### POST /system-controller/network/wifi/disconnect
**Owner tag:** System Controller
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8002/api/v1/system-controller/network/wifi/disconnect -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```
{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — POST /system-controller/network/bluetooth/enable

### POST /system-controller/network/bluetooth/enable
**Owner tag:** System Controller
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8002/api/v1/system-controller/network/bluetooth/enable -H 'Content-Type: application/json' -d '{"payload": {"enabled": true}, "confirm": false}'
```

**Output:**

```
{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — POST /system-controller/network/bluetooth/disable

### POST /system-controller/network/bluetooth/disable
**Owner tag:** System Controller
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8002/api/v1/system-controller/network/bluetooth/disable -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```
{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — POST /system-controller/network/bluetooth/scan/start

### POST /system-controller/network/bluetooth/scan/start
**Owner tag:** System Controller
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8002/api/v1/system-controller/network/bluetooth/scan/start -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```
{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — POST /system-controller/network/bluetooth/scan/stop

### POST /system-controller/network/bluetooth/scan/stop
**Owner tag:** System Controller
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8002/api/v1/system-controller/network/bluetooth/scan/stop -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```
{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — POST /system-controller/network/bluetooth/pair

### POST /system-controller/network/bluetooth/pair
**Owner tag:** System Controller
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8002/api/v1/system-controller/network/bluetooth/pair -H 'Content-Type: application/json' -d '{"payload": {"addr": "00:11:22:33:44:55"}, "confirm": false}'
```

**Output:**

```
{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — POST /system-controller/network/bluetooth/unpair

### POST /system-controller/network/bluetooth/unpair
**Owner tag:** System Controller
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8002/api/v1/system-controller/network/bluetooth/unpair -H 'Content-Type: application/json' -d '{"payload": {"addr": "00:11:22:33:44:55"}, "confirm": false}'
```

**Output:**

```
{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — GET /system-controller/gps

### GET /system-controller/gps
**Owner tag:** System Controller
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8002/api/v1/system-controller/gps
```

**Output:**

```
{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — POST /system-controller/gps/restart

### POST /system-controller/gps/restart
**Owner tag:** System Controller
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8002/api/v1/system-controller/gps/restart -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```
{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — GET /system-controller/audio

### GET /system-controller/audio
**Owner tag:** System Controller
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8002/api/v1/system-controller/audio
```

**Output:**

```
{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — POST /system-controller/audio/mute

### POST /system-controller/audio/mute
**Owner tag:** System Controller
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8002/api/v1/system-controller/audio/mute -H 'Content-Type: application/json' -d '{"payload": {"muted": true}, "confirm": false}'
```

**Output:**

```
{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — POST /system-controller/audio/volume

### POST /system-controller/audio/volume
**Owner tag:** System Controller
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8002/api/v1/system-controller/audio/volume -H 'Content-Type: application/json' -d '{"payload": {"volume_percent": 50}, "confirm": false}'
```

**Output:**

```
{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — POST /system-controller/system/reboot

### POST /system-controller/system/reboot
**Owner tag:** System Controller
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8002/api/v1/system-controller/system/reboot -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```
{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — POST /system-controller/system/shutdown

### POST /system-controller/system/shutdown
**Owner tag:** System Controller
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8002/api/v1/system-controller/system/shutdown -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```
{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — GET /system-controller/ws

### GET /system-controller/ws
**Owner tag:** System Controller
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8002/api/v1/system-controller/ws
```

**Output:**

```
{"detail":"Not Found"}
HTTP_STATUS:404
```

**Result:** FAIL


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — GET /observability/health

### GET /observability/health
**Owner tag:** Observability
**Owner base:** N/A (owner not exposed)

**Direct-owner check:**

SKIPPED (DIRECT OWNER NOT EXPOSED IN PORT LIST)


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** SKIP (NEEDS REAL INPUT/OWNER NOT EXPOSED)


## 3) Endpoint Coverage — GET /observability/health/detail

### GET /observability/health/detail
**Owner tag:** Observability
**Owner base:** N/A (owner not exposed)

**Direct-owner check:**

SKIPPED (DIRECT OWNER NOT EXPOSED IN PORT LIST)


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** SKIP (NEEDS REAL INPUT/OWNER NOT EXPOSED)


## 3) Endpoint Coverage — GET /observability/status

### GET /observability/status
**Owner tag:** Observability
**Owner base:** N/A (owner not exposed)

**Direct-owner check:**

SKIPPED (DIRECT OWNER NOT EXPOSED IN PORT LIST)


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** SKIP (NEEDS REAL INPUT/OWNER NOT EXPOSED)


## 3) Endpoint Coverage — GET /observability/version

### GET /observability/version
**Owner tag:** Observability
**Owner base:** N/A (owner not exposed)

**Direct-owner check:**

SKIPPED (DIRECT OWNER NOT EXPOSED IN PORT LIST)


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** SKIP (NEEDS REAL INPUT/OWNER NOT EXPOSED)


## 3) Endpoint Coverage — GET /observability/config

### GET /observability/config
**Owner tag:** Observability
**Owner base:** N/A (owner not exposed)

**Direct-owner check:**

SKIPPED (DIRECT OWNER NOT EXPOSED IN PORT LIST)


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** SKIP (NEEDS REAL INPUT/OWNER NOT EXPOSED)


## 3) Endpoint Coverage — POST /observability/diag/bundle

### POST /observability/diag/bundle
**Owner tag:** Observability
**Owner base:** N/A (owner not exposed)

**Direct-owner check:**

SKIPPED (DIRECT OWNER NOT EXPOSED IN PORT LIST)


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** SKIP (NEEDS REAL INPUT/OWNER NOT EXPOSED)


## 3) Endpoint Coverage — GET /antsdr-scan/health

### GET /antsdr-scan/health
**Owner tag:** AntSDR Scan
**Owner base:** http://127.0.0.1:8890/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8890/api/v1/antsdr-scan/health
```

**Output:**

```
404: Not Found
HTTP_STATUS:404
```

**Result:** FAIL


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — GET /antsdr-scan/version

### GET /antsdr-scan/version
**Owner tag:** AntSDR Scan
**Owner base:** http://127.0.0.1:8890/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8890/api/v1/antsdr-scan/version
```

**Output:**

```
404: Not Found
HTTP_STATUS:404
```

**Result:** FAIL


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — GET /antsdr-scan/stats

### GET /antsdr-scan/stats
**Owner tag:** AntSDR Scan
**Owner base:** http://127.0.0.1:8890/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8890/api/v1/antsdr-scan/stats
```

**Output:**

```
404: Not Found
HTTP_STATUS:404
```

**Result:** FAIL


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — GET /antsdr-scan/device

### GET /antsdr-scan/device
**Owner tag:** AntSDR Scan
**Owner base:** http://127.0.0.1:8890/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8890/api/v1/antsdr-scan/device
```

**Output:**

```
404: Not Found
HTTP_STATUS:404
```

**Result:** FAIL


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — GET /antsdr-scan/sweep/state

### GET /antsdr-scan/sweep/state
**Owner tag:** AntSDR Scan
**Owner base:** http://127.0.0.1:8890/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8890/api/v1/antsdr-scan/sweep/state
```

**Output:**

```
404: Not Found
HTTP_STATUS:404
```

**Result:** FAIL


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — GET /antsdr-scan/gain

### GET /antsdr-scan/gain
**Owner tag:** AntSDR Scan
**Owner base:** http://127.0.0.1:8890/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8890/api/v1/antsdr-scan/gain
```

**Output:**

```
404: Not Found
HTTP_STATUS:404
```

**Result:** FAIL


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — GET /antsdr-scan/config

### GET /antsdr-scan/config
**Owner tag:** AntSDR Scan
**Owner base:** http://127.0.0.1:8890/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8890/api/v1/antsdr-scan/config
```

**Output:**

```
404: Not Found
HTTP_STATUS:404
```

**Result:** FAIL


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — POST /antsdr-scan/config/reload

### POST /antsdr-scan/config/reload
**Owner tag:** AntSDR Scan
**Owner base:** http://127.0.0.1:8890/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8890/api/v1/antsdr-scan/config/reload -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```
404: Not Found
HTTP_STATUS:404
```

**Result:** FAIL


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — POST /antsdr-scan/sweep/start

### POST /antsdr-scan/sweep/start
**Owner tag:** AntSDR Scan
**Owner base:** http://127.0.0.1:8890/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8890/api/v1/antsdr-scan/sweep/start -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```
404: Not Found
HTTP_STATUS:404
```

**Result:** FAIL


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — POST /antsdr-scan/sweep/stop

### POST /antsdr-scan/sweep/stop
**Owner tag:** AntSDR Scan
**Owner base:** http://127.0.0.1:8890/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8890/api/v1/antsdr-scan/sweep/stop -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```
404: Not Found
HTTP_STATUS:404
```

**Result:** FAIL


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — POST /antsdr-scan/gain/set

### POST /antsdr-scan/gain/set
**Owner tag:** AntSDR Scan
**Owner base:** http://127.0.0.1:8890/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8890/api/v1/antsdr-scan/gain/set -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```
404: Not Found
HTTP_STATUS:404
```

**Result:** FAIL


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — POST /antsdr-scan/device/reset

### POST /antsdr-scan/device/reset
**Owner tag:** AntSDR Scan
**Owner base:** http://127.0.0.1:8890/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8890/api/v1/antsdr-scan/device/reset -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```
404: Not Found
HTTP_STATUS:404
```

**Result:** FAIL


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — POST /antsdr-scan/device/calibrate

### POST /antsdr-scan/device/calibrate
**Owner tag:** AntSDR Scan
**Owner base:** http://127.0.0.1:8890/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8890/api/v1/antsdr-scan/device/calibrate -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```
404: Not Found
HTTP_STATUS:404
```

**Result:** FAIL


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — GET /antsdr-scan/events/last

### GET /antsdr-scan/events/last
**Owner tag:** AntSDR Scan
**Owner base:** http://127.0.0.1:8890/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8890/api/v1/antsdr-scan/events/last
```

**Output:**

```
404: Not Found
HTTP_STATUS:404
```

**Result:** FAIL


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** FAIL (UPSTREAM BUG)


## 3) Endpoint Coverage — GET /remoteid-engine/status

### GET /remoteid-engine/status
**Owner tag:** RemoteID Engine
**Owner base:** N/A (owner not exposed)

**Direct-owner check:**

SKIPPED (DIRECT OWNER NOT EXPOSED IN PORT LIST)


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** SKIP (NEEDS REAL INPUT/OWNER NOT EXPOSED)


## 3) Endpoint Coverage — GET /remoteid-engine/health

### GET /remoteid-engine/health
**Owner tag:** RemoteID Engine
**Owner base:** N/A (owner not exposed)

**Direct-owner check:**

SKIPPED (DIRECT OWNER NOT EXPOSED IN PORT LIST)


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** SKIP (NEEDS REAL INPUT/OWNER NOT EXPOSED)


## 3) Endpoint Coverage — GET /remoteid-engine/contacts

### GET /remoteid-engine/contacts
**Owner tag:** RemoteID Engine
**Owner base:** N/A (owner not exposed)

**Direct-owner check:**

SKIPPED (DIRECT OWNER NOT EXPOSED IN PORT LIST)


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** SKIP (NEEDS REAL INPUT/OWNER NOT EXPOSED)


## 3) Endpoint Coverage — GET /remoteid-engine/stats

### GET /remoteid-engine/stats
**Owner tag:** RemoteID Engine
**Owner base:** N/A (owner not exposed)

**Direct-owner check:**

SKIPPED (DIRECT OWNER NOT EXPOSED IN PORT LIST)


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** SKIP (NEEDS REAL INPUT/OWNER NOT EXPOSED)


## 3) Endpoint Coverage — GET /remoteid-engine/replay/state

### GET /remoteid-engine/replay/state
**Owner tag:** RemoteID Engine
**Owner base:** N/A (owner not exposed)

**Direct-owner check:**

SKIPPED (DIRECT OWNER NOT EXPOSED IN PORT LIST)


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** SKIP (NEEDS REAL INPUT/OWNER NOT EXPOSED)


## 3) Endpoint Coverage — POST /remoteid-engine/replay/start

### POST /remoteid-engine/replay/start
**Owner tag:** RemoteID Engine
**Owner base:** N/A (owner not exposed)

**Direct-owner check:**

SKIPPED (DIRECT OWNER NOT EXPOSED IN PORT LIST)


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** SKIP (NEEDS REAL INPUT/OWNER NOT EXPOSED)


## 3) Endpoint Coverage — POST /remoteid-engine/replay/stop

### POST /remoteid-engine/replay/stop
**Owner tag:** RemoteID Engine
**Owner base:** N/A (owner not exposed)

**Direct-owner check:**

SKIPPED (DIRECT OWNER NOT EXPOSED IN PORT LIST)


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** SKIP (NEEDS REAL INPUT/OWNER NOT EXPOSED)


## 3) Endpoint Coverage — POST /remoteid-engine/monitor/start

### POST /remoteid-engine/monitor/start
**Owner tag:** RemoteID Engine
**Owner base:** N/A (owner not exposed)

**Direct-owner check:**

SKIPPED (DIRECT OWNER NOT EXPOSED IN PORT LIST)


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** SKIP (NEEDS REAL INPUT/OWNER NOT EXPOSED)


## 3) Endpoint Coverage — POST /remoteid-engine/monitor/stop

### POST /remoteid-engine/monitor/stop
**Owner tag:** RemoteID Engine
**Owner base:** N/A (owner not exposed)

**Direct-owner check:**

SKIPPED (DIRECT OWNER NOT EXPOSED IN PORT LIST)


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** SKIP (NEEDS REAL INPUT/OWNER NOT EXPOSED)


## 3A) Endpoint Coverage Summary

Total GET endpoints: 56
Total POST endpoints: 56


## 4) Field-Level Contract Verification

### /status

**Command:**

```
curl -sS http://127.0.0.1:8001/api/v1/status | jq '.timestamp_ms, .overall_ok, .system.status, .network.connected, .gps.latitude, .gps.longitude, .remote_id.state, .rf.status'
```

**Output:**

```
1772220195327
false
"ok"
true
null
null
"DEGRADED"
"degraded"
```

**Result:** PASS

### /gps

**Command:**

```
curl -sS http://127.0.0.1:8001/api/v1/gps | jq '.fix, .satellites.in_view, .satellites.in_use, .latitude, .longitude'
```

**Output:**

```
"NO_FIX"
0
0
null
null
```

**Result:** PASS

### /network/wifi/state

**Command:**

```
curl -sS http://127.0.0.1:8001/api/v1/network/wifi/state | jq '.enabled, .connected, .ssid'
```

**Output:**

```
true
true
"Airtel_Toybook"
```

**Result:** PASS

### /network/wifi/scan

**Command:**

```
curl -sS http://127.0.0.1:8001/api/v1/network/wifi/scan | jq '.networks|length'
```

**Output:**

```
1
```

**Result:** PASS

### /network/bluetooth/state

**Command:**

```
curl -sS http://127.0.0.1:8001/api/v1/network/bluetooth/state | jq '.enabled, .scanning, .paired_count'
```

**Output:**

```
false
false
0
```

**Result:** PASS

### /network/bluetooth/devices

**Command:**

```
curl -sS http://127.0.0.1:8001/api/v1/network/bluetooth/devices | jq '.devices|length'
```

**Output:**

```
0
```

**Result:** PASS

### /contacts

**Command:**

```
curl -sS http://127.0.0.1:8001/api/v1/contacts | jq '.contacts[0].id, .contacts[0].type, .contacts[0].source, .contacts[0].last_seen_ts'
```

**Output:**

```
"fpv:1"
"FPV"
"esp32"
1772219282836
```

**Result:** PASS

### /esp32

**Command:**

```
curl -sS http://127.0.0.1:8001/api/v1/esp32 | jq '.connected, .heartbeat.ok, .capabilities'
```

**Output:**

```
false
null
null
```

**Result:** PASS

### /antsdr

**Command:**

```
curl -sS http://127.0.0.1:8001/api/v1/antsdr | jq '.connected, .uri'
```

**Output:**

```
false
"ip:192.168.10.2"
```

**Result:** PASS

### /remote_id/status

**Command:**

```
curl -sS http://127.0.0.1:8001/api/v1/remote_id/status | jq '.state, .mode, .capture_active, .contacts_active, .last_error'
```

**Output:**

```
"DEGRADED"
"live"
true
0
"no_odid_frames"
```

**Result:** PASS

### RFScan /health

**Command:**

```
curl -sS http://127.0.0.1:8890/api/v1/health | jq '.timestamp_ms'
```

**Output:**

```
1772220199027
```

**Result:** PASS

### RFScan /stats

**Command:**

```
curl -sS http://127.0.0.1:8890/api/v1/stats | jq '.timestamp_ms'
```

**Output:**

```
1772220199074
```

**Result:** PASS

### RFScan /config

**Command:**

```
curl -sS http://127.0.0.1:8890/api/v1/config | jq '.timestamp_ms'
```

**Output:**

```
null
```

**Result:** PASS


## 5) Confirm-Gating Proof

**Command:**

```
curl -sS -i -X POST http://127.0.0.1:8001/api/v1/system/reboot -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}' | sed -n '1,25p'
```

**Output:**

```
HTTP/1.1 400 Bad Request
date: Fri, 27 Feb 2026 19:23:18 GMT
server: uvicorn
content-length: 29
content-type: application/json

{"detail":"confirm_required"}
```

**Result:** PASS


## 6) WebSocket Proof

**Command:**

```
cd /home/toybook/ndefender-api-contracts && WS_URL=ws://127.0.0.1:8001/api/v1/ws timeout 5s python3 packages/examples/ws/ws_client_python.py
```

**Output:**

```

```

**Result:** FAIL


## 7) Summary Table

| Metric | Value |
|---|---|
| Total endpoints | 112 |
| PASS | 20 |
| FAIL | 61 |
| SKIP | 31 |

## 8) Failure Analysis + Next Fix Repo

| Endpoint | Direct-owner | Aggregator | Classification | Owning Repo | Suggested Fix |
|---|---|---|---|---|---|
| /power | FAIL | PASS | FAIL (UPSTREAM BUG) | ndefender-backend-aggregator | Add/fix endpoint or proxy; align contract |
| /rf | FAIL | PASS | FAIL (UPSTREAM BUG) | ndefender-backend-aggregator | Add/fix endpoint or proxy; align contract |
| /antsdr | FAIL | PASS | FAIL (UPSTREAM BUG) | ndefender-backend-aggregator | Add/fix endpoint or proxy; align contract |
| /antsdr/sweep/state | FAIL | PASS | FAIL (UPSTREAM BUG) | ndefender-backend-aggregator | Add/fix endpoint or proxy; align contract |
| /antsdr/gain | FAIL | PASS | FAIL (UPSTREAM BUG) | ndefender-backend-aggregator | Add/fix endpoint or proxy; align contract |
| /antsdr/stats | FAIL | PASS | FAIL (UPSTREAM BUG) | ndefender-backend-aggregator | Add/fix endpoint or proxy; align contract |
| /gps/restart | FAIL | FAIL | FAIL (UPSTREAM BUG) | ndefender-backend-aggregator | Add/fix endpoint or proxy; align contract |
| /antsdr/sweep/start | FAIL | PASS | FAIL (UPSTREAM BUG) | ndefender-backend-aggregator | Add/fix endpoint or proxy; align contract |
| /antsdr/sweep/stop | FAIL | FAIL | FAIL (UPSTREAM BUG) | ndefender-backend-aggregator | Add/fix endpoint or proxy; align contract |
| /antsdr/gain/set | FAIL | PASS | FAIL (UPSTREAM BUG) | ndefender-backend-aggregator | Add/fix endpoint or proxy; align contract |
| /antsdr/device/reset | FAIL | PASS | FAIL (UPSTREAM BUG) | ndefender-backend-aggregator | Add/fix endpoint or proxy; align contract |
| /remote_id/monitor/start | SKIP | FAIL | FAIL (AGGREGATOR PROXY GAP) | ndefender-backend-aggregator | Add/fix endpoint or proxy; align contract |
| /remote_id/monitor/stop | SKIP | FAIL | FAIL (AGGREGATOR PROXY GAP) | ndefender-backend-aggregator | Add/fix endpoint or proxy; align contract |
| /vrx/tune | FAIL | FAIL | FAIL (UPSTREAM BUG) | ndefender-backend-aggregator | Add/fix endpoint or proxy; align contract |
| /scan/start | FAIL | FAIL | FAIL (UPSTREAM BUG) | ndefender-backend-aggregator | Add/fix endpoint or proxy; align contract |
| /scan/stop | FAIL | FAIL | FAIL (UPSTREAM BUG) | ndefender-backend-aggregator | Add/fix endpoint or proxy; align contract |
| /video/select | FAIL | FAIL | FAIL (UPSTREAM BUG) | ndefender-backend-aggregator | Add/fix endpoint or proxy; align contract |
| /ws | FAIL | FAIL | FAIL (UPSTREAM BUG) | ndefender-backend-aggregator | Add/fix endpoint or proxy; align contract |
| /system-controller/health | FAIL | SKIP | FAIL (UPSTREAM BUG) | ndefender-system-controller | Add/fix endpoint or proxy; align contract |
| /system-controller/status | FAIL | SKIP | FAIL (UPSTREAM BUG) | ndefender-system-controller | Add/fix endpoint or proxy; align contract |
| /system-controller/system | FAIL | SKIP | FAIL (UPSTREAM BUG) | ndefender-system-controller | Add/fix endpoint or proxy; align contract |
| /system-controller/ups | FAIL | SKIP | FAIL (UPSTREAM BUG) | ndefender-system-controller | Add/fix endpoint or proxy; align contract |
| /system-controller/services | FAIL | SKIP | FAIL (UPSTREAM BUG) | ndefender-system-controller | Add/fix endpoint or proxy; align contract |
| /system-controller/services/{name}/restart | FAIL | SKIP | FAIL (UPSTREAM BUG) | ndefender-system-controller | Add/fix endpoint or proxy; align contract |
| /system-controller/network | FAIL | SKIP | FAIL (UPSTREAM BUG) | ndefender-system-controller | Add/fix endpoint or proxy; align contract |
| /system-controller/network/wifi/state | FAIL | SKIP | FAIL (UPSTREAM BUG) | ndefender-system-controller | Add/fix endpoint or proxy; align contract |
| /system-controller/network/wifi/scan | FAIL | SKIP | FAIL (UPSTREAM BUG) | ndefender-system-controller | Add/fix endpoint or proxy; align contract |
| /system-controller/network/bluetooth/state | FAIL | SKIP | FAIL (UPSTREAM BUG) | ndefender-system-controller | Add/fix endpoint or proxy; align contract |
| /system-controller/network/bluetooth/devices | FAIL | SKIP | FAIL (UPSTREAM BUG) | ndefender-system-controller | Add/fix endpoint or proxy; align contract |
| /system-controller/network/wifi/enable | FAIL | SKIP | FAIL (UPSTREAM BUG) | ndefender-system-controller | Add/fix endpoint or proxy; align contract |
| /system-controller/network/wifi/disable | FAIL | SKIP | FAIL (UPSTREAM BUG) | ndefender-system-controller | Add/fix endpoint or proxy; align contract |
| /system-controller/network/wifi/connect | FAIL | SKIP | FAIL (UPSTREAM BUG) | ndefender-system-controller | Add/fix endpoint or proxy; align contract |
| /system-controller/network/wifi/disconnect | FAIL | SKIP | FAIL (UPSTREAM BUG) | ndefender-system-controller | Add/fix endpoint or proxy; align contract |
| /system-controller/network/bluetooth/enable | FAIL | SKIP | FAIL (UPSTREAM BUG) | ndefender-system-controller | Add/fix endpoint or proxy; align contract |
| /system-controller/network/bluetooth/disable | FAIL | SKIP | FAIL (UPSTREAM BUG) | ndefender-system-controller | Add/fix endpoint or proxy; align contract |
| /system-controller/network/bluetooth/scan/start | FAIL | SKIP | FAIL (UPSTREAM BUG) | ndefender-system-controller | Add/fix endpoint or proxy; align contract |
| /system-controller/network/bluetooth/scan/stop | FAIL | SKIP | FAIL (UPSTREAM BUG) | ndefender-system-controller | Add/fix endpoint or proxy; align contract |
| /system-controller/network/bluetooth/pair | FAIL | SKIP | FAIL (UPSTREAM BUG) | ndefender-system-controller | Add/fix endpoint or proxy; align contract |
| /system-controller/network/bluetooth/unpair | FAIL | SKIP | FAIL (UPSTREAM BUG) | ndefender-system-controller | Add/fix endpoint or proxy; align contract |
| /system-controller/gps | FAIL | SKIP | FAIL (UPSTREAM BUG) | ndefender-system-controller | Add/fix endpoint or proxy; align contract |
| /system-controller/gps/restart | FAIL | SKIP | FAIL (UPSTREAM BUG) | ndefender-system-controller | Add/fix endpoint or proxy; align contract |
| /system-controller/audio | FAIL | SKIP | FAIL (UPSTREAM BUG) | ndefender-system-controller | Add/fix endpoint or proxy; align contract |
| /system-controller/audio/mute | FAIL | SKIP | FAIL (UPSTREAM BUG) | ndefender-system-controller | Add/fix endpoint or proxy; align contract |
| /system-controller/audio/volume | FAIL | SKIP | FAIL (UPSTREAM BUG) | ndefender-system-controller | Add/fix endpoint or proxy; align contract |
| /system-controller/system/reboot | FAIL | SKIP | FAIL (UPSTREAM BUG) | ndefender-system-controller | Add/fix endpoint or proxy; align contract |
| /system-controller/system/shutdown | FAIL | SKIP | FAIL (UPSTREAM BUG) | ndefender-system-controller | Add/fix endpoint or proxy; align contract |
| /system-controller/ws | FAIL | SKIP | FAIL (UPSTREAM BUG) | ndefender-system-controller | Add/fix endpoint or proxy; align contract |
| /antsdr-scan/health | FAIL | SKIP | FAIL (UPSTREAM BUG) | ndefender-antsdr-scan | Add/fix endpoint or proxy; align contract |
| /antsdr-scan/version | FAIL | SKIP | FAIL (UPSTREAM BUG) | ndefender-antsdr-scan | Add/fix endpoint or proxy; align contract |
| /antsdr-scan/stats | FAIL | SKIP | FAIL (UPSTREAM BUG) | ndefender-antsdr-scan | Add/fix endpoint or proxy; align contract |
| /antsdr-scan/device | FAIL | SKIP | FAIL (UPSTREAM BUG) | ndefender-antsdr-scan | Add/fix endpoint or proxy; align contract |
| /antsdr-scan/sweep/state | FAIL | SKIP | FAIL (UPSTREAM BUG) | ndefender-antsdr-scan | Add/fix endpoint or proxy; align contract |
| /antsdr-scan/gain | FAIL | SKIP | FAIL (UPSTREAM BUG) | ndefender-antsdr-scan | Add/fix endpoint or proxy; align contract |
| /antsdr-scan/config | FAIL | SKIP | FAIL (UPSTREAM BUG) | ndefender-antsdr-scan | Add/fix endpoint or proxy; align contract |
| /antsdr-scan/config/reload | FAIL | SKIP | FAIL (UPSTREAM BUG) | ndefender-antsdr-scan | Add/fix endpoint or proxy; align contract |
| /antsdr-scan/sweep/start | FAIL | SKIP | FAIL (UPSTREAM BUG) | ndefender-antsdr-scan | Add/fix endpoint or proxy; align contract |
| /antsdr-scan/sweep/stop | FAIL | SKIP | FAIL (UPSTREAM BUG) | ndefender-antsdr-scan | Add/fix endpoint or proxy; align contract |
| /antsdr-scan/gain/set | FAIL | SKIP | FAIL (UPSTREAM BUG) | ndefender-antsdr-scan | Add/fix endpoint or proxy; align contract |
| /antsdr-scan/device/reset | FAIL | SKIP | FAIL (UPSTREAM BUG) | ndefender-antsdr-scan | Add/fix endpoint or proxy; align contract |
| /antsdr-scan/device/calibrate | FAIL | SKIP | FAIL (UPSTREAM BUG) | ndefender-antsdr-scan | Add/fix endpoint or proxy; align contract |
| /antsdr-scan/events/last | FAIL | SKIP | FAIL (UPSTREAM BUG) | ndefender-antsdr-scan | Add/fix endpoint or proxy; align contract |
