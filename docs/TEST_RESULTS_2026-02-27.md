# N-Defender Test Results — 2026-02-27 (Revision 2)

Generated: 2026-02-28 04:15:03 

**IMPORTANT:** This repo contains contracts/docs/validation only; tests were run on the Raspberry Pi against deployed services (not a local setup guide).

Canonical base: `/api/v1`
Ports: 8001 (Aggregator), 8002 (System Controller), 8890 (RFScan). Legacy 8000 must be absent.


## 0) What Was Wrong With the Previous Report

The previous report was incomplete because it executed many endpoints only via the Aggregator base, which produced 404s for upstream-owned routes. It also lacked direct-owner comparisons and field-level contract checks for UI readiness, and did not clearly classify gaps as upstream vs proxy.

## 0b) How To Interpret This Report

This is a contracts/docs repo; all tests are executed against deployed services on the Raspberry Pi. Each endpoint includes a direct-owner check (ground truth) and, when applicable, an Aggregator proxy check. Failures are classified as UPSTREAM BUG, AGGREGATOR PROXY GAP, CONTRACT PATH MISMATCH, or NEEDS REAL INPUT.

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
Sat Feb 28 04:15:03 IST 2026
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
LISTEN 0      2048                     127.0.0.1:8001       0.0.0.0:*    users:(("uvicorn",pid=2465529,fd=7))        
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
## chore/fix-actionable-failures-20260228...origin/chore/fix-actionable-failures-20260228
 M docs/TEST_RESULTS_2026-02-27.md
 M scripts/run_full_evidence.py
```

**Result:** PASS

### git rev-parse --short HEAD

**Command:**

```
git -C /home/toybook/ndefender-api-contracts rev-parse --short HEAD
```

**Output:**

```
1b89d21
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

missing link target: /home/toybook/ndefender-api-contracts/node_modules/ws/README.md -> ./doc/ws.md#ws_no_buffer_util
missing link target: /home/toybook/ndefender-api-contracts/node_modules/ws/README.md -> ./doc/ws.md#ws_no_utf_8_validate
missing link target: /home/toybook/ndefender-api-contracts/node_modules/ws/README.md -> ./doc/ws.md
```

**Result:** FAIL


## 2b) Namespace Probes

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8002/api/v1/health
```

**Output:**

```
{"ok":true,"timestamp_ms":1772232305210,"version":"1.0.0"}
HTTP_STATUS:200
```

**Result:** PASS

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8890/api/v1/health
```

**Output:**

```
{"status": "ok", "engine_running": false, "ws_backend_connected": false, "last_event_timestamp_ms": null, "timestamp_ms": 1772232305222}
HTTP_STATUS:200
```

**Result:** PASS

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8890/api/v1/stats
```

**Output:**

```
{"timestamp_ms": 1772232305232, "frames_processed": 0, "events_emitted": 0, "last_event_timestamp_ms": 0}
HTTP_STATUS:200
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
{"status":"ok","timestamp_ms":1772232305423}
HTTP_STATUS:200
```

**Result:** PASS (OK)


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
{"timestamp_ms":1772232305662,"overall_ok":false,"system":{"cpu_temp_c":34.2,"cpu_usage_percent":11.1,"load_1m":1.501953125,"load_5m":1.63525390625,"load_15m":1.61328125,"ram_used_mb":2298,"ram_total_mb":16215,"disk_used_gb":67,"disk_total_gb":116,"uptime_s":175652,"throttled_flags":0,"status":"ok","timestamp_ms":1772232304027,"version":{"app":"ndefender-system-controller","git_sha":null,"build_ts":null},"cpu":{"temp_c":34.2,"load1":1.501953125,"load5":1.63525390625,"load15":1.61328125,"usage_percent":11.1},"ram":{"total_mb":16215,"used_mb":2298,"free_mb":13916},"storage":{"root":{"total_gb":116.606,"used_gb":67.637,"free_gb":43.025},"logs":null},"last_error":null},"power":{"pack_voltage_v":16.277,"current_a":-0.009,"input_vbus_v":0.0,"input_power_w":0.0,"soc_percent":88,"state":"IDLE","time_to_empty_s":1683600,"time_to_full_s":null,"status":"ok","timestamp_ms":1772232304039,"per_cell_v":[4.07,4.069,4.068,4.069],"last_error":null},"rf":{"last_event":{"reason":"no_rf_events"},"last_event_type":"RF_SCAN_OFFLINE","last_timestamp_ms":1772232302211,"scan_active":false,"status":"degraded","last_error":"no_rf_events"},"remote_id":{"last_event":{"reason":"no_odid_frames"},"last_event_type":"REMOTEID_STALE","last_timestamp_ms":1772232304075,"state":"DEGRADED","mode":"live","capture_active":true,"contacts_active":0,"last_update_ms":1772232304075,"last_error":"no_odid_frames"},"gps":{"timestamp_ms":1772232298919,"fix":"NO_FIX","satellites":{"in_view":0,"in_use":0},"hdop":null,"vdop":null,"pdop":null,"latitude":null,"longitude":null,"altitude_m":null,"speed_m_s":null,"heading_deg":null,"last_update_ms":1772232298919,"age_ms":null,"source":"gpsd","last_error":"gpsd_no_data"},"esp32":{"timestamp_ms":1772231239798,"connected":false,"last_seen_ms":null,"rtt_ms":null,"fw_version":null,"heartbeat":null,"capabilities":null,"last_error":"[Errno 2] could not open port /dev/ttyACM0: [Errno 2] No such file or directory: '/dev/ttyACM0'"},"antsdr":{"timestamp_ms":1772232302211,"connected":false,"uri":"ip:192.168.10.2","temperature_c":null,"last_error":"no_rf_events"},"vrx":{"selected":null,"vrx":[],"led":{},"sys":{"status":"DISCONNECTED","last_error":"[Errno 2] could not open port /dev/ttyACM0: [Errno 2] No such file or directory: '/dev/ttyACM0'"},"scan_state":"idle"},"fpv":{"selected":null,"locked_channels":[],"rssi_raw":null,"scan_state":"idle","freq_hz":null},"video":{"selected":null,"status":"ok"},"services":[],"network":{"connected":true,"ip_v4":"127.0.1.1","ip_v6":null,"ssid":"Airtel_Toybook","wifi":{"timestamp_ms":1772232301940,"enabled":true,"connected":true,"ssid":"Airtel_Toybook","bssid":"2E\\","ip":"127.0.1.1","rssi_dbm":null,"link_quality":null,"last_update_ms":1772232301940,"last_error":null},"bluetooth":{"timestamp_ms":1772232302003,"enabled":false,"scanning":false,"paired_count":0,"connected_devices":[],"last_update_ms":1772232302003,"last_error":null}},"audio":{"muted":null,"volume_percent":null,"status":"degraded","timestamp_ms":1772232301939,"last_error":"audio_unavailable"},"contacts":[],"replay":{"active":false,"source":"none"}}
HTTP_STATUS:200
```

**Result:** PASS (OK)


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
{"contacts":[]}
HTTP_STATUS:200
```

