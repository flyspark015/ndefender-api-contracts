# N-Defender Post-Deploy Evidence Pack (2026-02-27)

## Summary
- Generated on: Fri Feb 27 03:24:23 IST 2026
- Host: ndefender-pi
- Scope: Steps C–I (baseline, systemd, logs, REST, confirm gating, WS/validator, repo audit)

## Step C — Baseline Host + Ports
```text
$ uname -a
Linux ndefender-pi 6.12.62+rpt-rpi-2712 #1 SMP PREEMPT Debian 1:6.12.62-1+rpt1~bookworm (2026-01-19) aarch64 GNU/Linux

$ hostname
ndefender-pi

$ date
Fri Feb 27 03:19:35 IST 2026

$ ss -lntp | egrep '(:8001|:8002|:8890|:8000)\b' || true
LISTEN 0      128                      127.0.0.1:8890       0.0.0.0:*    users:(("ndefender-antsd",pid=2071035,fd=6))
LISTEN 0      128                        0.0.0.0:8000       0.0.0.0:*    users:(("python",pid=1151,fd=11))           
LISTEN 0      2048                     127.0.0.1:8001       0.0.0.0:*    users:(("uvicorn",pid=2076223,fd=7))        
LISTEN 0      2048                     127.0.0.1:8002       0.0.0.0:*    users:(("uvicorn",pid=2076239,fd=14))       
```

## Step D — systemd Health + Logs
### Unit Files
```text
$ systemctl list-unit-files | grep -E 'ndefender-(backend-aggregator|system-controller|rfscan|remoteid-engine|remoteid)' || true
ndefender-backend-aggregator.service               enabled         enabled
ndefender-remoteid-engine.service                  enabled         enabled
ndefender-remoteid-live.service                    disabled        enabled
ndefender-remoteid-replay.service                  disabled        enabled
ndefender-rfscan.service                           enabled         enabled
ndefender-system-controller.service                enabled         enabled
```

### systemctl status: backend-aggregator
```text
$ systemctl status ndefender-backend-aggregator --no-pager
● ndefender-backend-aggregator.service - N-Defender Backend Aggregator (FastAPI)
     Loaded: loaded (/etc/systemd/system/ndefender-backend-aggregator.service; enabled; preset: enabled)
     Active: active (running) since Fri 2026-02-27 02:56:24 IST; 23min ago
   Main PID: 2076223 (uvicorn)
      Tasks: 4 (limit: 19359)
        CPU: 14.959s
     CGroup: /system.slice/ndefender-backend-aggregator.service
             └─2076223 /home/toybook/.venvs/ndefender-agg/bin/python /home/toybook/.venvs/ndefender-agg/bin/uvicorn ndefender_backend_aggregator.main:app --host 127.0.0.1 --port 8001

Feb 27 03:19:22 ndefender-pi uvicorn[2076223]: 2026-02-27 03:19:22,377 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:19:26 ndefender-pi uvicorn[2076223]: 2026-02-27 03:19:26,342 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:19:28 ndefender-pi uvicorn[2076223]: 2026-02-27 03:19:28,347 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:19:30 ndefender-pi uvicorn[2076223]: 2026-02-27 03:19:30,355 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:19:34 ndefender-pi uvicorn[2076223]: 2026-02-27 03:19:34,359 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:19:36 ndefender-pi uvicorn[2076223]: 2026-02-27 03:19:36,364 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:19:38 ndefender-pi uvicorn[2076223]: 2026-02-27 03:19:38,369 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:19:42 ndefender-pi uvicorn[2076223]: 2026-02-27 03:19:42,377 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:19:44 ndefender-pi uvicorn[2076223]: 2026-02-27 03:19:44,381 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:19:46 ndefender-pi uvicorn[2076223]: 2026-02-27 03:19:46,392 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
```

### systemctl status: system-controller
```text
$ systemctl status ndefender-system-controller --no-pager
● ndefender-system-controller.service - N-Defender System Controller (FastAPI)
     Loaded: loaded (/etc/systemd/system/ndefender-system-controller.service; enabled; preset: enabled)
     Active: active (running) since Fri 2026-02-27 02:56:25 IST; 23min ago
   Main PID: 2076239 (uvicorn)
      Tasks: 8 (limit: 19359)
        CPU: 16.148s
     CGroup: /system.slice/ndefender-system-controller.service
             ├─2076239 /home/toybook/ndefender-system-controller/.venv/bin/python3 /home/toybook/ndefender-system-controller/.venv/bin/uvicorn ndefender_system_controller.main:app --host 127.0.0.1 --port 8002
             └─2102161 gpspipe -w -n 5

Feb 27 03:19:22 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:19:26 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:19:28 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:19:30 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:19:34 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:19:36 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:19:38 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:19:42 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:19:44 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:19:46 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
```

### systemctl status: rfscan
```text
$ systemctl status ndefender-rfscan --no-pager
● ndefender-rfscan.service - N-Defender RF Scan Service
     Loaded: loaded (/etc/systemd/system/ndefender-rfscan.service; enabled; preset: enabled)
     Active: active (running) since Fri 2026-02-27 02:52:26 IST; 27min ago
   Main PID: 2071035 (ndefender-antsd)
      Tasks: 4 (limit: 19359)
        CPU: 616ms
     CGroup: /system.slice/ndefender-rfscan.service
             └─2071035 /home/toybook/ndefender-antsdr-scan/.venv/bin/python3 /home/toybook/ndefender-antsdr-scan/.venv/bin/ndefender-antsdr-scan api --config /home/toybook/ndefender-antsdr-scan/config/production.yaml --bind 127.0.0.1 --port 8890

Feb 27 02:52:27 ndefender-pi ndefender-antsdr-scan[2071035]: ======== Running on http://127.0.0.1:8890 ========
Feb 27 02:52:27 ndefender-pi ndefender-antsdr-scan[2071035]: (Press CTRL+C to quit)
```

### systemctl status: remoteid-engine
```text
$ systemctl status ndefender-remoteid-engine --no-pager
● ndefender-remoteid-engine.service - N-Defender RemoteID Engine
     Loaded: loaded (/etc/systemd/system/ndefender-remoteid-engine.service; enabled; preset: enabled)
     Active: active (running) since Fri 2026-02-27 02:49:41 IST; 30min ago
   Main PID: 2067068 (ndefender-remot)
      Tasks: 3 (limit: 19359)
        CPU: 42.083s
     CGroup: /system.slice/ndefender-remoteid-engine.service
             ├─2067068 /home/toybook/Ndefender-Remoteid-Engine/.venv/bin/python /home/toybook/Ndefender-Remoteid-Engine/.venv/bin/ndefender-remoteid run --config /home/toybook/Ndefender-Remoteid-Engine/config/default.yaml
             ├─2067069 tshark -i mon0 -l -T ek
             └─2067119 /usr/bin/dumpcap -n -i mon0 -Z none
```

