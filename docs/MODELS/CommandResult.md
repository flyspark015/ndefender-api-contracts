# CommandResult

Fields:
- `command` string
- `command_id` string
- `accepted` boolean
- `detail` string|null
- `timestamp_ms` epoch ms

Validation:
- `timestamp_ms` must be epoch ms.

Example:
```json
{"command":"scan/stop","command_id":"uuid","accepted":true,"detail":null,"timestamp_ms":1700000000000}
```