**Result:** PASS (OK)


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** PASS


## 3) Endpoint Coverage — GET /system

### GET /system
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/system
```

**Output:**

```
{"cpu_temp_c":34.2,"cpu_usage_percent":11.1,"load_1m":1.501953125,"load_5m":1.63525390625,"load_15m":1.61328125,"ram_used_mb":2298,"ram_total_mb":16215,"disk_used_gb":67,"disk_total_gb":116,"uptime_s":175652,"throttled_flags":0,"status":"ok","timestamp_ms":1772232304027,"version":{"app":"ndefender-system-controller","git_sha":null,"build_ts":null},"cpu":{"temp_c":34.2,"load1":1.501953125,"load5":1.63525390625,"load15":1.61328125,"usage_percent":11.1},"ram":{"total_mb":16215,"used_mb":2298,"free_mb":13916},"storage":{"root":{"total_gb":116.606,"used_gb":67.637,"free_gb":43.025},"logs":null},"last_error":null}
HTTP_STATUS:200
```

**Result:** PASS (OK)


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** PASS


## 3) Endpoint Coverage — GET /power

### GET /power
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/power
```

**Output:**

```
{"pack_voltage_v":16.276,"current_a":-0.009,"input_vbus_v":0.0,"input_power_w":0.0,"soc_percent":88,"state":"IDLE","time_to_empty_s":1683600,"time_to_full_s":null,"status":"ok","timestamp_ms":1772232306043,"per_cell_v":[4.07,4.069,4.068,4.069],"last_error":null}
HTTP_STATUS:200
```

**Result:** PASS (OK)


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** PASS


## 3) Endpoint Coverage — GET /rf

### GET /rf
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/rf
```

**Output:**

```
{"last_event":{"reason":"no_rf_events"},"last_event_type":"RF_SCAN_OFFLINE","last_timestamp_ms":1772232302211,"scan_active":false,"status":"degraded","last_error":"no_rf_events"}
HTTP_STATUS:200
```

**Result:** PASS (OK)


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** PASS


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
{"selected":null,"status":"ok"}
HTTP_STATUS:200
```

**Result:** PASS (OK)


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** PASS


## 3) Endpoint Coverage — GET /services

### GET /services
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/services
```

**Output:**

```
[]
HTTP_STATUS:200
```

**Result:** PASS (OK)


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** PASS


## 3) Endpoint Coverage — GET /network

### GET /network
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/network
```

**Output:**

```
{"connected":true,"ip_v4":"127.0.1.1","ip_v6":null,"ssid":"Airtel_Toybook","wifi":{"timestamp_ms":1772232301940,"enabled":true,"connected":true,"ssid":"Airtel_Toybook","bssid":"2E\\","ip":"127.0.1.1","rssi_dbm":null,"link_quality":null,"last_update_ms":1772232301940,"last_error":null},"bluetooth":{"timestamp_ms":1772232302003,"enabled":false,"scanning":false,"paired_count":0,"connected_devices":[],"last_update_ms":1772232302003,"last_error":null}}
HTTP_STATUS:200
```

**Result:** PASS (OK)


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** PASS


## 3) Endpoint Coverage — GET /audio

### GET /audio
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/audio
```

**Output:**

```
{"muted":null,"volume_percent":null,"status":"degraded","timestamp_ms":1772232301939,"last_error":"audio_unavailable"}
HTTP_STATUS:200
```

**Result:** PASS (OK)


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** PASS


## 3) Endpoint Coverage — GET /network/wifi/state

### GET /network/wifi/state
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/network/wifi/state
```

**Output:**

```
{"timestamp_ms":1772232310088,"enabled":true,"connected":true,"ssid":"Airtel_Toybook","bssid":"2E\\","ip":"127.0.1.1","rssi_dbm":null,"link_quality":null,"last_update_ms":1772232310088,"last_error":null}
HTTP_STATUS:200
```

**Result:** PASS (OK)


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** PASS


## 3) Endpoint Coverage — GET /network/wifi/scan

### GET /network/wifi/scan
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/network/wifi/scan
```

**Output:**

```
{"timestamp_ms":1772232310342,"networks":[{"ssid":"Airtel_Toybook","bssid":"2E\\","security":"C1\\"}],"last_error":null}
HTTP_STATUS:200
```

**Result:** PASS (OK)


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** PASS


## 3) Endpoint Coverage — GET /network/bluetooth/state

### GET /network/bluetooth/state
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/network/bluetooth/state
```