### journalctl: backend-aggregator (last 200)
```text
$ journalctl -u ndefender-backend-aggregator -n 200 --no-pager
Feb 27 03:12:31 ndefender-pi uvicorn[2076223]: INFO:     2401:4900:8fef:a440:69de:a6e0:f49b:2f21:0 - "GET /api/v1/network/bluetooth/state HTTP/1.1" 200 OK
Feb 27 03:12:31 ndefender-pi uvicorn[2076223]: 2026-02-27 03:12:31,708 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/network/bluetooth/devices "HTTP/1.1 200 OK"
Feb 27 03:12:31 ndefender-pi uvicorn[2076223]: INFO:     2401:4900:8fef:a440:69de:a6e0:f49b:2f21:0 - "GET /api/v1/network/bluetooth/devices HTTP/1.1" 200 OK
Feb 27 03:12:32 ndefender-pi uvicorn[2076223]: 2026-02-27 03:12:32,042 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:12:32 ndefender-pi uvicorn[2076223]: INFO:     2401:4900:8fef:a440:69de:a6e0:f49b:2f21:0 - "GET /api/v1/gps HTTP/1.1" 200 OK
Feb 27 03:12:32 ndefender-pi uvicorn[2076223]: INFO:     2401:4900:8fef:a440:69de:a6e0:f49b:2f21:0 - "GET /api/v1/esp32 HTTP/1.1" 200 OK
Feb 27 03:12:32 ndefender-pi uvicorn[2076223]: INFO:     2401:4900:8fef:a440:69de:a6e0:f49b:2f21:0 - "GET /api/v1/antsdr HTTP/1.1" 200 OK
Feb 27 03:12:33 ndefender-pi uvicorn[2076223]: INFO:     2401:4900:8fef:a440:69de:a6e0:f49b:2f21:0 - "GET /api/v1/remote_id HTTP/1.1" 200 OK
Feb 27 03:12:33 ndefender-pi uvicorn[2076223]: INFO:     2401:4900:8fef:a440:69de:a6e0:f49b:2f21:0 - "POST /api/v1/system/reboot HTTP/1.1" 400 Bad Request
Feb 27 03:12:34 ndefender-pi uvicorn[2076223]: 2026-02-27 03:12:34,047 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:12:34 ndefender-pi uvicorn[2076223]: INFO:     2401:4900:8fef:a440:69de:a6e0:f49b:2f21:0 - "WebSocket /api/v1/ws" [accepted]
Feb 27 03:12:34 ndefender-pi uvicorn[2076223]: INFO:     connection open
Feb 27 03:12:34 ndefender-pi uvicorn[2076223]: INFO:     connection closed
Feb 27 03:12:38 ndefender-pi uvicorn[2076223]: 2026-02-27 03:12:38,016 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:12:40 ndefender-pi uvicorn[2076223]: 2026-02-27 03:12:40,023 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:12:42 ndefender-pi uvicorn[2076223]: 2026-02-27 03:12:42,029 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:12:45 ndefender-pi uvicorn[2076223]: 2026-02-27 03:12:45,945 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:12:47 ndefender-pi uvicorn[2076223]: 2026-02-27 03:12:47,950 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:12:49 ndefender-pi uvicorn[2076223]: 2026-02-27 03:12:49,956 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:12:53 ndefender-pi uvicorn[2076223]: 2026-02-27 03:12:53,971 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:12:55 ndefender-pi uvicorn[2076223]: 2026-02-27 03:12:55,976 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:12:57 ndefender-pi uvicorn[2076223]: 2026-02-27 03:12:57,979 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:13:01 ndefender-pi uvicorn[2076223]: 2026-02-27 03:13:01,994 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:13:04 ndefender-pi uvicorn[2076223]: 2026-02-27 03:13:04,000 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:13:06 ndefender-pi uvicorn[2076223]: 2026-02-27 03:13:06,006 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:13:10 ndefender-pi uvicorn[2076223]: 2026-02-27 03:13:10,006 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:13:12 ndefender-pi uvicorn[2076223]: 2026-02-27 03:13:12,025 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:13:14 ndefender-pi uvicorn[2076223]: 2026-02-27 03:13:14,029 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:13:14 ndefender-pi uvicorn[2076223]: INFO:     2401:4900:8fef:a440:c091:1ebf:13cd:a3b3:0 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:13:17 ndefender-pi uvicorn[2076223]: 2026-02-27 03:13:17,992 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:13:19 ndefender-pi uvicorn[2076223]: 2026-02-27 03:13:19,996 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:13:21 ndefender-pi uvicorn[2076223]: INFO:     2406:da1a:c77:d408:c818:84a8:1f80:1749:0 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:13:22 ndefender-pi uvicorn[2076223]: 2026-02-27 03:13:22,000 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:13:22 ndefender-pi uvicorn[2076223]: INFO:     2406:da1a:c77:d404:e0f6:388:97ce:91ce:0 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:13:25 ndefender-pi uvicorn[2076223]: 2026-02-27 03:13:25,989 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:13:27 ndefender-pi uvicorn[2076223]: 2026-02-27 03:13:27,995 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:13:29 ndefender-pi uvicorn[2076223]: 2026-02-27 03:13:29,999 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:13:34 ndefender-pi uvicorn[2076223]: 2026-02-27 03:13:34,046 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:13:36 ndefender-pi uvicorn[2076223]: 2026-02-27 03:13:36,051 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:13:38 ndefender-pi uvicorn[2076223]: 2026-02-27 03:13:38,054 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:13:42 ndefender-pi uvicorn[2076223]: 2026-02-27 03:13:42,042 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:13:44 ndefender-pi uvicorn[2076223]: 2026-02-27 03:13:44,048 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:13:46 ndefender-pi uvicorn[2076223]: 2026-02-27 03:13:46,052 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:13:50 ndefender-pi uvicorn[2076223]: 2026-02-27 03:13:50,035 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:13:52 ndefender-pi uvicorn[2076223]: 2026-02-27 03:13:52,040 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:13:54 ndefender-pi uvicorn[2076223]: 2026-02-27 03:13:54,047 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:13:58 ndefender-pi uvicorn[2076223]: 2026-02-27 03:13:58,091 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:14:00 ndefender-pi uvicorn[2076223]: 2026-02-27 03:14:00,100 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:14:02 ndefender-pi uvicorn[2076223]: 2026-02-27 03:14:02,106 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:14:06 ndefender-pi uvicorn[2076223]: 2026-02-27 03:14:06,073 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:14:08 ndefender-pi uvicorn[2076223]: 2026-02-27 03:14:08,079 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:14:10 ndefender-pi uvicorn[2076223]: 2026-02-27 03:14:10,084 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:14:14 ndefender-pi uvicorn[2076223]: 2026-02-27 03:14:14,059 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:14:14 ndefender-pi uvicorn[2076223]: INFO:     2401:4900:8fef:a440:c091:1ebf:13cd:a3b3:0 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:14:16 ndefender-pi uvicorn[2076223]: 2026-02-27 03:14:16,065 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:14:18 ndefender-pi uvicorn[2076223]: 2026-02-27 03:14:18,069 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:14:21 ndefender-pi uvicorn[2076223]: INFO:     2406:da1a:c77:d404:669d:1f7b:5fc6:9466:0 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:14:22 ndefender-pi uvicorn[2076223]: INFO:     2406:da1a:c77:d40a:d032:5177:9a48:f5f9:0 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:14:22 ndefender-pi uvicorn[2076223]: 2026-02-27 03:14:22,067 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:14:24 ndefender-pi uvicorn[2076223]: 2026-02-27 03:14:24,071 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:14:26 ndefender-pi uvicorn[2076223]: 2026-02-27 03:14:26,075 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:14:30 ndefender-pi uvicorn[2076223]: 2026-02-27 03:14:30,067 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:14:32 ndefender-pi uvicorn[2076223]: 2026-02-27 03:14:32,071 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:14:34 ndefender-pi uvicorn[2076223]: 2026-02-27 03:14:34,075 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:14:38 ndefender-pi uvicorn[2076223]: 2026-02-27 03:14:38,085 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:14:40 ndefender-pi uvicorn[2076223]: 2026-02-27 03:14:40,090 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:14:42 ndefender-pi uvicorn[2076223]: 2026-02-27 03:14:42,093 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:14:46 ndefender-pi uvicorn[2076223]: 2026-02-27 03:14:46,099 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:14:48 ndefender-pi uvicorn[2076223]: 2026-02-27 03:14:48,106 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:14:50 ndefender-pi uvicorn[2076223]: 2026-02-27 03:14:50,110 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:14:54 ndefender-pi uvicorn[2076223]: 2026-02-27 03:14:54,148 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:14:56 ndefender-pi uvicorn[2076223]: 2026-02-27 03:14:56,153 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:14:58 ndefender-pi uvicorn[2076223]: 2026-02-27 03:14:58,158 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:15:02 ndefender-pi uvicorn[2076223]: 2026-02-27 03:15:02,105 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:15:04 ndefender-pi uvicorn[2076223]: 2026-02-27 03:15:04,109 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:15:06 ndefender-pi uvicorn[2076223]: 2026-02-27 03:15:06,113 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:15:10 ndefender-pi uvicorn[2076223]: 2026-02-27 03:15:10,141 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:15:12 ndefender-pi uvicorn[2076223]: 2026-02-27 03:15:12,146 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:15:14 ndefender-pi uvicorn[2076223]: 2026-02-27 03:15:14,149 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:15:14 ndefender-pi uvicorn[2076223]: INFO:     2401:4900:8fef:a440:c091:1ebf:13cd:a3b3:0 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:15:18 ndefender-pi uvicorn[2076223]: 2026-02-27 03:15:18,165 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:15:20 ndefender-pi uvicorn[2076223]: 2026-02-27 03:15:20,171 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:15:22 ndefender-pi uvicorn[2076223]: 2026-02-27 03:15:22,176 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:15:22 ndefender-pi uvicorn[2076223]: INFO:     2406:da1a:c77:d400:d411:51c:a937:1a21:0 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:15:22 ndefender-pi uvicorn[2076223]: INFO:     2406:da1a:c77:d400:cc95:9502:84c1:c888:0 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:15:26 ndefender-pi uvicorn[2076223]: 2026-02-27 03:15:26,123 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:15:28 ndefender-pi uvicorn[2076223]: 2026-02-27 03:15:28,158 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:15:30 ndefender-pi uvicorn[2076223]: 2026-02-27 03:15:30,163 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:15:34 ndefender-pi uvicorn[2076223]: 2026-02-27 03:15:34,192 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:15:36 ndefender-pi uvicorn[2076223]: 2026-02-27 03:15:36,198 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:15:38 ndefender-pi uvicorn[2076223]: 2026-02-27 03:15:38,202 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:15:42 ndefender-pi uvicorn[2076223]: 2026-02-27 03:15:42,220 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:15:44 ndefender-pi uvicorn[2076223]: 2026-02-27 03:15:44,242 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:15:46 ndefender-pi uvicorn[2076223]: 2026-02-27 03:15:46,247 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:15:50 ndefender-pi uvicorn[2076223]: 2026-02-27 03:15:50,199 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:15:52 ndefender-pi uvicorn[2076223]: 2026-02-27 03:15:52,204 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:15:54 ndefender-pi uvicorn[2076223]: 2026-02-27 03:15:54,212 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:15:58 ndefender-pi uvicorn[2076223]: 2026-02-27 03:15:58,188 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:16:00 ndefender-pi uvicorn[2076223]: 2026-02-27 03:16:00,194 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:16:02 ndefender-pi uvicorn[2076223]: 2026-02-27 03:16:02,199 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:16:06 ndefender-pi uvicorn[2076223]: 2026-02-27 03:16:06,261 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:16:08 ndefender-pi uvicorn[2076223]: 2026-02-27 03:16:08,267 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:16:10 ndefender-pi uvicorn[2076223]: 2026-02-27 03:16:10,270 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:16:14 ndefender-pi uvicorn[2076223]: 2026-02-27 03:16:14,213 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:16:14 ndefender-pi uvicorn[2076223]: INFO:     2401:4900:8fef:a440:c091:1ebf:13cd:a3b3:0 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:16:16 ndefender-pi uvicorn[2076223]: 2026-02-27 03:16:16,217 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:16:18 ndefender-pi uvicorn[2076223]: 2026-02-27 03:16:18,221 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:16:21 ndefender-pi uvicorn[2076223]: INFO:     2406:da1a:c77:d407:284c:956f:8b32:1b7a:0 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:16:22 ndefender-pi uvicorn[2076223]: INFO:     2406:da1a:c77:d402:ac65:921:15e7:50bb:0 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:16:22 ndefender-pi uvicorn[2076223]: 2026-02-27 03:16:22,223 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:16:24 ndefender-pi uvicorn[2076223]: 2026-02-27 03:16:24,229 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:16:26 ndefender-pi uvicorn[2076223]: 2026-02-27 03:16:26,234 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:16:30 ndefender-pi uvicorn[2076223]: 2026-02-27 03:16:30,224 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:16:32 ndefender-pi uvicorn[2076223]: 2026-02-27 03:16:32,230 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:16:34 ndefender-pi uvicorn[2076223]: 2026-02-27 03:16:34,235 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:16:38 ndefender-pi uvicorn[2076223]: 2026-02-27 03:16:38,207 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:16:40 ndefender-pi uvicorn[2076223]: 2026-02-27 03:16:40,214 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:16:42 ndefender-pi uvicorn[2076223]: 2026-02-27 03:16:42,220 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:16:46 ndefender-pi uvicorn[2076223]: 2026-02-27 03:16:46,216 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:16:48 ndefender-pi uvicorn[2076223]: 2026-02-27 03:16:48,221 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:16:50 ndefender-pi uvicorn[2076223]: 2026-02-27 03:16:50,224 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:16:54 ndefender-pi uvicorn[2076223]: 2026-02-27 03:16:54,216 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:16:56 ndefender-pi uvicorn[2076223]: 2026-02-27 03:16:56,220 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:16:58 ndefender-pi uvicorn[2076223]: 2026-02-27 03:16:58,224 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:17:02 ndefender-pi uvicorn[2076223]: 2026-02-27 03:17:02,304 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:17:04 ndefender-pi uvicorn[2076223]: 2026-02-27 03:17:04,308 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:17:06 ndefender-pi uvicorn[2076223]: 2026-02-27 03:17:06,312 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:17:10 ndefender-pi uvicorn[2076223]: 2026-02-27 03:17:10,204 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:17:12 ndefender-pi uvicorn[2076223]: 2026-02-27 03:17:12,208 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:17:14 ndefender-pi uvicorn[2076223]: 2026-02-27 03:17:14,212 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:17:14 ndefender-pi uvicorn[2076223]: INFO:     2401:4900:8fef:a440:c091:1ebf:13cd:a3b3:0 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:17:18 ndefender-pi uvicorn[2076223]: 2026-02-27 03:17:18,207 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:17:20 ndefender-pi uvicorn[2076223]: 2026-02-27 03:17:20,211 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:17:21 ndefender-pi uvicorn[2076223]: INFO:     2406:da1a:c77:d40b:7ef1:a3f8:e593:a480:0 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:17:22 ndefender-pi uvicorn[2076223]: INFO:     2406:da1a:c77:d401:3371:f5e9:1b99:d55f:0 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:17:22 ndefender-pi uvicorn[2076223]: 2026-02-27 03:17:22,215 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:17:26 ndefender-pi uvicorn[2076223]: 2026-02-27 03:17:26,371 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:17:28 ndefender-pi uvicorn[2076223]: 2026-02-27 03:17:28,377 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:17:30 ndefender-pi uvicorn[2076223]: 2026-02-27 03:17:30,387 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:17:34 ndefender-pi uvicorn[2076223]: 2026-02-27 03:17:34,255 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:17:36 ndefender-pi uvicorn[2076223]: 2026-02-27 03:17:36,259 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:17:38 ndefender-pi uvicorn[2076223]: 2026-02-27 03:17:38,304 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:17:42 ndefender-pi uvicorn[2076223]: 2026-02-27 03:17:42,275 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:17:44 ndefender-pi uvicorn[2076223]: 2026-02-27 03:17:44,280 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:17:46 ndefender-pi uvicorn[2076223]: 2026-02-27 03:17:46,284 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:17:50 ndefender-pi uvicorn[2076223]: 2026-02-27 03:17:50,273 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:17:52 ndefender-pi uvicorn[2076223]: 2026-02-27 03:17:52,278 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:17:54 ndefender-pi uvicorn[2076223]: 2026-02-27 03:17:54,282 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:17:58 ndefender-pi uvicorn[2076223]: 2026-02-27 03:17:58,285 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:18:00 ndefender-pi uvicorn[2076223]: 2026-02-27 03:18:00,293 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:18:02 ndefender-pi uvicorn[2076223]: 2026-02-27 03:18:02,297 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:18:06 ndefender-pi uvicorn[2076223]: 2026-02-27 03:18:06,371 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:18:08 ndefender-pi uvicorn[2076223]: 2026-02-27 03:18:08,376 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:18:10 ndefender-pi uvicorn[2076223]: 2026-02-27 03:18:10,382 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:18:14 ndefender-pi uvicorn[2076223]: 2026-02-27 03:18:14,308 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:18:14 ndefender-pi uvicorn[2076223]: INFO:     2401:4900:8fef:a440:c091:1ebf:13cd:a3b3:0 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:18:15 ndefender-pi uvicorn[2076223]: INFO:     23.27.145.157:0 - "GET / HTTP/1.1" 404 Not Found
Feb 27 03:18:16 ndefender-pi uvicorn[2076223]: 2026-02-27 03:18:16,314 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:18:18 ndefender-pi uvicorn[2076223]: 2026-02-27 03:18:18,318 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:18:21 ndefender-pi uvicorn[2076223]: INFO:     2406:da1a:c77:d40b:953b:ddd5:d05d:36cc:0 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:18:22 ndefender-pi uvicorn[2076223]: INFO:     2406:da1a:c77:d407:37e8:da7:704c:8c5a:0 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:18:22 ndefender-pi uvicorn[2076223]: 2026-02-27 03:18:22,284 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:18:24 ndefender-pi uvicorn[2076223]: 2026-02-27 03:18:24,288 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:18:26 ndefender-pi uvicorn[2076223]: 2026-02-27 03:18:26,296 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:18:30 ndefender-pi uvicorn[2076223]: 2026-02-27 03:18:30,328 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:18:32 ndefender-pi uvicorn[2076223]: 2026-02-27 03:18:32,335 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:18:34 ndefender-pi uvicorn[2076223]: 2026-02-27 03:18:34,340 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:18:38 ndefender-pi uvicorn[2076223]: 2026-02-27 03:18:38,370 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:18:40 ndefender-pi uvicorn[2076223]: 2026-02-27 03:18:40,396 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:18:42 ndefender-pi uvicorn[2076223]: 2026-02-27 03:18:42,401 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:18:46 ndefender-pi uvicorn[2076223]: 2026-02-27 03:18:46,314 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:18:48 ndefender-pi uvicorn[2076223]: 2026-02-27 03:18:48,319 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:18:50 ndefender-pi uvicorn[2076223]: 2026-02-27 03:18:50,323 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:18:54 ndefender-pi uvicorn[2076223]: 2026-02-27 03:18:54,361 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:18:56 ndefender-pi uvicorn[2076223]: 2026-02-27 03:18:56,367 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:18:58 ndefender-pi uvicorn[2076223]: 2026-02-27 03:18:58,373 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:19:02 ndefender-pi uvicorn[2076223]: 2026-02-27 03:19:02,336 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:19:04 ndefender-pi uvicorn[2076223]: 2026-02-27 03:19:04,340 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:19:06 ndefender-pi uvicorn[2076223]: 2026-02-27 03:19:06,343 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:19:10 ndefender-pi uvicorn[2076223]: 2026-02-27 03:19:10,325 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:19:12 ndefender-pi uvicorn[2076223]: 2026-02-27 03:19:12,353 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:19:14 ndefender-pi uvicorn[2076223]: 2026-02-27 03:19:14,359 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:19:14 ndefender-pi uvicorn[2076223]: INFO:     2401:4900:8fef:a440:c091:1ebf:13cd:a3b3:0 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:19:18 ndefender-pi uvicorn[2076223]: 2026-02-27 03:19:18,368 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:19:20 ndefender-pi uvicorn[2076223]: 2026-02-27 03:19:20,372 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:19:21 ndefender-pi uvicorn[2076223]: INFO:     2406:da1a:c77:d401:9150:d363:782c:853e:0 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:19:22 ndefender-pi uvicorn[2076223]: INFO:     2406:da1a:c77:d404:ffd:79e3:4935:d3fd:0 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:19:22 ndefender-pi uvicorn[2076223]: 2026-02-27 03:19:22,377 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:19:26 ndefender-pi uvicorn[2076223]: 2026-02-27 03:19:26,342 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:19:28 ndefender-pi uvicorn[2076223]: 2026-02-27 03:19:28,347 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:19:30 ndefender-pi uvicorn[2076223]: 2026-02-27 03:19:30,355 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:19:34 ndefender-pi uvicorn[2076223]: 2026-02-27 03:19:34,359 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:19:36 ndefender-pi uvicorn[2076223]: 2026-02-27 03:19:36,364 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:19:38 ndefender-pi uvicorn[2076223]: 2026-02-27 03:19:38,369 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:19:42 ndefender-pi uvicorn[2076223]: 2026-02-27 03:19:42,377 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:19:44 ndefender-pi uvicorn[2076223]: 2026-02-27 03:19:44,381 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:19:46 ndefender-pi uvicorn[2076223]: 2026-02-27 03:19:46,392 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:19:50 ndefender-pi uvicorn[2076223]: 2026-02-27 03:19:50,404 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:19:52 ndefender-pi uvicorn[2076223]: 2026-02-27 03:19:52,410 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
Feb 27 03:19:54 ndefender-pi uvicorn[2076223]: 2026-02-27 03:19:54,415 INFO httpx HTTP Request: GET http://127.0.0.1:8002/api/v1/status "HTTP/1.1 200 OK"
```

