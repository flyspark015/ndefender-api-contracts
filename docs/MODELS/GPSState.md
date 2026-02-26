# GPSState

Schema: `schemas/GPSState.json`

Fields:
- `timestamp_ms`, `fix`, `satellites`, `latitude?`, `longitude?`, `altitude_m?`, `speed_m_s?`, `heading_deg?`, `last_update_ms`, `age_ms?`, `source`, `last_error?`

Example:
```json
{"timestamp_ms":1700000000000,"fix":"NO_FIX","satellites":{"in_view":0,"in_use":0},"last_update_ms":1700000000000,"source":"gpsd"}
```
