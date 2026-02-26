# Contact

Base fields:
- `id` (string, stable)
- `type` (`REMOTE_ID|RF|FPV`)
- `source` (`remoteid|antsdr|esp32`)
- `last_seen_ts` (epoch ms)
- `last_seen_uptime_ms` (optional; uptime-based)
- `severity` (`critical|high|medium|low|unknown`)

RemoteID fields:
- `model`, `operator_id`, `lat`, `lon`, `altitude_m`, `speed_m_s`

RF fields:
- `freq_hz`, `bucket_hz`, `band`, `snr_db`, `peak_db`, `noise_floor_db`, `bandwidth_class`, `confidence`, `features.*`

FPV fields:
- `vrx_id`, `freq_hz`, `rssi_raw`, `selected`

## Notes
- `last_seen_ts` is always epoch ms for UI display.
- If uptime-based timestamps are provided by device, they are preserved in `last_seen_uptime_ms`.
- `freq_hz` is always Hertz (not MHz).

## Example
```json
{
  "id": "fpv:1",
  "type": "FPV",
  "source": "esp32",
  "last_seen_ts": 1700000000000,
  "last_seen_uptime_ms": 4686359,
  "severity": "unknown",
  "vrx_id": 1,
  "freq_hz": 5740000000,
  "rssi_raw": 632,
  "selected": 1
}
```