### journalctl: system-controller (last 200)
```text
$ journalctl -u ndefender-system-controller -n 200 --no-pager
Feb 27 03:12:09 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:12:14 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:12:14 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:35912 - "GET /api/v1/network/wifi/state HTTP/1.1" 200 OK
Feb 27 03:12:14 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:35912 - "GET /api/v1/network/wifi/scan HTTP/1.1" 200 OK
Feb 27 03:12:14 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:35912 - "GET /api/v1/network/bluetooth/state HTTP/1.1" 200 OK
Feb 27 03:12:14 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:35912 - "GET /api/v1/network/bluetooth/devices HTTP/1.1" 200 OK
Feb 27 03:12:14 ndefender-pi uvicorn[2093594]: Error: failed to set Wi-Fi radio: Not authorized to perform this operation
Feb 27 03:12:14 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:35912 - "POST /api/v1/network/wifi/disable HTTP/1.1" 200 OK
Feb 27 03:12:14 ndefender-pi uvicorn[2093604]: Changing power off succeeded
Feb 27 03:12:14 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:35912 - "POST /api/v1/network/bluetooth/disable HTTP/1.1" 200 OK
Feb 27 03:12:14 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:50148 - "GET /api/v1/health HTTP/1.1" 200 OK
Feb 27 03:12:17 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:50162 - "GET /api/v1/gps HTTP/1.1" 200 OK
Feb 27 03:12:17 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:12:17 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:50174 - "GET /api/v1/network/wifi/state HTTP/1.1" 200 OK
Feb 27 03:12:17 ndefender-pi uvicorn[2093676]: Error: failed to set Wi-Fi radio: Not authorized to perform this operation
Feb 27 03:12:17 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:50176 - "POST /api/v1/network/wifi/disable HTTP/1.1" 200 OK
Feb 27 03:12:21 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:12:22 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:50184 - "GET /api/v1/network/wifi/state HTTP/1.1" 200 OK
Feb 27 03:12:22 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:50184 - "GET /api/v1/network/wifi/scan HTTP/1.1" 200 OK
Feb 27 03:12:22 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:50184 - "GET /api/v1/network/bluetooth/state HTTP/1.1" 200 OK
Feb 27 03:12:22 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:50184 - "GET /api/v1/network/bluetooth/devices HTTP/1.1" 200 OK
Feb 27 03:12:23 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:12:25 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:12:26 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:50184 - "GET /api/v1/network/wifi/state HTTP/1.1" 200 OK
Feb 27 03:12:26 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:50184 - "GET /api/v1/network/wifi/scan HTTP/1.1" 200 OK
Feb 27 03:12:26 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:50184 - "GET /api/v1/network/bluetooth/state HTTP/1.1" 200 OK
Feb 27 03:12:26 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:50184 - "GET /api/v1/network/bluetooth/devices HTTP/1.1" 200 OK
Feb 27 03:12:30 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:50184 - "GET /api/v1/network/wifi/state HTTP/1.1" 200 OK
Feb 27 03:12:30 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:12:30 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:50184 - "GET /api/v1/network/wifi/scan HTTP/1.1" 200 OK
Feb 27 03:12:31 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:50184 - "GET /api/v1/network/bluetooth/state HTTP/1.1" 200 OK
Feb 27 03:12:31 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:50184 - "GET /api/v1/network/bluetooth/devices HTTP/1.1" 200 OK
Feb 27 03:12:32 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:12:34 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:12:38 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:12:40 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:12:42 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:12:45 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:12:47 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:12:49 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:12:53 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:12:55 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:12:57 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:13:01 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:13:04 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:13:06 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:13:10 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:13:12 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:13:14 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:13:17 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:13:19 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:13:21 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:13:25 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:13:27 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:13:29 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:13:34 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:13:36 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:13:38 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:13:42 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:13:44 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:13:46 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:13:50 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:13:52 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:13:54 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:13:58 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:14:00 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:14:02 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:14:06 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:14:08 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:14:10 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:14:14 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:14:16 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:14:18 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:14:22 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:14:24 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:14:26 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:14:30 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:14:32 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:14:34 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:14:38 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:14:40 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:14:42 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:14:46 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:14:48 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:14:50 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:14:54 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:14:56 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:14:58 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:15:02 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:15:04 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:15:06 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:15:10 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:15:12 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:15:14 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:15:18 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:15:20 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:15:22 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:15:26 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:15:28 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:15:30 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:15:34 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:15:36 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:15:38 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:15:42 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:15:44 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:15:46 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:15:50 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:15:52 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:15:54 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:15:58 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:16:00 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:16:02 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:16:06 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:16:08 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:16:10 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:16:14 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:16:16 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:16:18 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:16:22 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:16:24 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:16:26 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:16:30 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:16:32 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:16:34 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:16:38 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:16:40 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:16:42 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:16:46 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:16:48 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:16:50 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:16:54 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:16:56 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:16:58 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:17:02 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:17:04 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:17:06 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:17:10 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:17:12 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:17:14 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:17:18 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:17:20 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:17:22 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:17:26 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:17:28 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:17:30 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:17:34 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:17:36 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:17:38 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:17:42 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:17:44 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:17:46 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:17:50 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:17:52 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:17:54 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:17:58 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:18:00 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:18:02 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:18:06 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:18:08 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:18:10 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:18:14 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:18:16 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:18:18 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:18:22 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:18:24 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:18:26 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:18:30 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:18:32 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:18:34 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:18:38 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:18:40 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:18:42 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:18:46 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:18:48 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:18:50 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:18:54 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:18:56 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:18:58 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:19:02 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:19:04 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:19:06 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:19:10 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:19:12 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:19:14 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:19:18 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:19:20 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:19:22 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:19:26 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:19:28 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:19:30 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:19:34 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:19:36 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:19:38 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:19:42 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:19:44 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:19:46 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:19:50 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:19:52 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:19:54 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
Feb 27 03:19:58 ndefender-pi uvicorn[2076239]: INFO:     127.0.0.1:59554 - "GET /api/v1/status HTTP/1.1" 200 OK
```

