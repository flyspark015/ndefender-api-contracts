# EventEnvelope

Envelope:
```json
{"type":"SYSTEM_UPDATE","timestamp_ms":1700000000000,"source":"aggregator","data":{}}
```

Rules:
- `timestamp_ms` is epoch ms.
- `data` is event-specific object.

## Notes
- All WS events must use this envelope.
- `HEARTBEAT` is currently a contract gap if emitted.
