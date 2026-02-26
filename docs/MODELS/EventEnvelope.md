# EventEnvelope

Schema: `schemas/EventEnvelope.json`

Fields:
- `type` string
- `timestamp_ms` integer (epoch ms)
- `source` string
- `data` object

Example:
```json
{"type":"SYSTEM_UPDATE","timestamp_ms":1700000000000,"source":"aggregator","data":{"timestamp_ms":1700000000000}}
```
