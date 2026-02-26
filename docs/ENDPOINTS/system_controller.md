# System Controller Endpoints

Base: `/api/v1`

## Read Endpoints
- `GET /health`
- `GET /status`
- `GET /system`
- `GET /ups`
- `GET /services`
- `GET /network` (summary)
- `GET /network/wifi/state`
- `GET /network/wifi/scan`
- `GET /network/bluetooth/state`
- `GET /network/bluetooth/devices`
- `GET /gps`
- `GET /audio`

## Write/Command Endpoints
All commands use `{payload,confirm}`.

- `POST /services/{name}/restart` (confirm required)
- `POST /network/wifi/enable`
- `POST /network/wifi/disable`
- `POST /network/wifi/connect`
- `POST /network/wifi/disconnect`
- `POST /network/bluetooth/enable`
- `POST /network/bluetooth/disable`
- `POST /network/bluetooth/scan/start`
- `POST /network/bluetooth/scan/stop`
- `POST /network/bluetooth/pair`
- `POST /network/bluetooth/unpair`
- `POST /gps/restart` (confirm required)
- `POST /audio/mute`
- `POST /audio/volume`
- `POST /system/reboot` (dangerous)
- `POST /system/shutdown` (dangerous)

## WebSocket
- `WS /api/v1/ws`
- Envelope: `{type,timestamp_ms,source,data}`

See `docs/ALL_IN_ONE_API.md` for full schemas and examples.