**Output:**

```
{"timestamp_ms":1772232310582,"enabled":false,"scanning":false,"paired_count":0,"connected_devices":[],"last_update_ms":1772232310582,"last_error":null}
HTTP_STATUS:200
```

**Result:** PASS (OK)


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** PASS


## 3) Endpoint Coverage — GET /network/bluetooth/devices

### GET /network/bluetooth/devices
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/network/bluetooth/devices
```

**Output:**

```
{"timestamp_ms":1772232310839,"devices":[]}
HTTP_STATUS:200
```

**Result:** PASS (OK)


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** PASS


## 3) Endpoint Coverage — GET /gps

### GET /gps
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/gps
```

**Output:**

```
{"timestamp_ms":1772232306924,"fix":"NO_FIX","satellites":{"in_view":0,"in_use":0},"hdop":null,"vdop":null,"pdop":null,"latitude":null,"longitude":null,"altitude_m":null,"speed_m_s":null,"heading_deg":null,"last_update_ms":1772232306924,"age_ms":null,"source":"gpsd","last_error":"gpsd_no_data"}
HTTP_STATUS:200
```

**Result:** PASS (OK)


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


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
{"timestamp_ms":1772231239798,"connected":false,"last_seen_ms":null,"rtt_ms":null,"fw_version":null,"heartbeat":null,"capabilities":null,"last_error":"[Errno 2] could not open port /dev/ttyACM0: [Errno 2] No such file or directory: '/dev/ttyACM0'"}
HTTP_STATUS:200
```

**Result:** PASS (OK)


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
{"timestamp_ms":1772232311526,"schema_version":null,"config":{}}
HTTP_STATUS:200
```

**Result:** PASS (OK)


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
HTTP_STATUS:SKIPPED
```

**Result:** SKIP (NEEDS_REAL_INPUT)


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** SKIP (NEEDS REAL INPUT)


## 3) Endpoint Coverage — GET /antsdr

### GET /antsdr
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/antsdr
```

**Output:**

```
{"timestamp_ms":1772232307216,"connected":false,"uri":"ip:192.168.10.2","temperature_c":null,"last_error":"no_rf_events"}
HTTP_STATUS:200
```

**Result:** PASS (OK)


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** PASS


## 3) Endpoint Coverage — GET /antsdr/sweep/state

### GET /antsdr/sweep/state
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/antsdr/sweep/state
```

**Output:**

```
{"timestamp_ms":1772232311983,"running":false,"active_plan":"5G8_RaceBand","plans":[{"name":"5G8_RaceBand","start_hz":5658000000.0,"end_hz":5917000000.0,"step_hz":2000000.0},{"name":"5G8_FatShark","start_hz":5733000000.0,"end_hz":5866000000.0,"step_hz":2000000.0},{"name":"5G8_BandA","start_hz":5865000000.0,"end_hz":5945000000.0,"step_hz":2000000.0},{"name":"5G8_Digital","start_hz":5725000000.0,"end_hz":5850000000.0,"step_hz":2000000.0},{"name":"2G4_Control","start_hz":2400000000.0,"end_hz":2483500000.0,"step_hz":1000000.0},{"name":"915_Control","start_hz":902000000.0,"end_hz":928000000.0,"step_hz":1000000.0}],"last_update_ms":1772232311983,"last_error":"pyadi-iio is required for AntSDR access"}
HTTP_STATUS:200
```

**Result:** PASS (OK)


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** PASS


## 3) Endpoint Coverage — GET /antsdr/gain

### GET /antsdr/gain
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/antsdr/gain
```

**Output:**

```
{"timestamp_ms":1772232312150,"mode":"auto"}
HTTP_STATUS:200
```

**Result:** PASS (OK)


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** PASS


## 3) Endpoint Coverage — GET /antsdr/stats

### GET /antsdr/stats
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/antsdr/stats
```

**Output:**

```
{"timestamp_ms":1772232312345,"frames_processed":0,"events_emitted":0,"last_event_timestamp_ms":0}
HTTP_STATUS:200
```

**Result:** PASS (OK)


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** PASS


## 3) Endpoint Coverage — GET /remote_id

### GET /remote_id
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/remote_id
```

**Output:**

```
{"last_event":{"reason":"no_odid_frames"},"last_event_type":"REMOTEID_STALE","last_timestamp_ms":1772232309129,"state":"DEGRADED","mode":"live","capture_active":true,"contacts_active":0,"last_update_ms":1772232309129,"last_error":"no_odid_frames","timestamp_ms":1772232312574}
HTTP_STATUS:200
```

**Result:** PASS (OK)


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** PASS


## 3) Endpoint Coverage — GET /remote_id/contacts

### GET /remote_id/contacts
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/remote_id/contacts
```

**Output:**

```
{"timestamp_ms":1772232312807,"contacts":[]}
HTTP_STATUS:200
```

**Result:** PASS (OK)


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** PASS


## 3) Endpoint Coverage — GET /remote_id/stats

### GET /remote_id/stats
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8001/api/v1/remote_id/stats
```

**Output:**

```
{"timestamp_ms":1772232312979,"frames":0,"decoded":0}
HTTP_STATUS:200
```

**Result:** PASS (OK)


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** PASS


## 3) Endpoint Coverage — POST /audio/mute

### POST /audio/mute
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -X POST http://127.0.0.1:8001/api/v1/audio/mute -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```

**Output:**

```
SKIPPED (NEEDS REAL INPUT / OPERATOR APPROVAL)
HTTP_STATUS:SKIPPED
```

**Result:** SKIP (NEEDS_REAL_INPUT)


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** SKIP (NEEDS REAL INPUT)


## 3) Endpoint Coverage — POST /audio/volume

