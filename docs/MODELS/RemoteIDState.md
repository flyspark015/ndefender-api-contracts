# RemoteIDState

Schema: `schemas/RemoteIDState.json`

Fields:
- `timestamp_ms`, `state`, `mode`, `capture_active`, `contacts_active?`, `last_update_ms?`, `last_error?`

Example:
```json
{"timestamp_ms":1700000000000,"state":"degraded","mode":"live","capture_active":true,"last_error":"no_odid_frames"}
```
