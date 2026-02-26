# SystemStats

Schema: `schemas/SystemStats.json`

Key fields:
- `timestamp_ms`, `status`, `uptime_s`, `version`, `cpu`, `ram`, `storage`, `last_error`

Example:
```json
{"timestamp_ms":1700000000000,"status":"ok","uptime_s":1234,"version":{"app":"ndefender-system-controller","git_sha":"dev","build_ts":1700000000000},"cpu":{"temp_c":45.2,"load1":0.2},"ram":{"total_mb":4096,"used_mb":512,"free_mb":3584},"storage":{"root":{"total_gb":117,"used_gb":70,"free_gb":47}}}
```