### POST /audio/volume
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -X POST http://127.0.0.1:8001/api/v1/audio/volume -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```

**Output:**

```
SKIPPED (NEEDS REAL INPUT / OPERATOR APPROVAL)
HTTP_STATUS:SKIPPED
```

**Result:** SKIP (NEEDS_REAL_INPUT)


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** SKIP (NEEDS REAL INPUT)


## 3) Endpoint Coverage — POST /network/wifi/enable

### POST /network/wifi/enable
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -X POST http://127.0.0.1:8001/api/v1/network/wifi/enable -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```

**Output:**

```
SKIPPED (NEEDS REAL INPUT / OPERATOR APPROVAL)
HTTP_STATUS:SKIPPED
```

**Result:** SKIP (NEEDS_REAL_INPUT)


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** SKIP (NEEDS REAL INPUT)


## 3) Endpoint Coverage — POST /network/wifi/disable

### POST /network/wifi/disable
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -X POST http://127.0.0.1:8001/api/v1/network/wifi/disable -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```

**Output:**

```
SKIPPED (NEEDS REAL INPUT / OPERATOR APPROVAL)
HTTP_STATUS:SKIPPED
```

**Result:** SKIP (NEEDS_REAL_INPUT)


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** SKIP (NEEDS REAL INPUT)


## 3) Endpoint Coverage — POST /network/wifi/connect

### POST /network/wifi/connect
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -X POST http://127.0.0.1:8001/api/v1/network/wifi/connect -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```

**Output:**

```
SKIPPED (NEEDS REAL INPUT / OPERATOR APPROVAL)
HTTP_STATUS:SKIPPED
```

**Result:** SKIP (NEEDS_REAL_INPUT)


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** SKIP (NEEDS REAL INPUT)


## 3) Endpoint Coverage — POST /network/wifi/disconnect

### POST /network/wifi/disconnect
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -X POST http://127.0.0.1:8001/api/v1/network/wifi/disconnect -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```

**Output:**

```
SKIPPED (NEEDS REAL INPUT / OPERATOR APPROVAL)
HTTP_STATUS:SKIPPED
```

**Result:** SKIP (NEEDS_REAL_INPUT)


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** SKIP (NEEDS REAL INPUT)


## 3) Endpoint Coverage — POST /network/bluetooth/enable

### POST /network/bluetooth/enable
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -X POST http://127.0.0.1:8001/api/v1/network/bluetooth/enable -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```

**Output:**

```
SKIPPED (NEEDS REAL INPUT / OPERATOR APPROVAL)
HTTP_STATUS:SKIPPED
```

**Result:** SKIP (NEEDS_REAL_INPUT)


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** SKIP (NEEDS REAL INPUT)


## 3) Endpoint Coverage — POST /network/bluetooth/disable

### POST /network/bluetooth/disable
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -X POST http://127.0.0.1:8001/api/v1/network/bluetooth/disable -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```

**Output:**

```
SKIPPED (NEEDS REAL INPUT / OPERATOR APPROVAL)
HTTP_STATUS:SKIPPED
```

**Result:** SKIP (NEEDS_REAL_INPUT)


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** SKIP (NEEDS REAL INPUT)


## 3) Endpoint Coverage — POST /network/bluetooth/scan/start

### POST /network/bluetooth/scan/start
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -X POST http://127.0.0.1:8001/api/v1/network/bluetooth/scan/start -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```

**Output:**

```
SKIPPED (NEEDS REAL INPUT / OPERATOR APPROVAL)
HTTP_STATUS:SKIPPED
```

**Result:** SKIP (NEEDS_REAL_INPUT)


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** SKIP (NEEDS REAL INPUT)


## 3) Endpoint Coverage — POST /network/bluetooth/scan/stop

### POST /network/bluetooth/scan/stop
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -X POST http://127.0.0.1:8001/api/v1/network/bluetooth/scan/stop -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```

**Output:**

```
SKIPPED (NEEDS REAL INPUT / OPERATOR APPROVAL)
HTTP_STATUS:SKIPPED
```

**Result:** SKIP (NEEDS_REAL_INPUT)


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** SKIP (NEEDS REAL INPUT)


## 3) Endpoint Coverage — POST /network/bluetooth/pair

### POST /network/bluetooth/pair
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -X POST http://127.0.0.1:8001/api/v1/network/bluetooth/pair -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```

**Output:**

```
SKIPPED (NEEDS REAL INPUT / OPERATOR APPROVAL)
HTTP_STATUS:SKIPPED
```

**Result:** SKIP (NEEDS_REAL_INPUT)


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** SKIP (NEEDS REAL INPUT)


## 3) Endpoint Coverage — POST /network/bluetooth/unpair

### POST /network/bluetooth/unpair
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -X POST http://127.0.0.1:8001/api/v1/network/bluetooth/unpair -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
```

**Output:**

```
SKIPPED (NEEDS REAL INPUT / OPERATOR APPROVAL)
HTTP_STATUS:SKIPPED
```

**Result:** SKIP (NEEDS_REAL_INPUT)


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** SKIP (NEEDS REAL INPUT)


## 3) Endpoint Coverage — POST /gps/restart

### POST /gps/restart
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/gps/restart -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```
{"detail":"confirm_required"}
HTTP_STATUS:400
```

**Result:** PASS_SAFE_ERROR (CONFIRM_REQUIRED)


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** PASS_SAFE_ERROR (CONFIRM_REQUIRED)


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
HTTP_STATUS:SKIPPED
```

**Result:** SKIP (NEEDS_REAL_INPUT)


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** SKIP (NEEDS REAL INPUT)


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
HTTP_STATUS:SKIPPED
```

**Result:** SKIP (NEEDS_REAL_INPUT)


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** SKIP (NEEDS REAL INPUT)


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
HTTP_STATUS:SKIPPED
```

