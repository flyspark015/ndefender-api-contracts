# WifiScanResult

Schema: `schemas/WifiScanResult.json`

Fields:
- `timestamp_ms`, `networks[]` (`ssid`,`bssid`,`security`,`signal_dbm?`,`channel?`,`frequency_mhz?`,`known?`)

Example:
```json
{"timestamp_ms":1700000000000,"networks":[{"ssid":"MyWiFi","bssid":"aa:bb:cc:dd:ee:ff","security":"wpa2","signal_dbm":-48,"channel":11,"frequency_mhz":2462,"known":true}]}
```
