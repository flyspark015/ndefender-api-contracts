# StatusSnapshot

Required:
- `timestamp_ms` (epoch ms)

Optional sections (may be omitted in minimal deployments, but should be present for UI stability):
- `system`, `power`, `rf`, `remote_id`, `vrx`, `fpv`, `video`
- `services`, `network`, `audio`, `contacts`, `replay`
- `overall_ok`

## Validation Rules
- No empty `{}` for major sections in production UI.
- All timestamps are epoch ms.
- Frequencies use `freq_hz` in Hz.

## Enums (Common)
- `status`: `ok|degraded|offline|unknown`
- `remote_id.state`: `ok|degraded|offline|replay`
- `replay.active`: boolean

## Notes
- `rf.status` + `rf.last_error` indicate offline/degraded reason.
- `remote_id.capture_active` indicates capture running even if no decodes.
- Some implementations also include `remote_id.last_ts` (ms) from the RemoteID engine; prefer `last_timestamp_ms` when present.
- `vrx.scan_state` and `vrx.sys.status` may be present when ESP32 telemetry is connected.
- `video.status` is inferred by device presence.

## Example
```json
{
  "timestamp_ms": 1700000000000,
  "system": {"status":"degraded","cpu_temp_c":36.9,"cpu_usage_percent":15.8,"ram_used_mb":1931,"ram_total_mb":16215,"disk_used_gb":70,"disk_total_gb":117,"uptime_s":4671},
  "power": {"status":"ok","pack_voltage_v":16.62,"current_a":-0.01,"soc_percent":98,"state":"IDLE"},
  "rf": {"status":"offline","last_error":"antsdr_unreachable","scan_active":false,"last_event_type":"RF_SCAN_OFFLINE","last_timestamp_ms":1700000000000,"last_event":{"reason":"antsdr_unreachable"}},
  "remote_id": {"state":"DEGRADED","mode":"live","capture_active":true,"last_error":"no_odid_frames","last_event_type":"REMOTEID_STALE","last_timestamp_ms":1700000000000,"last_event":{"reason":"no_odid_frames"}},
  "vrx": {"selected":1,"scan_state":"idle","vrx":[{"id":1,"freq_hz":5740000000,"rssi_raw":632}]},
  "fpv": {"selected":1,"scan_state":"idle","freq_hz":5740000000,"rssi_raw":632},
  "video": {"selected":1,"status":"ok"},
  "services": [{"name":"ndefender-backend","active_state":"active","sub_state":"running","restart_count":0}],
  "network": {"status":"ok","connected":true,"ip_v4":"192.168.1.35","ssid":"example"},
  "audio": {"status":"ok","muted":false,"volume_percent":100},
  "contacts": [],
  "replay": {"active":false,"source":"none"},
  "overall_ok": false
}
```