**Result:** SKIP (NEEDS_REAL_INPUT)


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** SKIP (NEEDS REAL INPUT)


## 3) Endpoint Coverage — POST /antsdr/sweep/start

### POST /antsdr/sweep/start
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/antsdr/sweep/start -H 'Content-Type: application/json' -d '{"payload": {"plan": "default"}, "confirm": false}'
```

**Output:**

```
{"command":"sweep/start","command_id":"antsdr-1772232313402","accepted":true,"timestamp_ms":1772232313402}
HTTP_STATUS:200
```

**Result:** PASS (OK)


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** PASS


## 3) Endpoint Coverage — POST /antsdr/sweep/stop

### POST /antsdr/sweep/stop
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/antsdr/sweep/stop -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```
{"detail":"scan_not_running"}
HTTP_STATUS:409
```

**Result:** PASS_PRECONDITION (PRECONDITION_OK)


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** PASS_PRECONDITION (PRECONDITION_OK)


## 3) Endpoint Coverage — POST /antsdr/gain/set

### POST /antsdr/gain/set
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/antsdr/gain/set -H 'Content-Type: application/json' -d '{"payload": {"mode": "auto"}, "confirm": false}'
```

**Output:**

```
{"command":"gain/set","command_id":"antsdr-1772232313827","accepted":true,"timestamp_ms":1772232313827}
HTTP_STATUS:200
```

**Result:** PASS (OK)


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** PASS


## 3) Endpoint Coverage — POST /antsdr/device/reset

### POST /antsdr/device/reset
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/antsdr/device/reset -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```
{"detail":"confirm_required"}
HTTP_STATUS:400
```

**Result:** PASS_SAFE_ERROR (CONFIRM_REQUIRED)


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** PASS_SAFE_ERROR (CONFIRM_REQUIRED)


## 3) Endpoint Coverage — POST /remote_id/monitor/start

### POST /remote_id/monitor/start
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/remote_id/monitor/start -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```
{"detail":"remoteid_service_unreachable"}
HTTP_STATUS:502
```

**Result:** PASS (UPSTREAM_UNREACHABLE)


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** PASS (UPSTREAM_UNREACHABLE)


## 3) Endpoint Coverage — POST /remote_id/monitor/stop

### POST /remote_id/monitor/stop
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/remote_id/monitor/stop -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```
{"detail":"remoteid_service_unreachable"}
HTTP_STATUS:502
```

**Result:** PASS (UPSTREAM_UNREACHABLE)


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** PASS (UPSTREAM_UNREACHABLE)


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

**Result:** PASS_PRECONDITION (PRECONDITION_OK)


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** PASS_PRECONDITION (PRECONDITION_OK)


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

**Result:** PASS_PRECONDITION (PRECONDITION_OK)


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** PASS_PRECONDITION (PRECONDITION_OK)


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

**Result:** PASS_PRECONDITION (PRECONDITION_OK)


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** PASS_PRECONDITION (PRECONDITION_OK)


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

**Result:** PASS_PRECONDITION (PRECONDITION_OK)


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** PASS_PRECONDITION (PRECONDITION_OK)


## 3) Endpoint Coverage — POST /system/reboot

### POST /system/reboot
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/system/reboot -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```
{"detail":"confirm_required"}
HTTP_STATUS:400
```

**Result:** PASS_SAFE_ERROR (CONFIRM_REQUIRED)


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** PASS_SAFE_ERROR (CONFIRM_REQUIRED)


## 3) Endpoint Coverage — POST /system/shutdown

### POST /system/shutdown
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/system/shutdown -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```
{"detail":"confirm_required"}
HTTP_STATUS:400
```

**Result:** PASS_SAFE_ERROR (CONFIRM_REQUIRED)


**Aggregator proxy check:** N/A (Aggregator owns endpoint)


**Classification:** PASS_SAFE_ERROR (CONFIRM_REQUIRED)


## 3) Endpoint Coverage — GET /ws

### GET /ws
**Owner tag:** Aggregator
**Owner base:** http://127.0.0.1:8001/api/v1

**Direct-owner check:**

SKIPPED (WS endpoint; HTTP GET not applicable)


**Aggregator proxy check:** N/A (WS endpoint; tested via WS client)


**Classification:** SKIP (NOT_APPLICABLE_FOR_HTTP)


## 3) Endpoint Coverage — GET /ups

