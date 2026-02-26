# AntSDRSweepState

Schema: `schemas/AntSDRSweepState.json`

Fields:
- `timestamp_ms`, `running`, `active_plan?`, `plans[]`, `last_update_ms`, `last_error?`

Example:
```json
{"timestamp_ms":1700000000000,"running":false,"plans":[{"name":"analog_5g8","start_hz":5645000000,"end_hz":5865000000,"step_hz":2000000}],"last_update_ms":1700000000000}
```
