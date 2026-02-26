# StatusSnapshot

Schema: `schemas/StatusSnapshot.json`

Top-level fields:
- `timestamp_ms` (required)
- `overall_ok`
- `system`, `power`, `rf`, `remote_id`, `vrx`, `fpv`, `video`
- `services`, `network`, `gps`, `esp32`, `antsdr`, `audio`
- `contacts`, `replay`

Example:
```json
{"timestamp_ms":1700000000000,"overall_ok":false,"system":{"status":"ok","uptime_s":1234},"power":{"status":"ok","soc_percent":78},"rf":{"status":"offline","last_error":"antsdr_unreachable"},"remote_id":{"state":"degraded","mode":"live","capture_active":true,"last_error":"no_odid_frames"},"vrx":{"selected":1,"vrx":[]},"fpv":{"selected":1,"scan_state":"idle"},"video":{"selected":1,"status":"ok"},"services":[],"network":{"wifi":{"timestamp_ms":1700000000000,"enabled":true,"connected":true,"ssid":"MyWiFi"}},"gps":{"timestamp_ms":1700000000000,"fix":"NO_FIX","satellites":{"in_view":0,"in_use":0},"last_update_ms":1700000000000,"source":"gpsd"},"esp32":{"timestamp_ms":1700000000000,"connected":true,"last_seen_ms":1700000000000},"antsdr":{"timestamp_ms":1700000000000,"connected":false,"last_error":"antsdr_unreachable"},"audio":{"timestamp_ms":1700000000000,"status":"ok","volume_percent":60,"muted":false},"contacts":[],"replay":{"active":false,"source":"none"}}
```