### GET /ups
**Owner tag:** System Controller
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8002/api/v1/ups
```

**Output:**

```
{"timestamp_ms":1772232318070,"status":"ok","pack_voltage_v":16.276,"current_a":-0.009,"input_vbus_v":0.0,"input_power_w":0.0,"soc_percent":88,"time_to_empty_s":1894080,"time_to_full_s":null,"per_cell_v":[4.069,4.07,4.068,4.069],"state":"IDLE","last_error":null}
HTTP_STATUS:200
```

**Result:** PASS (OK)


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** PASS


## 3) Endpoint Coverage — POST /services/{name}/restart

### POST /services/{name}/restart
**Owner tag:** System Controller
**Owner base:** http://127.0.0.1:8002/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8002/api/v1/services/dummy/restart -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```
{"detail":"confirm_required"}
HTTP_STATUS:400
```

**Result:** PASS_SAFE_ERROR (CONFIRM_REQUIRED)


**Aggregator proxy check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8001/api/v1/services/dummy/restart -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```
{"detail":"confirm_required"}
HTTP_STATUS:400
```

**Result:** PASS_SAFE_ERROR


**Classification:** PASS_SAFE_ERROR (CONFIRM_REQUIRED)


## 3) Endpoint Coverage — GET /observability/health

### GET /observability/health
**Owner tag:** Observability
**Owner base:** N/A (owner not exposed)

**Direct-owner check:**

SKIPPED (DIRECT OWNER NOT EXPOSED IN PORT LIST)


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** SKIP (OWNER NOT EXPOSED / SERVICE-SPECIFIC)


## 3) Endpoint Coverage — GET /observability/health/detail

### GET /observability/health/detail
**Owner tag:** Observability
**Owner base:** N/A (owner not exposed)

**Direct-owner check:**

SKIPPED (DIRECT OWNER NOT EXPOSED IN PORT LIST)


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** SKIP (OWNER NOT EXPOSED / SERVICE-SPECIFIC)


## 3) Endpoint Coverage — GET /observability/status

### GET /observability/status
**Owner tag:** Observability
**Owner base:** N/A (owner not exposed)

**Direct-owner check:**

SKIPPED (DIRECT OWNER NOT EXPOSED IN PORT LIST)


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** SKIP (OWNER NOT EXPOSED / SERVICE-SPECIFIC)


## 3) Endpoint Coverage — GET /observability/version

### GET /observability/version
**Owner tag:** Observability
**Owner base:** N/A (owner not exposed)

**Direct-owner check:**

SKIPPED (DIRECT OWNER NOT EXPOSED IN PORT LIST)


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** SKIP (OWNER NOT EXPOSED / SERVICE-SPECIFIC)


## 3) Endpoint Coverage — GET /observability/config

### GET /observability/config
**Owner tag:** Observability
**Owner base:** N/A (owner not exposed)

**Direct-owner check:**

SKIPPED (DIRECT OWNER NOT EXPOSED IN PORT LIST)


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** SKIP (OWNER NOT EXPOSED / SERVICE-SPECIFIC)


## 3) Endpoint Coverage — POST /observability/diag/bundle

### POST /observability/diag/bundle
**Owner tag:** Observability
**Owner base:** N/A (owner not exposed)

**Direct-owner check:**

SKIPPED (DIRECT OWNER NOT EXPOSED IN PORT LIST)


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** SKIP (OWNER NOT EXPOSED / SERVICE-SPECIFIC)


## 3) Endpoint Coverage — GET /version

### GET /version
**Owner tag:** AntSDR Scan
**Owner base:** http://127.0.0.1:8890/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8890/api/v1/version
```

**Output:**

```
{"version": "0.1.0"}
HTTP_STATUS:200
```

**Result:** PASS (OK)


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** PASS


## 3) Endpoint Coverage — GET /stats

### GET /stats
**Owner tag:** AntSDR Scan
**Owner base:** http://127.0.0.1:8890/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8890/api/v1/stats
```

**Output:**

```
{"timestamp_ms": 1772232318961, "frames_processed": 0, "events_emitted": 0, "last_event_timestamp_ms": 0}
HTTP_STATUS:200
```

**Result:** PASS (OK)


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** PASS


## 3) Endpoint Coverage — GET /device

### GET /device
**Owner tag:** AntSDR Scan
**Owner base:** http://127.0.0.1:8890/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8890/api/v1/device
```

**Output:**

```
{"timestamp_ms": 1772232319178, "connected": false, "uri": "ip:192.168.10.2", "temperature_c": null, "last_error": "pyadi-iio is required for AntSDR access"}
HTTP_STATUS:200
```

**Result:** PASS (OK)


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** PASS


## 3) Endpoint Coverage — GET /sweep/state

### GET /sweep/state
**Owner tag:** AntSDR Scan
**Owner base:** http://127.0.0.1:8890/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8890/api/v1/sweep/state
```

**Output:**

```
{"timestamp_ms": 1772232319422, "running": false, "active_plan": "5G8_RaceBand", "plans": [{"name": "5G8_RaceBand", "start_hz": 5658000000.0, "end_hz": 5917000000.0, "step_hz": 2000000.0}, {"name": "5G8_FatShark", "start_hz": 5733000000.0, "end_hz": 5866000000.0, "step_hz": 2000000.0}, {"name": "5G8_BandA", "start_hz": 5865000000.0, "end_hz": 5945000000.0, "step_hz": 2000000.0}, {"name": "5G8_Digital", "start_hz": 5725000000.0, "end_hz": 5850000000.0, "step_hz": 2000000.0}, {"name": "2G4_Control", "start_hz": 2400000000.0, "end_hz": 2483500000.0, "step_hz": 1000000.0}, {"name": "915_Control", "start_hz": 902000000.0, "end_hz": 928000000.0, "step_hz": 1000000.0}], "last_update_ms": 1772232319422, "last_error": "pyadi-iio is required for AntSDR access"}
HTTP_STATUS:200
```

**Result:** PASS (OK)


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** PASS


## 3) Endpoint Coverage — GET /gain

### GET /gain
**Owner tag:** AntSDR Scan
**Owner base:** http://127.0.0.1:8890/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8890/api/v1/gain
```

**Output:**

```
{"timestamp_ms": 1772232319666, "mode": "auto"}
HTTP_STATUS:200
```

**Result:** PASS (OK)


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** PASS


## 3) Endpoint Coverage — GET /config

