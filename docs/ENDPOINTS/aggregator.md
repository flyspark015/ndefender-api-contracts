# Backend Aggregator Endpoints

This is the primary public API. Canonical contract: `docs/ALL_IN_ONE_API.md`.

Base: `/api/v1`

## Read Endpoints
- `GET /health`
- `GET /status`
- `GET /contacts`
- `GET /system`
- `GET /power`
- `GET /rf`
- `GET /video`
- `GET /services`
- `GET /network` (summary)
- `GET /network/wifi/state`
- `GET /network/wifi/scan`
- `GET /network/bluetooth/state`
- `GET /network/bluetooth/devices`
- `GET /audio`
- `GET /gps`
- `GET /esp32`
- `GET /esp32/config`
- `GET /antsdr`
- `GET /antsdr/sweep/state`
- `GET /antsdr/gain`
- `GET /antsdr/stats`
- `GET /remote_id`
- `GET /remote_id/contacts`
- `GET /remote_id/stats`

## Write/Command Endpoints
All commands use:
```json
{"payload":{...},"confirm":false}
```

- `POST /vrx/tune`
- `POST /scan/start`
- `POST /scan/stop`
- `POST /video/select`
- `POST /audio/mute`
- `POST /audio/volume`
- `POST /network/wifi/enable`
- `POST /network/wifi/connect`
- `POST /network/wifi/disconnect`
- `POST /network/bluetooth/enable`
- `POST /network/bluetooth/scan/start`
- `POST /network/bluetooth/scan/stop`
- `POST /network/bluetooth/pair`
- `POST /network/bluetooth/unpair`
- `POST /gps/restart` (confirm required)
- `POST /esp32/buzzer`
- `POST /esp32/leds`
- `POST /esp32/buttons/simulate` (local-only)
- `POST /esp32/config`
- `POST /antsdr/sweep/start`
- `POST /antsdr/sweep/stop`
- `POST /antsdr/gain/set`
- `POST /antsdr/device/reset` (dangerous)
- `POST /remote_id/monitor/start`
- `POST /remote_id/monitor/stop`
- `POST /system/reboot` (dangerous)
- `POST /system/shutdown` (dangerous)

## WebSocket
- `WS /api/v1/ws`
- Envelope: `{type,timestamp_ms,source,data}`
- Must send >=3 messages / 10s (SYSTEM_UPDATE + HEARTBEAT).

See `docs/ALL_IN_ONE_API.md` for full schemas and examples.