### journalctl: rfscan (last 200)
```text
$ journalctl -u ndefender-rfscan -n 200 --no-pager
Feb 27 02:49:36 ndefender-pi python3[2038875]: {"t":1772140776.8368096,"detector":"peak","type":"PEAK","severity":2,"data":{"center_hz":1338000000,"peak_freq_hz":1338140693.6645508,"snr_db":38.946499786627584,"peak_db":128.11364808296722,"noise_floor_db":89.16714829633963,"bandwidth_class":"narrow"}}
Feb 27 02:49:36 ndefender-pi python3[2038875]: {"type":"RF_CONTACT_UPDATE","ts_ms":1772140776836,"id":"rf:1338000000","data":{"center_hz":1338000000,"bandwidth_class":"narrow","family_hint":"unknown","snr_db":38.946499786627584,"peak_db":128.11364808296722}}
Feb 27 02:49:36 ndefender-pi python3[2038875]: {"t":1772140776.8368096,"detector":"peak","type":"PEAK","severity":2,"data":{"center_hz":1338000000,"peak_freq_hz":1338548103.3325195,"snr_db":43.41791308015607,"peak_db":132.5850613764957,"noise_floor_db":89.16714829633963,"bandwidth_class":"narrow"}}
Feb 27 02:49:36 ndefender-pi python3[2038875]: {"type":"RF_CONTACT_UPDATE","ts_ms":1772140776836,"id":"rf:1338000000","data":{"center_hz":1338000000,"bandwidth_class":"narrow","family_hint":"unknown","snr_db":43.41791308015607,"peak_db":132.5850613764957}}
Feb 27 02:49:36 ndefender-pi python3[2038875]: {"t":1772140776.8368096,"detector":"peak","type":"PEAK","severity":2,"data":{"center_hz":1338000000,"peak_freq_hz":1338802734.375,"snr_db":35.561046264727906,"peak_db":124.72819456106754,"noise_floor_db":89.16714829633963,"bandwidth_class":"narrow"}}
Feb 27 02:49:36 ndefender-pi python3[2038875]: {"type":"RF_CONTACT_UPDATE","ts_ms":1772140776836,"id":"rf:1338000000","data":{"center_hz":1338000000,"bandwidth_class":"narrow","family_hint":"unknown","snr_db":35.561046264727906,"peak_db":124.72819456106754}}
Feb 27 02:49:36 ndefender-pi python3[2038875]: {"type":"RF_CONTACT_LOST","ts_ms":1772140776850,"id":"rf:1318000000","data":{"center_hz":1318000000,"bandwidth_class":"narrow","family_hint":"unknown","snr_db":39.03879981801187,"peak_db":127.32190498809894}}
Feb 27 02:49:37 ndefender-pi python3[2038875]: {"t":1772140777.119281,"detector":"peak","type":"PEAK","severity":2,"data":{"center_hz":1340000000,"peak_freq_hz":1339159225.4638672,"snr_db":46.515340390385916,"peak_db":135.93264427950874,"noise_floor_db":89.41730388912282,"bandwidth_class":"narrow"}}
Feb 27 02:49:37 ndefender-pi python3[2038875]: {"type":"RF_CONTACT_NEW","ts_ms":1772140777119,"id":"rf:1340000000","data":{"center_hz":1340000000,"bandwidth_class":"narrow","family_hint":"unknown","snr_db":46.515340390385916,"peak_db":135.93264427950874}}
Feb 27 02:49:37 ndefender-pi python3[2038875]: {"t":1772140777.119281,"detector":"peak","type":"PEAK","severity":2,"data":{"center_hz":1340000000,"peak_freq_hz":1339413864.1357422,"snr_db":40.15106095338467,"peak_db":129.5683648425075,"noise_floor_db":89.41730388912282,"bandwidth_class":"narrow"}}
Feb 27 02:49:37 ndefender-pi python3[2038875]: {"type":"RF_CONTACT_UPDATE","ts_ms":1772140777119,"id":"rf:1340000000","data":{"center_hz":1340000000,"bandwidth_class":"narrow","family_hint":"unknown","snr_db":40.15106095338467,"peak_db":129.5683648425075}}
Feb 27 02:49:37 ndefender-pi python3[2038875]: {"t":1772140777.119281,"detector":"peak","type":"PEAK","severity":2,"data":{"center_hz":1340000000,"peak_freq_hz":1339770347.5952148,"snr_db":50.571520082277885,"peak_db":139.9888239714007,"noise_floor_db":89.41730388912282,"bandwidth_class":"narrow"}}
Feb 27 02:49:37 ndefender-pi python3[2038875]: {"type":"RF_CONTACT_UPDATE","ts_ms":1772140777119,"id":"rf:1340000000","data":{"center_hz":1340000000,"bandwidth_class":"narrow","family_hint":"unknown","snr_db":50.571520082277885,"peak_db":139.9888239714007}}
Feb 27 02:49:37 ndefender-pi python3[2038875]: {"t":1772140777.119281,"detector":"peak","type":"PEAK","severity":2,"data":{"center_hz":1340000000,"peak_freq_hz":1340228683.4716797,"snr_db":46.27263341242099,"peak_db":135.6899373015438,"noise_floor_db":89.41730388912282,"bandwidth_class":"narrow"}}
Feb 27 02:49:37 ndefender-pi python3[2038875]: {"type":"RF_CONTACT_UPDATE","ts_ms":1772140777119,"id":"rf:1340000000","data":{"center_hz":1340000000,"bandwidth_class":"narrow","family_hint":"unknown","snr_db":46.27263341242099,"peak_db":135.6899373015438}}
Feb 27 02:49:37 ndefender-pi python3[2038875]: {"t":1772140777.119281,"detector":"peak","type":"PEAK","severity":2,"data":{"center_hz":1340000000,"peak_freq_hz":1340483314.5141602,"snr_db":42.9861543880514,"peak_db":132.40345827717422,"noise_floor_db":89.41730388912282,"bandwidth_class":"narrow"}}
Feb 27 02:49:37 ndefender-pi python3[2038875]: {"type":"RF_CONTACT_UPDATE","ts_ms":1772140777119,"id":"rf:1340000000","data":{"center_hz":1340000000,"bandwidth_class":"narrow","family_hint":"unknown","snr_db":42.9861543880514,"peak_db":132.40345827717422}}
Feb 27 02:49:37 ndefender-pi python3[2038875]: {"t":1772140777.119281,"detector":"peak","type":"PEAK","severity":2,"data":{"center_hz":1340000000,"peak_freq_hz":1340839797.9736328,"snr_db":44.56990254982455,"peak_db":133.98720643894737,"noise_floor_db":89.41730388912282,"bandwidth_class":"narrow"}}
Feb 27 02:49:37 ndefender-pi python3[2038875]: {"type":"RF_CONTACT_UPDATE","ts_ms":1772140777119,"id":"rf:1340000000","data":{"center_hz":1340000000,"bandwidth_class":"narrow","family_hint":"unknown","snr_db":44.56990254982455,"peak_db":133.98720643894737}}
Feb 27 02:49:37 ndefender-pi python3[2038875]: {"type":"RF_CONTACT_LOST","ts_ms":1772140777137,"id":"rf:1320000000","data":{"center_hz":1320000000,"bandwidth_class":"narrow","family_hint":"unknown","snr_db":39.46332778896296,"peak_db":127.62444284224969}}
Feb 27 02:49:37 ndefender-pi python3[2038875]: {"t":1772140777.3632033,"detector":"peak","type":"PEAK","severity":2,"data":{"center_hz":1342000000,"peak_freq_hz":1341145347.5952148,"snr_db":35.44093450559822,"peak_db":122.93530640790902,"noise_floor_db":87.4943719023108,"bandwidth_class":"narrow"}}
Feb 27 02:49:37 ndefender-pi python3[2038875]: {"type":"RF_CONTACT_NEW","ts_ms":1772140777363,"id":"rf:1342000000","data":{"center_hz":1342000000,"bandwidth_class":"narrow","family_hint":"unknown","snr_db":35.44093450559822,"peak_db":122.93530640790902}}
Feb 27 02:49:37 ndefender-pi python3[2038875]: {"t":1772140777.3632033,"detector":"peak","type":"PEAK","severity":2,"data":{"center_hz":1342000000,"peak_freq_hz":1341501831.0546875,"snr_db":39.44854661476589,"peak_db":126.94291851707669,"noise_floor_db":87.4943719023108,"bandwidth_class":"narrow"}}
Feb 27 02:49:37 ndefender-pi python3[2038875]: {"type":"RF_CONTACT_UPDATE","ts_ms":1772140777363,"id":"rf:1342000000","data":{"center_hz":1342000000,"bandwidth_class":"narrow","family_hint":"unknown","snr_db":39.44854661476589,"peak_db":126.94291851707669}}
Feb 27 02:49:37 ndefender-pi python3[2038875]: {"t":1772140777.3632033,"detector":"peak","type":"PEAK","severity":2,"data":{"center_hz":1342000000,"peak_freq_hz":1342011100.769043,"snr_db":41.091351448755745,"peak_db":128.58572335106655,"noise_floor_db":87.4943719023108,"bandwidth_class":"narrow"}}
Feb 27 02:49:37 ndefender-pi python3[2038875]: {"t":1772140777.3632033,"detector":"peak","type":"PEAK","severity":2,"data":{"center_hz":1342000000,"peak_freq_hz":1342316658.0200195,"snr_db":41.95975139141447,"peak_db":129.45412329372527,"noise_floor_db":87.4943719023108,"bandwidth_class":"narrow"}}
Feb 27 02:49:37 ndefender-pi python3[2038875]: {"type":"RF_CONTACT_UPDATE","ts_ms":1772140777363,"id":"rf:1342000000","data":{"center_hz":1342000000,"bandwidth_class":"narrow","family_hint":"unknown","snr_db":41.95975139141447,"peak_db":129.45412329372527}}
Feb 27 02:49:37 ndefender-pi python3[2038875]: {"t":1772140777.3632033,"detector":"peak","type":"PEAK","severity":2,"data":{"center_hz":1342000000,"peak_freq_hz":1342622215.270996,"snr_db":34.77825114112389,"peak_db":122.27262304343469,"noise_floor_db":87.4943719023108,"bandwidth_class":"narrow"}}
Feb 27 02:49:37 ndefender-pi python3[2038875]: {"type":"RF_CONTACT_UPDATE","ts_ms":1772140777363,"id":"rf:1342000000","data":{"center_hz":1342000000,"bandwidth_class":"narrow","family_hint":"unknown","snr_db":34.77825114112389,"peak_db":122.27262304343469}}
Feb 27 02:49:37 ndefender-pi python3[2038875]: {"t":1772140777.3632033,"detector":"peak","type":"PEAK","severity":2,"data":{"center_hz":1342000000,"peak_freq_hz":1342876846.3134766,"snr_db":30.24401392995148,"peak_db":117.73838583226228,"noise_floor_db":87.4943719023108,"bandwidth_class":"narrow"}}
Feb 27 02:49:37 ndefender-pi python3[2038875]: {"type":"RF_CONTACT_UPDATE","ts_ms":1772140777363,"id":"rf:1342000000","data":{"center_hz":1342000000,"bandwidth_class":"narrow","family_hint":"unknown","snr_db":30.24401392995148,"peak_db":117.73838583226228}}
Feb 27 02:49:37 ndefender-pi python3[2038875]: {"type":"RF_CONTACT_LOST","ts_ms":1772140777378,"id":"rf:1322000000","data":{"center_hz":1322000000,"bandwidth_class":"narrow","family_hint":"unknown","snr_db":33.23684073433141,"peak_db":121.72016789183196}}
Feb 27 02:49:37 ndefender-pi python3[2038875]: {"t":1772140777.6283581,"detector":"peak","type":"PEAK","severity":2,"data":{"center_hz":1344000000,"peak_freq_hz":1343131484.9853516,"snr_db":41.477259799286585,"peak_db":126.90138426063987,"noise_floor_db":85.42412446135329,"bandwidth_class":"narrow"}}
Feb 27 02:49:37 ndefender-pi python3[2038875]: {"type":"RF_CONTACT_NEW","ts_ms":1772140777628,"id":"rf:1344000000","data":{"center_hz":1344000000,"bandwidth_class":"narrow","family_hint":"unknown","snr_db":41.477259799286585,"peak_db":126.90138426063987}}
Feb 27 02:49:37 ndefender-pi python3[2038875]: {"t":1772140777.6283581,"detector":"peak","type":"PEAK","severity":2,"data":{"center_hz":1344000000,"peak_freq_hz":1343538894.6533203,"snr_db":40.92643747020176,"peak_db":126.35056193155505,"noise_floor_db":85.42412446135329,"bandwidth_class":"narrow"}}
Feb 27 02:49:37 ndefender-pi python3[2038875]: {"type":"RF_CONTACT_UPDATE","ts_ms":1772140777628,"id":"rf:1344000000","data":{"center_hz":1344000000,"bandwidth_class":"narrow","family_hint":"unknown","snr_db":40.92643747020176,"peak_db":126.35056193155505}}
Feb 27 02:49:37 ndefender-pi python3[2038875]: {"t":1772140777.6283581,"detector":"peak","type":"PEAK","severity":2,"data":{"center_hz":1344000000,"peak_freq_hz":1344019096.3745117,"snr_db":57.59904024231709,"peak_db":143.02316470367037,"noise_floor_db":85.42412446135329,"bandwidth_class":"narrow"}}
Feb 27 02:49:37 ndefender-pi python3[2038875]: {"t":1772140777.6283581,"detector":"peak","type":"PEAK","severity":2,"data":{"center_hz":1344000000,"peak_freq_hz":1344302787.7807617,"snr_db":39.258884913537216,"peak_db":124.6830093748905,"noise_floor_db":85.42412446135329,"bandwidth_class":"narrow"}}
Feb 27 02:49:37 ndefender-pi python3[2038875]: {"type":"RF_CONTACT_UPDATE","ts_ms":1772140777628,"id":"rf:1344000000","data":{"center_hz":1344000000,"bandwidth_class":"narrow","family_hint":"unknown","snr_db":39.258884913537216,"peak_db":124.6830093748905}}
Feb 27 02:49:37 ndefender-pi python3[2038875]: {"t":1772140777.6283581,"detector":"peak","type":"PEAK","severity":2,"data":{"center_hz":1344000000,"peak_freq_hz":1344659271.2402344,"snr_db":37.8393800417839,"peak_db":123.26350450313718,"noise_floor_db":85.42412446135329,"bandwidth_class":"narrow"}}
Feb 27 02:49:37 ndefender-pi python3[2038875]: {"type":"RF_CONTACT_UPDATE","ts_ms":1772140777628,"id":"rf:1344000000","data":{"center_hz":1344000000,"bandwidth_class":"narrow","family_hint":"unknown","snr_db":37.8393800417839,"peak_db":123.26350450313718}}
Feb 27 02:49:37 ndefender-pi python3[2038875]: {"type":"RF_CONTACT_LOST","ts_ms":1772140777684,"id":"rf:1324000000","data":{"center_hz":1324000000,"bandwidth_class":"narrow","family_hint":"unknown","snr_db":42.40641276873008,"peak_db":132.1601146127543}}
Feb 27 02:49:37 ndefender-pi python3[2038875]: {"t":1772140777.8845031,"detector":"peak","type":"PEAK","severity":2,"data":{"center_hz":1346000000,"peak_freq_hz":1345321311.9506836,"snr_db":39.47568329417588,"peak_db":125.22464575668793,"noise_floor_db":85.74896246251205,"bandwidth_class":"narrow"}}
Feb 27 02:49:37 ndefender-pi python3[2038875]: {"type":"RF_CONTACT_NEW","ts_ms":1772140777884,"id":"rf:1346000000","data":{"center_hz":1346000000,"bandwidth_class":"narrow","family_hint":"unknown","snr_db":39.47568329417588,"peak_db":125.22464575668793}}
Feb 27 02:49:37 ndefender-pi python3[2038875]: {"t":1772140777.8845031,"detector":"peak","type":"PEAK","severity":2,"data":{"center_hz":1346000000,"peak_freq_hz":1345779647.8271484,"snr_db":40.67949059827774,"peak_db":126.42845306078979,"noise_floor_db":85.74896246251205,"bandwidth_class":"narrow"}}
Feb 27 02:49:37 ndefender-pi python3[2038875]: {"type":"RF_CONTACT_UPDATE","ts_ms":1772140777884,"id":"rf:1346000000","data":{"center_hz":1346000000,"bandwidth_class":"narrow","family_hint":"unknown","snr_db":40.67949059827774,"peak_db":126.42845306078979}}
Feb 27 02:49:37 ndefender-pi python3[2038875]: {"t":1772140777.8845031,"detector":"peak","type":"PEAK","severity":2,"data":{"center_hz":1346000000,"peak_freq_hz":1346085205.078125,"snr_db":31.868844341488312,"peak_db":117.61780680400037,"noise_floor_db":85.74896246251205,"bandwidth_class":"narrow"}}
Feb 27 02:49:37 ndefender-pi python3[2038875]: {"t":1772140777.8845031,"detector":"peak","type":"PEAK","severity":2,"data":{"center_hz":1346000000,"peak_freq_hz":1346339836.1206055,"snr_db":41.1669616186921,"peak_db":126.91592408120415,"noise_floor_db":85.74896246251205,"bandwidth_class":"narrow"}}
Feb 27 02:49:37 ndefender-pi python3[2038875]: {"type":"RF_CONTACT_UPDATE","ts_ms":1772140777884,"id":"rf:1346000000","data":{"center_hz":1346000000,"bandwidth_class":"narrow","family_hint":"unknown","snr_db":41.1669616186921,"peak_db":126.91592408120415}}
Feb 27 02:49:37 ndefender-pi python3[2038875]: {"t":1772140777.8845031,"detector":"peak","type":"PEAK","severity":2,"data":{"center_hz":1346000000,"peak_freq_hz":1346594467.163086,"snr_db":23.43066488722927,"peak_db":109.17962734974132,"noise_floor_db":85.74896246251205,"bandwidth_class":"narrow"}}
Feb 27 02:49:37 ndefender-pi python3[2038875]: {"type":"RF_CONTACT_UPDATE","ts_ms":1772140777884,"id":"rf:1346000000","data":{"center_hz":1346000000,"bandwidth_class":"narrow","family_hint":"unknown","snr_db":23.43066488722927,"peak_db":109.17962734974132}}
Feb 27 02:49:37 ndefender-pi python3[2038875]: {"t":1772140777.8845031,"detector":"peak","type":"PEAK","severity":2,"data":{"center_hz":1346000000,"peak_freq_hz":1346849098.2055664,"snr_db":37.9523614139015,"peak_db":123.70132387641355,"noise_floor_db":85.74896246251205,"bandwidth_class":"narrow"}}
Feb 27 02:49:37 ndefender-pi python3[2038875]: {"type":"RF_CONTACT_UPDATE","ts_ms":1772140777884,"id":"rf:1346000000","data":{"center_hz":1346000000,"bandwidth_class":"narrow","family_hint":"unknown","snr_db":37.9523614139015,"peak_db":123.70132387641355}}
Feb 27 02:49:37 ndefender-pi python3[2038875]: {"type":"RF_CONTACT_LOST","ts_ms":1772140777896,"id":"rf:1326000000","data":{"center_hz":1326000000,"bandwidth_class":"narrow","family_hint":"unknown","snr_db":39.33428008247084,"peak_db":128.57091482087196}}
Feb 27 02:49:38 ndefender-pi python3[2038875]: {"t":1772140778.1698608,"detector":"peak","type":"PEAK","severity":2,"data":{"center_hz":1348000000,"peak_freq_hz":1347103736.8774414,"snr_db":30.11887445287877,"peak_db":114.71248095546903,"noise_floor_db":84.59360650259026,"bandwidth_class":"narrow"}}
Feb 27 02:49:38 ndefender-pi python3[2038875]: {"type":"RF_CONTACT_NEW","ts_ms":1772140778169,"id":"rf:1348000000","data":{"center_hz":1348000000,"bandwidth_class":"narrow","family_hint":"unknown","snr_db":30.11887445287877,"peak_db":114.71248095546903}}
Feb 27 02:49:38 ndefender-pi python3[2038875]: {"t":1772140778.1698608,"detector":"peak","type":"PEAK","severity":2,"data":{"center_hz":1348000000,"peak_freq_hz":1347511146.5454102,"snr_db":37.70283259393693,"peak_db":122.2964390965272,"noise_floor_db":84.59360650259026,"bandwidth_class":"narrow"}}
Feb 27 02:49:38 ndefender-pi python3[2038875]: {"type":"RF_CONTACT_UPDATE","ts_ms":1772140778169,"id":"rf:1348000000","data":{"center_hz":1348000000,"bandwidth_class":"narrow","family_hint":"unknown","snr_db":37.70283259393693,"peak_db":122.2964390965272}}
Feb 27 02:49:38 ndefender-pi python3[2038875]: {"t":1772140778.1698608,"detector":"peak","type":"PEAK","severity":2,"data":{"center_hz":1348000000,"peak_freq_hz":1347765777.5878906,"snr_db":34.72575504828134,"peak_db":119.3193615508716,"noise_floor_db":84.59360650259026,"bandwidth_class":"narrow"}}
Feb 27 02:49:38 ndefender-pi python3[2038875]: {"type":"RF_CONTACT_UPDATE","ts_ms":1772140778169,"id":"rf:1348000000","data":{"center_hz":1348000000,"bandwidth_class":"narrow","family_hint":"unknown","snr_db":34.72575504828134,"peak_db":119.3193615508716}}
Feb 27 02:49:38 ndefender-pi python3[2038875]: {"t":1772140778.1698608,"detector":"peak","type":"PEAK","severity":2,"data":{"center_hz":1348000000,"peak_freq_hz":1348071334.8388672,"snr_db":42.99000739088473,"peak_db":127.58361389347499,"noise_floor_db":84.59360650259026,"bandwidth_class":"narrow"}}
Feb 27 02:49:38 ndefender-pi python3[2038875]: {"t":1772140778.1698608,"detector":"peak","type":"PEAK","severity":2,"data":{"center_hz":1348000000,"peak_freq_hz":1348326026.916504,"snr_db":28.64293672643514,"peak_db":113.2365432290254,"noise_floor_db":84.59360650259026,"bandwidth_class":"narrow"}}
Feb 27 02:49:38 ndefender-pi python3[2038875]: {"type":"RF_CONTACT_UPDATE","ts_ms":1772140778169,"id":"rf:1348000000","data":{"center_hz":1348000000,"bandwidth_class":"narrow","family_hint":"unknown","snr_db":28.64293672643514,"peak_db":113.2365432290254}}
Feb 27 02:49:38 ndefender-pi python3[2038875]: {"t":1772140778.1698608,"detector":"peak","type":"PEAK","severity":2,"data":{"center_hz":1348000000,"peak_freq_hz":1348682449.3408203,"snr_db":42.579012183609535,"peak_db":127.1726186861998,"noise_floor_db":84.59360650259026,"bandwidth_class":"narrow"}}
Feb 27 02:49:38 ndefender-pi python3[2038875]: {"type":"RF_CONTACT_UPDATE","ts_ms":1772140778169,"id":"rf:1348000000","data":{"center_hz":1348000000,"bandwidth_class":"narrow","family_hint":"unknown","snr_db":42.579012183609535,"peak_db":127.1726186861998}}
Feb 27 02:49:38 ndefender-pi python3[2038875]: {"type":"RF_CONTACT_LOST","ts_ms":1772140778184,"id":"rf:1328000000","data":{"center_hz":1328000000,"bandwidth_class":"narrow","family_hint":"unknown","snr_db":27.157920869420465,"peak_db":115.27201767178069}}
Feb 27 02:49:38 ndefender-pi python3[2038875]: {"t":1772140778.419304,"detector":"peak","type":"PEAK","severity":2,"data":{"center_hz":1350000000,"peak_freq_hz":1349242637.6342773,"snr_db":40.81884237301571,"peak_db":126.27747252582728,"noise_floor_db":85.45863015281157,"bandwidth_class":"narrow"}}
Feb 27 02:49:38 ndefender-pi python3[2038875]: {"type":"RF_CONTACT_NEW","ts_ms":1772140778419,"id":"rf:1350000000","data":{"center_hz":1350000000,"bandwidth_class":"narrow","family_hint":"unknown","snr_db":40.81884237301571,"peak_db":126.27747252582728}}
Feb 27 02:49:38 ndefender-pi python3[2038875]: {"t":1772140778.419304,"detector":"peak","type":"PEAK","severity":2,"data":{"center_hz":1350000000,"peak_freq_hz":1349497268.6767578,"snr_db":40.94288840688307,"peak_db":126.40151855969464,"noise_floor_db":85.45863015281157,"bandwidth_class":"narrow"}}
Feb 27 02:49:38 ndefender-pi python3[2038875]: {"type":"RF_CONTACT_UPDATE","ts_ms":1772140778419,"id":"rf:1350000000","data":{"center_hz":1350000000,"bandwidth_class":"narrow","family_hint":"unknown","snr_db":40.94288840688307,"peak_db":126.40151855969464}}
Feb 27 02:49:38 ndefender-pi python3[2038875]: {"t":1772140778.419304,"detector":"peak","type":"PEAK","severity":2,"data":{"center_hz":1350000000,"peak_freq_hz":1349946846.0083008,"snr_db":42.737596770685315,"peak_db":128.19622692349688,"noise_floor_db":85.45863015281157,"bandwidth_class":"narrow"}}
Feb 27 02:49:38 ndefender-pi python3[2038875]: {"t":1772140778.419304,"detector":"peak","type":"PEAK","severity":2,"data":{"center_hz":1350000000,"peak_freq_hz":1350210235.5957031,"snr_db":39.06981005040181,"peak_db":124.52844020321338,"noise_floor_db":85.45863015281157,"bandwidth_class":"narrow"}}
Feb 27 02:49:38 ndefender-pi python3[2038875]: {"type":"RF_CONTACT_UPDATE","ts_ms":1772140778419,"id":"rf:1350000000","data":{"center_hz":1350000000,"bandwidth_class":"narrow","family_hint":"unknown","snr_db":39.06981005040181,"peak_db":124.52844020321338}}
Feb 27 02:49:38 ndefender-pi python3[2038875]: {"t":1772140778.419304,"detector":"peak","type":"PEAK","severity":2,"data":{"center_hz":1350000000,"peak_freq_hz":1350566726.6845703,"snr_db":36.72227679893636,"peak_db":122.18090695174793,"noise_floor_db":85.45863015281157,"bandwidth_class":"narrow"}}
Feb 27 02:49:38 ndefender-pi python3[2038875]: {"type":"RF_CONTACT_UPDATE","ts_ms":1772140778419,"id":"rf:1350000000","data":{"center_hz":1350000000,"bandwidth_class":"narrow","family_hint":"unknown","snr_db":36.72227679893636,"peak_db":122.18090695174793}}
Feb 27 02:49:38 ndefender-pi python3[2038875]: {"t":1772140778.419304,"detector":"peak","type":"PEAK","severity":2,"data":{"center_hz":1350000000,"peak_freq_hz":1350821357.7270508,"snr_db":39.920930733337045,"peak_db":125.37956088614861,"noise_floor_db":85.45863015281157,"bandwidth_class":"narrow"}}
Feb 27 02:49:38 ndefender-pi python3[2038875]: {"type":"RF_CONTACT_UPDATE","ts_ms":1772140778419,"id":"rf:1350000000","data":{"center_hz":1350000000,"bandwidth_class":"narrow","family_hint":"unknown","snr_db":39.920930733337045,"peak_db":125.37956088614861}}
Feb 27 02:49:38 ndefender-pi python3[2038875]: {"type":"RF_CONTACT_LOST","ts_ms":1772140778430,"id":"rf:1330000000","data":{"center_hz":1330000000,"bandwidth_class":"narrow","family_hint":"unknown","snr_db":38.6525889563453,"peak_db":126.89975329542527}}
Feb 27 02:49:43 ndefender-pi ndefender-antsdr-scan[2067071]: Traceback (most recent call last):
Feb 27 02:49:43 ndefender-pi ndefender-antsdr-scan[2067071]:   File "/home/toybook/ndefender-antsdr-scan/.venv/bin/ndefender-antsdr-scan", line 8, in <module>
Feb 27 02:49:43 ndefender-pi ndefender-antsdr-scan[2067071]:     sys.exit(main())
Feb 27 02:49:43 ndefender-pi ndefender-antsdr-scan[2067071]:              ^^^^^^
Feb 27 02:49:43 ndefender-pi ndefender-antsdr-scan[2067071]:   File "/home/toybook/ndefender-antsdr-scan/src/ndefender_antsdr_scan/cli/main.py", line 147, in main
Feb 27 02:49:43 ndefender-pi ndefender-antsdr-scan[2067071]:     return int(args.func(args))
Feb 27 02:49:43 ndefender-pi ndefender-antsdr-scan[2067071]:                ^^^^^^^^^^^^^^^
Feb 27 02:49:43 ndefender-pi ndefender-antsdr-scan[2067071]:   File "/home/toybook/ndefender-antsdr-scan/src/ndefender_antsdr_scan/cli/main.py", line 71, in _cmd_api
Feb 27 02:49:43 ndefender-pi ndefender-antsdr-scan[2067071]:     return run_api_server(
Feb 27 02:49:43 ndefender-pi ndefender-antsdr-scan[2067071]:            ^^^^^^^^^^^^^^^
Feb 27 02:49:43 ndefender-pi ndefender-antsdr-scan[2067071]:   File "/home/toybook/ndefender-antsdr-scan/src/ndefender_antsdr_scan/api/server.py", line 413, in run_api_server
Feb 27 02:49:43 ndefender-pi ndefender-antsdr-scan[2067071]:     config = load_config(config_path)
Feb 27 02:49:43 ndefender-pi ndefender-antsdr-scan[2067071]:              ^^^^^^^^^^^^^^^^^^^^^^^^
Feb 27 02:49:43 ndefender-pi ndefender-antsdr-scan[2067071]:   File "/home/toybook/ndefender-antsdr-scan/src/ndefender_antsdr_scan/core/config.py", line 60, in load_config
Feb 27 02:49:43 ndefender-pi ndefender-antsdr-scan[2067071]:     bands = _load_bands(config_path, sweep)
Feb 27 02:49:43 ndefender-pi ndefender-antsdr-scan[2067071]:             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Feb 27 02:49:43 ndefender-pi ndefender-antsdr-scan[2067071]:   File "/home/toybook/ndefender-antsdr-scan/src/ndefender_antsdr_scan/core/config.py", line 129, in _load_bands
Feb 27 02:49:43 ndefender-pi ndefender-antsdr-scan[2067071]:     plan_file = (config_path.parent / plan_path).resolve()
Feb 27 02:49:43 ndefender-pi ndefender-antsdr-scan[2067071]:                  ~~~~~~~~~~~~~~~~~~~^~~~~~~~~~~
Feb 27 02:49:43 ndefender-pi ndefender-antsdr-scan[2067071]: TypeError: unsupported operand type(s) for /: 'PosixPath' and 'dict'
Feb 27 02:49:49 ndefender-pi ndefender-antsdr-scan[2067369]: Traceback (most recent call last):
Feb 27 02:49:49 ndefender-pi ndefender-antsdr-scan[2067369]:   File "/home/toybook/ndefender-antsdr-scan/.venv/bin/ndefender-antsdr-scan", line 8, in <module>
Feb 27 02:49:49 ndefender-pi ndefender-antsdr-scan[2067369]:     sys.exit(main())
Feb 27 02:49:49 ndefender-pi ndefender-antsdr-scan[2067369]:              ^^^^^^
Feb 27 02:49:49 ndefender-pi ndefender-antsdr-scan[2067369]:   File "/home/toybook/ndefender-antsdr-scan/src/ndefender_antsdr_scan/cli/main.py", line 147, in main
Feb 27 02:49:49 ndefender-pi ndefender-antsdr-scan[2067369]:     return int(args.func(args))
Feb 27 02:49:49 ndefender-pi ndefender-antsdr-scan[2067369]:                ^^^^^^^^^^^^^^^
Feb 27 02:49:49 ndefender-pi ndefender-antsdr-scan[2067369]:   File "/home/toybook/ndefender-antsdr-scan/src/ndefender_antsdr_scan/cli/main.py", line 71, in _cmd_api
Feb 27 02:49:49 ndefender-pi ndefender-antsdr-scan[2067369]:     return run_api_server(
Feb 27 02:49:49 ndefender-pi ndefender-antsdr-scan[2067369]:            ^^^^^^^^^^^^^^^
Feb 27 02:49:49 ndefender-pi ndefender-antsdr-scan[2067369]:   File "/home/toybook/ndefender-antsdr-scan/src/ndefender_antsdr_scan/api/server.py", line 413, in run_api_server
Feb 27 02:49:49 ndefender-pi ndefender-antsdr-scan[2067369]:     config = load_config(config_path)
Feb 27 02:49:49 ndefender-pi ndefender-antsdr-scan[2067369]:              ^^^^^^^^^^^^^^^^^^^^^^^^
Feb 27 02:49:49 ndefender-pi ndefender-antsdr-scan[2067369]:   File "/home/toybook/ndefender-antsdr-scan/src/ndefender_antsdr_scan/core/config.py", line 60, in load_config
Feb 27 02:49:49 ndefender-pi ndefender-antsdr-scan[2067369]:     bands = _load_bands(config_path, sweep)
Feb 27 02:49:49 ndefender-pi ndefender-antsdr-scan[2067369]:             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Feb 27 02:49:49 ndefender-pi ndefender-antsdr-scan[2067369]:   File "/home/toybook/ndefender-antsdr-scan/src/ndefender_antsdr_scan/core/config.py", line 129, in _load_bands
Feb 27 02:49:49 ndefender-pi ndefender-antsdr-scan[2067369]:     plan_file = (config_path.parent / plan_path).resolve()
Feb 27 02:49:49 ndefender-pi ndefender-antsdr-scan[2067369]:                  ~~~~~~~~~~~~~~~~~~~^~~~~~~~~~~
Feb 27 02:49:49 ndefender-pi ndefender-antsdr-scan[2067369]: TypeError: unsupported operand type(s) for /: 'PosixPath' and 'dict'
Feb 27 02:49:55 ndefender-pi ndefender-antsdr-scan[2067598]: Traceback (most recent call last):
Feb 27 02:49:55 ndefender-pi ndefender-antsdr-scan[2067598]:   File "/home/toybook/ndefender-antsdr-scan/.venv/bin/ndefender-antsdr-scan", line 8, in <module>
Feb 27 02:49:55 ndefender-pi ndefender-antsdr-scan[2067598]:     sys.exit(main())
Feb 27 02:49:55 ndefender-pi ndefender-antsdr-scan[2067598]:              ^^^^^^
Feb 27 02:49:55 ndefender-pi ndefender-antsdr-scan[2067598]:   File "/home/toybook/ndefender-antsdr-scan/src/ndefender_antsdr_scan/cli/main.py", line 147, in main
Feb 27 02:49:55 ndefender-pi ndefender-antsdr-scan[2067598]:     return int(args.func(args))
Feb 27 02:49:55 ndefender-pi ndefender-antsdr-scan[2067598]:                ^^^^^^^^^^^^^^^
Feb 27 02:49:55 ndefender-pi ndefender-antsdr-scan[2067598]:   File "/home/toybook/ndefender-antsdr-scan/src/ndefender_antsdr_scan/cli/main.py", line 71, in _cmd_api
Feb 27 02:49:55 ndefender-pi ndefender-antsdr-scan[2067598]:     return run_api_server(
Feb 27 02:49:55 ndefender-pi ndefender-antsdr-scan[2067598]:            ^^^^^^^^^^^^^^^
Feb 27 02:49:55 ndefender-pi ndefender-antsdr-scan[2067598]:   File "/home/toybook/ndefender-antsdr-scan/src/ndefender_antsdr_scan/api/server.py", line 413, in run_api_server
Feb 27 02:49:55 ndefender-pi ndefender-antsdr-scan[2067598]:     config = load_config(config_path)
Feb 27 02:49:55 ndefender-pi ndefender-antsdr-scan[2067598]:              ^^^^^^^^^^^^^^^^^^^^^^^^
Feb 27 02:49:55 ndefender-pi ndefender-antsdr-scan[2067598]:   File "/home/toybook/ndefender-antsdr-scan/src/ndefender_antsdr_scan/core/config.py", line 60, in load_config
Feb 27 02:49:55 ndefender-pi ndefender-antsdr-scan[2067598]:     bands = _load_bands(config_path, sweep)
Feb 27 02:49:55 ndefender-pi ndefender-antsdr-scan[2067598]:             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Feb 27 02:49:55 ndefender-pi ndefender-antsdr-scan[2067598]:   File "/home/toybook/ndefender-antsdr-scan/src/ndefender_antsdr_scan/core/config.py", line 129, in _load_bands
Feb 27 02:49:55 ndefender-pi ndefender-antsdr-scan[2067598]:     plan_file = (config_path.parent / plan_path).resolve()
Feb 27 02:49:55 ndefender-pi ndefender-antsdr-scan[2067598]:                  ~~~~~~~~~~~~~~~~~~~^~~~~~~~~~~
Feb 27 02:49:55 ndefender-pi ndefender-antsdr-scan[2067598]: TypeError: unsupported operand type(s) for /: 'PosixPath' and 'dict'
Feb 27 02:50:02 ndefender-pi ndefender-antsdr-scan[2067792]: Traceback (most recent call last):
Feb 27 02:50:02 ndefender-pi ndefender-antsdr-scan[2067792]:   File "/home/toybook/ndefender-antsdr-scan/.venv/bin/ndefender-antsdr-scan", line 8, in <module>
Feb 27 02:50:02 ndefender-pi ndefender-antsdr-scan[2067792]:     sys.exit(main())
Feb 27 02:50:02 ndefender-pi ndefender-antsdr-scan[2067792]:              ^^^^^^
Feb 27 02:50:02 ndefender-pi ndefender-antsdr-scan[2067792]:   File "/home/toybook/ndefender-antsdr-scan/src/ndefender_antsdr_scan/cli/main.py", line 147, in main
Feb 27 02:50:02 ndefender-pi ndefender-antsdr-scan[2067792]:     return int(args.func(args))
Feb 27 02:50:02 ndefender-pi ndefender-antsdr-scan[2067792]:                ^^^^^^^^^^^^^^^
Feb 27 02:50:02 ndefender-pi ndefender-antsdr-scan[2067792]:   File "/home/toybook/ndefender-antsdr-scan/src/ndefender_antsdr_scan/cli/main.py", line 71, in _cmd_api
Feb 27 02:50:02 ndefender-pi ndefender-antsdr-scan[2067792]:     return run_api_server(
Feb 27 02:50:02 ndefender-pi ndefender-antsdr-scan[2067792]:            ^^^^^^^^^^^^^^^
Feb 27 02:50:02 ndefender-pi ndefender-antsdr-scan[2067792]:   File "/home/toybook/ndefender-antsdr-scan/src/ndefender_antsdr_scan/api/server.py", line 413, in run_api_server
Feb 27 02:50:02 ndefender-pi ndefender-antsdr-scan[2067792]:     config = load_config(config_path)
Feb 27 02:50:02 ndefender-pi ndefender-antsdr-scan[2067792]:              ^^^^^^^^^^^^^^^^^^^^^^^^
Feb 27 02:50:02 ndefender-pi ndefender-antsdr-scan[2067792]:   File "/home/toybook/ndefender-antsdr-scan/src/ndefender_antsdr_scan/core/config.py", line 60, in load_config
Feb 27 02:50:02 ndefender-pi ndefender-antsdr-scan[2067792]:     bands = _load_bands(config_path, sweep)
Feb 27 02:50:02 ndefender-pi ndefender-antsdr-scan[2067792]:             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Feb 27 02:50:02 ndefender-pi ndefender-antsdr-scan[2067792]:   File "/home/toybook/ndefender-antsdr-scan/src/ndefender_antsdr_scan/core/config.py", line 129, in _load_bands
Feb 27 02:50:02 ndefender-pi ndefender-antsdr-scan[2067792]:     plan_file = (config_path.parent / plan_path).resolve()
Feb 27 02:50:02 ndefender-pi ndefender-antsdr-scan[2067792]:                  ~~~~~~~~~~~~~~~~~~~^~~~~~~~~~~
Feb 27 02:50:02 ndefender-pi ndefender-antsdr-scan[2067792]: TypeError: unsupported operand type(s) for /: 'PosixPath' and 'dict'
Feb 27 02:50:08 ndefender-pi ndefender-antsdr-scan[2068003]: Traceback (most recent call last):
Feb 27 02:50:08 ndefender-pi ndefender-antsdr-scan[2068003]:   File "/home/toybook/ndefender-antsdr-scan/.venv/bin/ndefender-antsdr-scan", line 8, in <module>
Feb 27 02:50:08 ndefender-pi ndefender-antsdr-scan[2068003]:     sys.exit(main())
Feb 27 02:50:08 ndefender-pi ndefender-antsdr-scan[2068003]:              ^^^^^^
Feb 27 02:50:08 ndefender-pi ndefender-antsdr-scan[2068003]:   File "/home/toybook/ndefender-antsdr-scan/src/ndefender_antsdr_scan/cli/main.py", line 147, in main
Feb 27 02:50:08 ndefender-pi ndefender-antsdr-scan[2068003]:     return int(args.func(args))
Feb 27 02:50:08 ndefender-pi ndefender-antsdr-scan[2068003]:                ^^^^^^^^^^^^^^^
Feb 27 02:50:08 ndefender-pi ndefender-antsdr-scan[2068003]:   File "/home/toybook/ndefender-antsdr-scan/src/ndefender_antsdr_scan/cli/main.py", line 71, in _cmd_api
Feb 27 02:50:08 ndefender-pi ndefender-antsdr-scan[2068003]:     return run_api_server(
Feb 27 02:50:08 ndefender-pi ndefender-antsdr-scan[2068003]:            ^^^^^^^^^^^^^^^
Feb 27 02:50:08 ndefender-pi ndefender-antsdr-scan[2068003]:   File "/home/toybook/ndefender-antsdr-scan/src/ndefender_antsdr_scan/api/server.py", line 413, in run_api_server
Feb 27 02:50:08 ndefender-pi ndefender-antsdr-scan[2068003]:     config = load_config(config_path)
Feb 27 02:50:08 ndefender-pi ndefender-antsdr-scan[2068003]:              ^^^^^^^^^^^^^^^^^^^^^^^^
Feb 27 02:50:08 ndefender-pi ndefender-antsdr-scan[2068003]:   File "/home/toybook/ndefender-antsdr-scan/src/ndefender_antsdr_scan/core/config.py", line 60, in load_config
Feb 27 02:50:08 ndefender-pi ndefender-antsdr-scan[2068003]:     bands = _load_bands(config_path, sweep)
Feb 27 02:50:08 ndefender-pi ndefender-antsdr-scan[2068003]:             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Feb 27 02:50:08 ndefender-pi ndefender-antsdr-scan[2068003]:   File "/home/toybook/ndefender-antsdr-scan/src/ndefender_antsdr_scan/core/config.py", line 129, in _load_bands
Feb 27 02:50:08 ndefender-pi ndefender-antsdr-scan[2068003]:     plan_file = (config_path.parent / plan_path).resolve()
Feb 27 02:50:08 ndefender-pi ndefender-antsdr-scan[2068003]:                  ~~~~~~~~~~~~~~~~~~~^~~~~~~~~~~
Feb 27 02:50:08 ndefender-pi ndefender-antsdr-scan[2068003]: TypeError: unsupported operand type(s) for /: 'PosixPath' and 'dict'
Feb 27 02:50:14 ndefender-pi ndefender-antsdr-scan[2068195]: Traceback (most recent call last):
Feb 27 02:50:14 ndefender-pi ndefender-antsdr-scan[2068195]:   File "/home/toybook/ndefender-antsdr-scan/.venv/bin/ndefender-antsdr-scan", line 8, in <module>
Feb 27 02:50:14 ndefender-pi ndefender-antsdr-scan[2068195]:     sys.exit(main())
Feb 27 02:50:14 ndefender-pi ndefender-antsdr-scan[2068195]:              ^^^^^^
Feb 27 02:50:14 ndefender-pi ndefender-antsdr-scan[2068195]:   File "/home/toybook/ndefender-antsdr-scan/src/ndefender_antsdr_scan/cli/main.py", line 147, in main
Feb 27 02:50:14 ndefender-pi ndefender-antsdr-scan[2068195]:     return int(args.func(args))
Feb 27 02:50:14 ndefender-pi ndefender-antsdr-scan[2068195]:                ^^^^^^^^^^^^^^^
Feb 27 02:50:14 ndefender-pi ndefender-antsdr-scan[2068195]:   File "/home/toybook/ndefender-antsdr-scan/src/ndefender_antsdr_scan/cli/main.py", line 71, in _cmd_api
Feb 27 02:50:14 ndefender-pi ndefender-antsdr-scan[2068195]:     return run_api_server(
Feb 27 02:50:14 ndefender-pi ndefender-antsdr-scan[2068195]:            ^^^^^^^^^^^^^^^
Feb 27 02:50:14 ndefender-pi ndefender-antsdr-scan[2068195]:   File "/home/toybook/ndefender-antsdr-scan/src/ndefender_antsdr_scan/api/server.py", line 413, in run_api_server
Feb 27 02:50:14 ndefender-pi ndefender-antsdr-scan[2068195]:     config = load_config(config_path)
Feb 27 02:50:14 ndefender-pi ndefender-antsdr-scan[2068195]:              ^^^^^^^^^^^^^^^^^^^^^^^^
Feb 27 02:50:14 ndefender-pi ndefender-antsdr-scan[2068195]:   File "/home/toybook/ndefender-antsdr-scan/src/ndefender_antsdr_scan/core/config.py", line 60, in load_config
Feb 27 02:50:14 ndefender-pi ndefender-antsdr-scan[2068195]:     bands = _load_bands(config_path, sweep)
Feb 27 02:50:14 ndefender-pi ndefender-antsdr-scan[2068195]:             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Feb 27 02:50:14 ndefender-pi ndefender-antsdr-scan[2068195]:   File "/home/toybook/ndefender-antsdr-scan/src/ndefender_antsdr_scan/core/config.py", line 129, in _load_bands
Feb 27 02:50:14 ndefender-pi ndefender-antsdr-scan[2068195]:     plan_file = (config_path.parent / plan_path).resolve()
Feb 27 02:50:14 ndefender-pi ndefender-antsdr-scan[2068195]:                  ~~~~~~~~~~~~~~~~~~~^~~~~~~~~~~
Feb 27 02:50:14 ndefender-pi ndefender-antsdr-scan[2068195]: TypeError: unsupported operand type(s) for /: 'PosixPath' and 'dict'
Feb 27 02:52:27 ndefender-pi ndefender-antsdr-scan[2071035]: ======== Running on http://127.0.0.1:8890 ========
Feb 27 02:52:27 ndefender-pi ndefender-antsdr-scan[2071035]: (Press CTRL+C to quit)
```