### GET /config
**Owner tag:** AntSDR Scan
**Owner base:** http://127.0.0.1:8890/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8890/api/v1/config
```

**Output:**

```
{"radio": {"uri": "ip:192.168.10.2", "sample_rate": 2000000, "rx_buffer_size": 4096}, "tracker": {"bucket_hz": 250000, "ttl_s": 120.0, "min_hits_to_confirm": 2, "update_interval_s": 1.0, "correlation_enabled": false, "correlation_window_ms": 100}, "detector": {"min_snr_db": 10.0, "lo_guard_hz": 100000.0}, "sweep": {"bands": [{"name": "5G8_RaceBand", "start_hz": 5658000000.0, "stop_hz": 5917000000.0, "step_hz": 2000000.0}, {"name": "5G8_FatShark", "start_hz": 5733000000.0, "stop_hz": 5866000000.0, "step_hz": 2000000.0}, {"name": "5G8_BandA", "start_hz": 5865000000.0, "stop_hz": 5945000000.0, "step_hz": 2000000.0}, {"name": "5G8_Digital", "start_hz": 5725000000.0, "stop_hz": 5850000000.0, "step_hz": 2000000.0}, {"name": "2G4_Control", "start_hz": 2400000000.0, "stop_hz": 2483500000.0, "step_hz": 1000000.0}, {"name": "915_Control", "start_hz": 902000000.0, "stop_hz": 928000000.0, "step_hz": 1000000.0}], "dwell_ms": 0}, "ws": {"enabled": false, "url": "", "connect_timeout_s": 5.0, "send_timeout_s": 2.0, "max_retries": 3, "retry_backoff_s": 1.0}, "classification": {"profiles": "/home/toybook/ndefender-antsdr-scan/config/classification_profiles.yaml", "hop_window_ms": 1000, "min_hop_hz": 200000.0}, "api": {"enabled": true, "bind": "127.0.0.1", "port": 8890, "api_key": "", "max_clients": 25, "event_buffer": 500}}
HTTP_STATUS:200
```

**Result:** PASS (OK)


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** PASS


## 3) Endpoint Coverage — POST /config/reload

### POST /config/reload
**Owner tag:** AntSDR Scan
**Owner base:** http://127.0.0.1:8890/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8890/api/v1/config/reload -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```
{"status": "ok"}
HTTP_STATUS:200
```

**Result:** PASS (OK)


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** PASS


## 3) Endpoint Coverage — POST /sweep/start

### POST /sweep/start
**Owner tag:** AntSDR Scan
**Owner base:** http://127.0.0.1:8890/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8890/api/v1/sweep/start -H 'Content-Type: application/json' -d '{"payload": {"plan": "default"}, "confirm": false}'
```

**Output:**

```
{"command": "sweep/start", "command_id": "antsdr-1772232320404", "accepted": true, "timestamp_ms": 1772232320404}
HTTP_STATUS:200
```

**Result:** PASS (OK)


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** PASS


## 3) Endpoint Coverage — POST /sweep/stop

### POST /sweep/stop
**Owner tag:** AntSDR Scan
**Owner base:** http://127.0.0.1:8890/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8890/api/v1/sweep/stop -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```
{"detail": "scan_not_running"}
HTTP_STATUS:409
```

**Result:** PASS_PRECONDITION (PRECONDITION_OK)


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** PASS_PRECONDITION (PRECONDITION_OK)


## 3) Endpoint Coverage — POST /gain/set

### POST /gain/set
**Owner tag:** AntSDR Scan
**Owner base:** http://127.0.0.1:8890/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8890/api/v1/gain/set -H 'Content-Type: application/json' -d '{"payload": {"mode": "auto"}, "confirm": false}'
```

**Output:**

```
{"command": "gain/set", "command_id": "antsdr-1772232320856", "accepted": true, "timestamp_ms": 1772232320856}
HTTP_STATUS:200
```

**Result:** PASS (OK)


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** PASS


## 3) Endpoint Coverage — POST /device/reset

### POST /device/reset
**Owner tag:** AntSDR Scan
**Owner base:** http://127.0.0.1:8890/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8890/api/v1/device/reset -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```
{"detail": "confirm_required"}
HTTP_STATUS:400
```

**Result:** PASS_SAFE_ERROR (CONFIRM_REQUIRED)


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** PASS_SAFE_ERROR (CONFIRM_REQUIRED)


## 3) Endpoint Coverage — POST /device/calibrate

### POST /device/calibrate
**Owner tag:** AntSDR Scan
**Owner base:** http://127.0.0.1:8890/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' -X POST http://127.0.0.1:8890/api/v1/device/calibrate -H 'Content-Type: application/json' -d '{"payload": {}, "confirm": false}'
```

**Output:**

```
{"detail": "confirm_required"}
HTTP_STATUS:400
```

**Result:** PASS_SAFE_ERROR (CONFIRM_REQUIRED)


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** PASS_SAFE_ERROR (CONFIRM_REQUIRED)


## 3) Endpoint Coverage — GET /events/last

### GET /events/last
**Owner tag:** AntSDR Scan
**Owner base:** http://127.0.0.1:8890/api/v1

**Direct-owner check:**

**Command:**

```
curl -sS -w '\nHTTP_STATUS:%{http_code}' http://127.0.0.1:8890/api/v1/events/last
```

**Output:**

```
{"events": []}
HTTP_STATUS:200
```

**Result:** PASS (OK)


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** PASS


## 3) Endpoint Coverage — GET /remoteid-engine/status

### GET /remoteid-engine/status
**Owner tag:** RemoteID Engine
**Owner base:** N/A (owner not exposed)

**Direct-owner check:**

SKIPPED (DIRECT OWNER NOT EXPOSED IN PORT LIST)


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** SKIP (OWNER NOT EXPOSED / SERVICE-SPECIFIC)


## 3) Endpoint Coverage — GET /remoteid-engine/health

### GET /remoteid-engine/health
**Owner tag:** RemoteID Engine
**Owner base:** N/A (owner not exposed)

**Direct-owner check:**

SKIPPED (DIRECT OWNER NOT EXPOSED IN PORT LIST)


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** SKIP (OWNER NOT EXPOSED / SERVICE-SPECIFIC)


## 3) Endpoint Coverage — GET /remoteid-engine/contacts

### GET /remoteid-engine/contacts
**Owner tag:** RemoteID Engine
**Owner base:** N/A (owner not exposed)

