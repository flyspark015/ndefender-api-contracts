# BluetoothDeviceList

Schema: `schemas/BluetoothDeviceList.json`

Fields:
- `timestamp_ms`, `devices[]` (`addr`,`name?`,`rssi_dbm?`,`paired`,`connected`)

Example:
```json
{"timestamp_ms":1700000000000,"devices":[{"addr":"00:11:22:33:44:55","name":"Headset","paired":true,"connected":false}]}
```