### journalctl: remoteid-engine (last 200)
```text
$ journalctl -u ndefender-remoteid-engine -n 200 --no-pager
-- No entries --
```

## Step E — REST Smoke Tests (Local)
```text
$ curl -sS http://127.0.0.1:8001/api/v1/health
{"status":"ok","timestamp_ms":1772142613669}
$ curl -sS http://127.0.0.1:8001/api/v1/status
{"timestamp_ms":1772142613680,"overall_ok":false,"system":{"cpu_temp_c":39.1,"cpu_usage_percent":10.3,"load_1m":3.3251953125,"load_5m":2.6220703125,"load_15m":2.52294921875,"ram_used_mb":2328,"ram_total_mb":16215,"disk_used_gb":66,"disk_total_gb":116,"uptime_s":85958,"throttled_flags":0,"status":"ok","timestamp_ms":1772142610398,"version":{"app":"ndefender-system-controller","git_sha":null,"build_ts":null},"cpu":{"temp_c":39.1,"load1":3.3251953125,"load5":2.6220703125,"load15":2.52294921875,"usage_percent":10.3},"ram":{"total_mb":16215,"used_mb":2328,"free_mb":13886},"storage":{"root":{"total_gb":116.606,"used_gb":66.089,"free_gb":44.573},"logs":null},"last_error":null},"power":{"pack_voltage_v":16.354,"current_a":-0.008,"input_vbus_v":0.0,"input_power_w":0.0,"soc_percent":93,"state":"IDLE","time_to_empty_s":2001600,"time_to_full_s":null,"status":"ok","timestamp_ms":1772142610405,"per_cell_v":[4.089,4.089,4.088,4.089],"last_error":null},"rf":{"last_event":{"reason":"no_rf_events"},"last_event_type":"RF_SCAN_OFFLINE","last_timestamp_ms":1772142608769,"scan_active":false,"status":"degraded","last_error":"no_rf_events"},"remote_id":{"last_event":{"reason":"no_odid_frames"},"last_event_type":"REMOTEID_STALE","last_timestamp_ms":1772142613195,"state":"DEGRADED","mode":"live","capture_active":true,"contacts_active":0,"last_update_ms":1772142613195,"last_error":"no_odid_frames"},"gps":{"timestamp_ms":1772142603256,"fix":"NO_FIX","satellites":{"in_view":0,"in_use":0},"hdop":null,"vdop":null,"pdop":null,"latitude":null,"longitude":null,"altitude_m":null,"speed_m_s":null,"heading_deg":null,"last_update_ms":1772142603256,"age_ms":null,"source":"gpsd","last_error":"gpsd_no_data"},"esp32":{"timestamp_ms":1772142612917,"connected":true,"last_seen_ms":1772142612917,"rtt_ms":null,"fw_version":null,"heartbeat":{"ok":true,"interval_ms":999,"last_heartbeat_ms":1772142612917},"capabilities":{"buttons":false,"leds":true,"buzzer":false,"vrx":true,"video_switch":true,"config":false},"last_error":null},"antsdr":{"timestamp_ms":1772142608769,"connected":false,"uri":"ip:192.168.10.2","temperature_c":null,"last_error":"no_rf_events"},"vrx":{"selected":1,"vrx":[{"id":1,"freq_hz":5783000000,"rssi_raw":894},{"id":2,"freq_hz":5783000000,"rssi_raw":426},{"id":3,"freq_hz":5783000000,"rssi_raw":174}],"led":{"r":0,"y":0,"g":1},"sys":{"uptime_ms":3409364,"heap":337624,"status":"CONNECTED"},"scan_state":"idle"},"fpv":{"selected":1,"locked_channels":[],"rssi_raw":894,"scan_state":"idle","freq_hz":5783000000},"video":{"selected":1,"status":"ok"},"services":[],"network":{"connected":true,"ip_v4":"127.0.1.1","ip_v6":null,"ssid":"Airtel_Toybook","wifi":{"timestamp_ms":1772142606275,"enabled":true,"connected":true,"ssid":"Airtel_Toybook","bssid":"2E\\","ip":"127.0.1.1","rssi_dbm":null,"link_quality":null,"last_update_ms":1772142606275,"last_error":null},"bluetooth":{"timestamp_ms":1772142606369,"enabled":false,"scanning":false,"paired_count":0,"connected_devices":[],"last_update_ms":1772142606369,"last_error":null}},"audio":{"muted":null,"volume_percent":null,"status":"degraded","timestamp_ms":1772142606273,"last_error":"audio_unavailable"},"contacts":[{"id":"fpv:1","type":"FPV","source":"esp32","last_seen_ts":1772142612917,"severity":"unknown","vrx_id":1,"freq_hz":5783000000,"rssi_raw":894,"selected":1,"last_seen_uptime_ms":3409364}],"replay":{"active":false,"source":"none"}}
$ curl -sS http://127.0.0.1:8001/api/v1/contacts || true
{"contacts":[{"id":"fpv:1","type":"FPV","source":"esp32","last_seen_ts":1772142612917,"severity":"unknown","vrx_id":1,"freq_hz":5783000000,"rssi_raw":894,"selected":1,"last_seen_uptime_ms":3409364}]}
$ curl -sS http://127.0.0.1:8001/api/v1/gps
{"timestamp_ms":1772142603256,"fix":"NO_FIX","satellites":{"in_view":0,"in_use":0},"hdop":null,"vdop":null,"pdop":null,"latitude":null,"longitude":null,"altitude_m":null,"speed_m_s":null,"heading_deg":null,"last_update_ms":1772142603256,"age_ms":null,"source":"gpsd","last_error":"gpsd_no_data"}
$ curl -sS http://127.0.0.1:8001/api/v1/network/wifi/state
{"timestamp_ms":1772142614408,"enabled":true,"connected":true,"ssid":"Airtel_Toybook","bssid":"2E\\","ip":"127.0.1.1","rssi_dbm":null,"link_quality":null,"last_update_ms":1772142614408,"last_error":null}
$ curl -sS http://127.0.0.1:8001/api/v1/network/wifi/scan || true
{"timestamp_ms":1772142614517,"networks":[{"ssid":"Airtel_Toybook","bssid":"2E\\","security":"C1\\"}],"last_error":null}
$ curl -sS http://127.0.0.1:8001/api/v1/network/bluetooth/state
{"timestamp_ms":1772142614599,"enabled":false,"scanning":false,"paired_count":0,"connected_devices":[],"last_update_ms":1772142614599,"last_error":null}
$ curl -sS http://127.0.0.1:8001/api/v1/network/bluetooth/devices
{"timestamp_ms":1772142614634,"devices":[]}
$ curl -sS -X POST http://127.0.0.1:8001/api/v1/network/wifi/disable -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
{"command":"network/wifi/disable","command_id":"795046b2-e8f6-469e-9ffc-081d2c014686","accepted":true,"detail":null,"timestamp_ms":1772142614728}
$ curl -sS -X POST http://127.0.0.1:8001/api/v1/network/bluetooth/disable -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
{"command":"network/bluetooth/disable","command_id":"da19fde4-1f92-4612-938a-16a0f91d2f4f","accepted":true,"detail":null,"timestamp_ms":1772142614753}
$ curl -sS http://127.0.0.1:8001/api/v1/antsdr
{"timestamp_ms":1772142613774,"connected":false,"uri":"ip:192.168.10.2","temperature_c":null,"last_error":"no_rf_events"}
$ curl -sS http://127.0.0.1:8001/api/v1/remote_id/status
{"last_event":{"reason":"no_odid_frames"},"last_event_type":"REMOTEID_STALE","last_timestamp_ms":1772142613195,"state":"DEGRADED","mode":"live","capture_active":true,"contacts_active":0,"last_update_ms":1772142613195,"last_error":"no_odid_frames","timestamp_ms":1772142614778}
$ curl -sS http://127.0.0.1:8001/api/v1/esp32
{"timestamp_ms":1772142613918,"connected":true,"last_seen_ms":1772142613918,"rtt_ms":null,"fw_version":null,"heartbeat":{"ok":true,"interval_ms":1001,"last_heartbeat_ms":1772142613918},"capabilities":{"buttons":false,"leds":true,"buzzer":false,"vrx":true,"video_switch":true,"config":false},"last_error":null}
```