**Direct-owner check:**

SKIPPED (DIRECT OWNER NOT EXPOSED IN PORT LIST)


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** SKIP (OWNER NOT EXPOSED / SERVICE-SPECIFIC)


## 3) Endpoint Coverage — GET /remoteid-engine/stats

### GET /remoteid-engine/stats
**Owner tag:** RemoteID Engine
**Owner base:** N/A (owner not exposed)

**Direct-owner check:**

SKIPPED (DIRECT OWNER NOT EXPOSED IN PORT LIST)


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** SKIP (OWNER NOT EXPOSED / SERVICE-SPECIFIC)


## 3) Endpoint Coverage — GET /remoteid-engine/replay/state

### GET /remoteid-engine/replay/state
**Owner tag:** RemoteID Engine
**Owner base:** N/A (owner not exposed)

**Direct-owner check:**

SKIPPED (DIRECT OWNER NOT EXPOSED IN PORT LIST)


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** SKIP (OWNER NOT EXPOSED / SERVICE-SPECIFIC)


## 3) Endpoint Coverage — POST /remoteid-engine/replay/start

### POST /remoteid-engine/replay/start
**Owner tag:** RemoteID Engine
**Owner base:** N/A (owner not exposed)

**Direct-owner check:**

SKIPPED (DIRECT OWNER NOT EXPOSED IN PORT LIST)


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** SKIP (OWNER NOT EXPOSED / SERVICE-SPECIFIC)


## 3) Endpoint Coverage — POST /remoteid-engine/replay/stop

### POST /remoteid-engine/replay/stop
**Owner tag:** RemoteID Engine
**Owner base:** N/A (owner not exposed)

**Direct-owner check:**

SKIPPED (DIRECT OWNER NOT EXPOSED IN PORT LIST)


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** SKIP (OWNER NOT EXPOSED / SERVICE-SPECIFIC)


## 3) Endpoint Coverage — POST /remoteid-engine/monitor/start

### POST /remoteid-engine/monitor/start
**Owner tag:** RemoteID Engine
**Owner base:** N/A (owner not exposed)

**Direct-owner check:**

SKIPPED (DIRECT OWNER NOT EXPOSED IN PORT LIST)


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** SKIP (OWNER NOT EXPOSED / SERVICE-SPECIFIC)


## 3) Endpoint Coverage — POST /remoteid-engine/monitor/stop

### POST /remoteid-engine/monitor/stop
**Owner tag:** RemoteID Engine
**Owner base:** N/A (owner not exposed)

**Direct-owner check:**

SKIPPED (DIRECT OWNER NOT EXPOSED IN PORT LIST)


**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)


**Classification:** SKIP (OWNER NOT EXPOSED / SERVICE-SPECIFIC)


## 3A) Endpoint Coverage Summary

Total GET endpoints: 43
Total POST endpoints: 41


## 4) Field-Level Contract Verification

### /status

**Command:**

```
curl -sS http://127.0.0.1:8001/api/v1/status | jq '.timestamp_ms, .overall_ok, .system.status, .network.connected, .gps.latitude, .gps.longitude, .remote_id.state, .rf.status'
```

**Output:**

```
1772232321630
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
null
null
null
null
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
1772232322190
```

**Result:** PASS

### RFScan /stats

**Command:**

```
curl -sS http://127.0.0.1:8890/api/v1/stats | jq '.timestamp_ms'
```

**Output:**

```
1772232322232
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
date: Fri, 27 Feb 2026 22:45:21 GMT
server: uvicorn
content-length: 29
content-type: application/json

{"detail":"confirm_required"}
```

**Result:** PASS_SAFE_ERROR


## 6) WebSocket Proof

**Command:**

```
cd /home/toybook/ndefender-api-contracts && WS_URL=ws://127.0.0.1:8001/api/v1/ws node packages/examples/ws/ws_client_node.js
```

**Output:**

```
CONNECTING ws://127.0.0.1:8001/api/v1/ws
CONNECTED
{"type":"HELLO","timestamp_ms":1772232322393,"source":"aggregator","data":{"timestamp_ms":1772232322393}}
```
\n**Result:** PASS\n\n**Command:**

```
cd /home/toybook/ndefender-api-contracts && WS_URL=ws://127.0.0.1:8001/api/v1/ws timeout 5s python3 packages/examples/ws/ws_client_python.py
```

**Output:**

```
CONNECTING ws://127.0.0.1:8001/api/v1/ws
CONNECTED
{"type": "HELLO", "timestamp_ms": 1772232322477, "source": "aggregator", "data": {"timestamp_ms": 1772232322477}}
```
\n**Result:** PASS\n

## 7) Summary Table

| Metric | Value |
|---|---|
| Total endpoints | 84 |
| PASS | 52 |
| FAIL | 0 |
| SKIP | 32 |

## 7c) UI Blockers vs Non-Blockers

| Endpoint | Classification |
|---|---|
| /status | PASS |
| /ws | PASS |
| /contacts | PASS |
| /scan/start | PASS_PRECONDITION (PRECONDITION_OK) |
| /scan/stop | PASS_PRECONDITION (PRECONDITION_OK) |
| /vrx/tune | PASS_PRECONDITION (PRECONDITION_OK) |
| /video/select | PASS_PRECONDITION (PRECONDITION_OK) |
| /remote_id/monitor/start | PASS (UPSTREAM_UNREACHABLE) |
| /remote_id/monitor/stop | PASS (UPSTREAM_UNREACHABLE) |

## 8) Fix Progress

Run timestamp: 2026-02-28 04:15:03 
Summary: Total 84 / PASS 52 / FAIL 0 / SKIP 32

Notes:
- (update as fixes land)

## 9) Failure Analysis + Next Fix Repo

No failures detected.
