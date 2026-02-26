# Contact

Schema: `schemas/Contact.json`

Base fields:
- `id`, `type`, `source`, `last_seen_ts`, `severity`

RemoteID fields:
- `model`, `operator_id`, `lat`, `lon`, `altitude_m`, `speed_m_s`

RF fields:
- `freq_hz`, `bucket_hz`, `band`, `snr_db`, `peak_db`, `noise_floor_db`, `bandwidth_class`, `confidence`, `features`

FPV fields:
- `vrx_id`, `freq_hz`, `rssi_raw`, `selected`, `last_seen_uptime_ms?`

Example:
```json
{"id":"fpv:1","type":"FPV","source":"esp32","last_seen_ts":1700000000000,"severity":"unknown","vrx_id":1,"freq_hz":5740000000,"rssi_raw":632,"selected":1,"last_seen_uptime_ms":4686359}
```