## Step F — Confirm Gating Order (Local)
```text
$ curl -sS -i -X POST http://127.0.0.1:8001/api/v1/system/reboot -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}' | sed -n '1,30p'
HTTP/1.1 400 Bad Request
date: Thu, 26 Feb 2026 21:50:17 GMT
server: uvicorn
content-length: 29
content-type: application/json

{"detail":"confirm_required"}```

## Step G — Direct System Controller + RFScan Checks
```text
$ curl -sS http://127.0.0.1:8002/api/v1/health
{"ok":true,"timestamp_ms":1772142623519,"version":"1.0.0"}
$ curl -sS http://127.0.0.1:8002/api/v1/gps
{"timestamp_ms":1772142623528,"fix":"NO_FIX","satellites":{"in_view":0,"in_use":0},"hdop":null,"vdop":null,"pdop":null,"latitude":null,"longitude":null,"altitude_m":null,"speed_m_s":null,"heading_deg":null,"last_update_ms":1772142623528,"age_ms":null,"source":"gpsd","last_error":"gpsd_no_data"}
$ curl -sS http://127.0.0.1:8002/api/v1/network/wifi/state
{"timestamp_ms":1772142626644,"enabled":true,"connected":true,"ssid":"Airtel_Toybook","bssid":"2E\\","ip":"127.0.1.1","rssi_dbm":null,"link_quality":null,"last_update_ms":1772142626644,"last_error":null}
$ curl -sS -X POST http://127.0.0.1:8002/api/v1/network/wifi/disable -H 'Content-Type: application/json' -d '{"payload":{},"confirm":false}'
{"command":"network/wifi/disable","command_id":"f77e1130-6b7a-4cbb-a6e4-33a227fb985b","accepted":true,"detail":null,"timestamp_ms":1772142626802}
$ curl -sS http://127.0.0.1:8890/api/v1/health
{"status": "ok", "engine_running": false, "ws_backend_connected": false, "last_event_timestamp_ms": null, "timestamp_ms": 1772142626811}
$ curl -sS http://127.0.0.1:8890/api/v1/stats || true
{"timestamp_ms": 1772142626821, "frames_processed": 0, "events_emitted": 0, "last_event_timestamp_ms": 0}
$ curl -sS http://127.0.0.1:8890/api/v1/config || true
{"radio": {"uri": "ip:192.168.10.2", "sample_rate": 2000000, "rx_buffer_size": 4096}, "tracker": {"bucket_hz": 250000, "ttl_s": 120.0, "min_hits_to_confirm": 2, "update_interval_s": 1.0, "correlation_enabled": false, "correlation_window_ms": 100}, "detector": {"min_snr_db": 10.0, "lo_guard_hz": 100000.0}, "sweep": {"bands": [{"name": "5G8_RaceBand", "start_hz": 5658000000.0, "stop_hz": 5917000000.0, "step_hz": 2000000.0}, {"name": "5G8_FatShark", "start_hz": 5733000000.0, "stop_hz": 5866000000.0, "step_hz": 2000000.0}, {"name": "5G8_BandA", "start_hz": 5865000000.0, "stop_hz": 5945000000.0, "step_hz": 2000000.0}, {"name": "5G8_Digital", "start_hz": 5725000000.0, "stop_hz": 5850000000.0, "step_hz": 2000000.0}, {"name": "2G4_Control", "start_hz": 2400000000.0, "stop_hz": 2483500000.0, "step_hz": 1000000.0}, {"name": "915_Control", "start_hz": 902000000.0, "stop_hz": 928000000.0, "step_hz": 1000000.0}], "dwell_ms": 0}, "ws": {"enabled": false, "url": "", "connect_timeout_s": 5.0, "send_timeout_s": 2.0, "max_retries": 3, "retry_backoff_s": 1.0}, "classification": {"profiles": "/home/toybook/ndefender-antsdr-scan/config/classification_profiles.yaml", "hop_window_ms": 1000, "min_hop_hz": 200000.0}, "api": {"enabled": true, "bind": "127.0.0.1", "port": 8890, "api_key": "", "max_clients": 25, "event_buffer": 500}}
```

