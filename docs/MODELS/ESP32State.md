# ESP32State

Schema: `schemas/ESP32State.json`

Fields:
- `timestamp_ms`, `connected`, `last_seen_ms`, `rtt_ms?`, `fw_version?`, `heartbeat`, `capabilities`, `last_error?`

Example:
```json
{"timestamp_ms":1700000000000,"connected":true,"last_seen_ms":1700000000000,"heartbeat":{"ok":true,"interval_ms":1000,"last_heartbeat_ms":1700000000000},"capabilities":{"leds":true,"vrx":true,"video_switch":true}}
```