## Step H — WS + Contract Validator (Local + Public)
```text
$ python3 /home/toybook/ndefender-api-contracts/tools/validate_contract.py --local http://127.0.0.1:8001/api/v1 --ws-seconds 10
PASS

$ python3 /home/toybook/ndefender-api-contracts/tools/validate_contract.py --local http://127.0.0.1:8001/api/v1 --public https://n.flyspark.in/api/v1 --ws-seconds 10
PASS

```

## Step I — Repo State Audit
```text
== ndefender-api-contracts
origin	git@github.com:flyspark015/ndefender-api-contracts.git (fetch)
origin	git@github.com:flyspark015/ndefender-api-contracts.git (push)
## main...origin/main
05c7c7d
05c7c7d docs: add wifi/bluetooth disable endpoints
== ndefender-backend-aggregator
origin	https://github.com/flyspark015/ndefender-backend-aggregator.git (fetch)
origin	https://github.com/flyspark015/ndefender-backend-aggregator.git (push)
## main...origin/main
f5a21c7
f5a21c7 feat(network): add wifi/bluetooth disable proxies
== ndefender-system-controller
origin	git@github.com:flyspark015/ndefender-system-controller.git (fetch)
origin	git@github.com:flyspark015/ndefender-system-controller.git (push)
## main...origin/main
38e59a5
38e59a5 feat(network): add wifi/bluetooth disable endpoints
== ndefender-antsdr-scan
origin	git@github.com:flyspark015/ndefender-antsdr-scan.git (fetch)
origin	git@github.com:flyspark015/ndefender-antsdr-scan.git (push)
## main...origin/main
98a0641
98a0641 chore(config): add production api config
== Ndefender-Remoteid-Engine
origin	git@github.com:flyspark015/Ndefender-Remoteid-Engine.git (fetch)
origin	git@github.com:flyspark015/Ndefender-Remoteid-Engine.git (push)
## main...origin/main
294ca74
294ca74 feat: expand remoteid status api
== ndefender-esp32-panel
origin	git@github.com:flyspark015/ndefender-esp32-panel.git (fetch)
origin	git@github.com:flyspark015/ndefender-esp32-panel.git (push)
## main...origin/main
0d61f35
0d61f35 feat: add esp32 control stubs
```

## PASS/FAIL Table (Pre-Hardening)
- ports: PASS (8001/8002/8890 listening; 8000 exposed)
- systemd active: PASS
- REST local: PASS
- confirm gating: PASS (400 confirm_required)
- WS local: PASS (validator)
- validator local: PASS
- validator public: PASS
- legacy 8000 exposure removed: FAIL (pre-hardening)

## Step K — Legacy Flask Hardening (Port 8000)
Pre-hardening identification:
```text
$ ss -lntp | grep ':8000'
LISTEN 0      128                        0.0.0.0:8000       0.0.0.0:*    users:(("python",pid=1151,fd=11))

$ ps -fp 1151
UID          PID    PPID  C STIME TTY          TIME CMD
toybook     1151       1  3 Feb26 ?        00:52:17 /opt/ndefender/backend/venv/bin/python -u /opt/ndefender/backend/app.py
```

Executed:
- sudo systemctl stop ndefender-backend
- sudo systemctl disable ndefender-backend

Output from disable:
```text
Removed "/etc/systemd/system/multi-user.target.wants/ndefender-backend.service".
```

Post-hardening checks:
```text
$ ss -lntp | grep ':8000' || true

$ systemctl status ndefender-backend --no-pager || true
○ ndefender-backend.service - N-Defender Backend (Flask + WebSocket)
     Loaded: loaded (/etc/systemd/system/ndefender-backend.service; disabled; preset: enabled)
    Drop-In: /etc/systemd/system/ndefender-backend.service.d
             └─override.conf
     Active: inactive (dead)

Feb 27 03:21:26 ndefender-pi python[1151]: 127.0.0.1 - - [27/Feb/2026 03:21:26] "GET /api/v1/health HTTP/1.1" 200 -
Feb 27 03:21:26 ndefender-pi python[1151]: 127.0.0.1 - - [27/Feb/2026 03:21:26] "GET /api/v1/status HTTP/1.1" 200 -
Feb 27 03:21:28 ndefender-pi python[1151]: 127.0.0.1 - - [27/Feb/2026 03:21:28] "GET /api/v1/health HTTP/1.1" 200 -
Feb 27 03:21:29 ndefender-pi python[1151]: 127.0.0.1 - - [27/Feb/2026 03:21:29] "GET /api/v1/status HTTP/1.1" 200 -
Feb 27 03:21:31 ndefender-pi python[1151]: 127.0.0.1 - - [27/Feb/2026 03:21:31] "GET /api/v1/health HTTP/1.1" 200 -
Feb 27 03:21:31 ndefender-pi python[1151]: 127.0.0.1 - - [27/Feb/2026 03:21:31] "GET /api/v1/status HTTP/1.1" 200 -
Feb 27 03:21:33 ndefender-pi python[1151]: 127.0.0.1 - - [27/Feb/2026 03:21:33] "GET /api/v1/health HTTP/1.1" 200 -
Feb 27 03:21:33 ndefender-pi python[1151]: 127.0.0.1 - - [27/Feb/2026 03:21:33] "GET /api/v1/status HTTP/1.1" 200 -
Feb 27 03:21:35 ndefender-pi python[1151]: 127.0.0.1 - - [27/Feb/2026 03:21:35] "GET /api/v1/health HTTP/1.1" 200 -
Feb 27 03:21:36 ndefender-pi python[1151]: 127.0.0.1 - - [27/Feb/2026 03:21:36] "GET /api/v1/status HTTP/1.1" 200 -

$ systemctl is-enabled ndefender-backend || true
disabled

$ ss -lntp | egrep '(:8001|:8002|:8890|:8000)\b' || true
LISTEN 0      128                      127.0.0.1:8890       0.0.0.0:*    users:(("ndefender-antsd",pid=2071035,fd=6))
LISTEN 0      2048                     127.0.0.1:8001       0.0.0.0:*    users:(("uvicorn",pid=2076223,fd=7))        
LISTEN 0      2048                     127.0.0.1:8002       0.0.0.0:*    users:(("uvicorn",pid=2076239,fd=14))       
```

## Step L — Post-Hardening Contract Validator
```text
$ python3 /home/toybook/ndefender-api-contracts/tools/validate_contract.py --local http://127.0.0.1:8001/api/v1 --public https://n.flyspark.in/api/v1 --ws-seconds 10
PASS

```

## PASS/FAIL Table (Post-Hardening)
- ports: PASS (8000 removed; 8001/8002/8890 listening)
- systemd active: PASS
- REST local: PASS
- confirm gating: PASS (400 confirm_required)
- WS local: PASS (validator)
- validator local: PASS
- validator public: PASS
- legacy 8000 exposure removed: PASS
- post-hardening validator: PASS
