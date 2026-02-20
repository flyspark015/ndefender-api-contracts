# N-Defender WebSocket Events 📡

This document lists **all WebSocket event types across the system**, their canonical envelope formats, example payloads, and reconnect/snapshot behavior.

---

## ✅ Canonical Envelopes

### Backend Aggregator WS Envelope
Used by `/api/v1/ws` in the Backend Aggregator.
```json
{
  "type": "EVENT_TYPE",
  "timestamp_ms": 1700000000000,
  "source": "aggregator",
  "data": {}
}
```

### System Controller WS Envelope
Used by `/api/v1/ws` in the System Controller.
```json
{
  "type": "EVENT_TYPE",
  "timestamp_ms": 1700000000000,
  "source": "system",
  "data": {}
}
```

### AntSDR Local WS Envelope
Used by `/api/v1/events` in AntSDR Scan (local API).
```json
{
  "type": "RF_CONTACT_UPDATE",
  "timestamp": 1700000000000,
  "source": "antsdr",
  "data": {}
}
```

Notes:
- AntSDR events use `timestamp` (not `timestamp_ms`).
- Backend Aggregator and System Controller use `timestamp_ms`.

---

## 🔌 Reconnect + Snapshot Behavior

### Backend Aggregator
- On connect, server sends a **SYSTEM_UPDATE** with the full snapshot.
- Client should keep the socket alive by sending periodic messages (server reads `receive_text()`).
- On reconnect: re-fetch snapshot via `GET /api/v1/status` and then re-connect WS.

### System Controller
- On connect, server sends:
  1) `LOG_EVENT` with `{ "message": "HELLO" }`
  2) `SYSTEM_STATUS` with current system snapshot
- After that, incremental updates are sent.
- On reconnect: re-fetch `GET /api/v1/status` for full snapshot and then re-connect.

### AntSDR Scan (Local)
- No snapshot is sent on connect.
- Use `GET /api/v1/events/last?limit=N` to load a snapshot.
- Then connect to WS for live stream.

---

## 🌐 Backend Aggregator WS Events (Primary)
**Endpoint:** `WS /api/v1/ws`

Auth:
- No API key enforcement in code. Deploy behind network controls or proxy if required.

### SYSTEM_UPDATE
Full system snapshot.
```json
{
  "type": "SYSTEM_UPDATE",
  "timestamp_ms": 1700000000000,
  "source": "aggregator",
  "data": {
    "timestamp_ms": 1700000000000,
    "system": {},
    "power": {},
    "rf": {},
    "remote_id": {},
    "vrx": {},
    "video": {},
    "services": [],
    "network": {},
    "audio": {},
    "contacts": [],
    "replay": {}
  }
}
```

### COMMAND_ACK
Emitted by ESP32 serial ingest and System Controller commands.
```json
{
  "type": "COMMAND_ACK",
  "timestamp_ms": 1700000000000,
  "source": "esp32",
  "data": {"id":"123","ok":true,"err":null,"data":{"cmd":"SET_VRX_FREQ"}}
}
```

### ESP32_TELEMETRY
ESP32 telemetry passthrough.
```json
{
  "type": "ESP32_TELEMETRY",
  "timestamp_ms": 1700000000000,
  "source": "esp32",
  "data": {
    "type": "telemetry",
    "timestamp_ms": 1000,
    "sel": 1,
    "vrx": [
      {"id":1,"freq_hz":5740000000,"rssi_raw":219},
      {"id":2,"freq_hz":5800000000,"rssi_raw":140},
      {"id":3,"freq_hz":5860000000,"rssi_raw":98}
    ],
    "video": {"selected": 1},
    "led": {"r":0,"y":1,"g":0},
    "sys": {"uptime_ms": 1000, "heap": 123456}
  }
}
```

### LOG_EVENT
Subsystem log event.
```json
{
  "type": "LOG_EVENT",
  "timestamp_ms": 1700000000000,
  "source": "esp32",
  "data": {"type":"log_event","timestamp_ms":1000,"message":"boot"}
}
```

### CONTACT_NEW / CONTACT_UPDATE / CONTACT_LOST
RemoteID contact lifecycle events (from JSONL tailer).
```json
{
  "type": "CONTACT_NEW",
  "timestamp_ms": 1700000000000,
  "source": "remoteid",
  "data": {
    "id": "rid:ABC123",
    "type": "REMOTE_ID",
    "model": "DJI",
    "operator_id": "operator-1",
    "lat": 37.42,
    "lon": -122.08,
    "altitude_m": 120.5,
    "speed_m_s": 8.2,
    "last_seen_ts": 1700000000000
  }
}
```

### RF_CONTACT_NEW / RF_CONTACT_UPDATE / RF_CONTACT_LOST
AntSDR contact lifecycle events (from JSONL tailer).
```json
{
  "type": "RF_CONTACT_UPDATE",
  "timestamp_ms": 1700000000000,
  "source": "antsdr",
  "data": {
    "id": "rf:5658000000",
    "freq_hz": 5658000000,
    "bucket_hz": 5658000000,
    "band": "5G8",
    "snr_db": 34.5,
    "peak_db": 120.1,
    "noise_floor_db": 85.0,
    "bandwidth_class": "wide",
    "confidence": 0.87,
    "features": {
      "prominence_db": 30.0,
      "cluster_size": 12,
      "pattern_hint": "raceband_r1",
      "hop_hint": "none",
      "bandwidth_est_hz": 20.0,
      "burstiness": 0.1,
      "hop_rate_hz": 0.0,
      "control_score": 0.0,
      "class_path": ["Analog","Video","RaceBand","R1"],
      "classification_confidence": 0.9,
      "control_correlation": false
    }
  }
}
```

### TELEMETRY_UPDATE
RemoteID health telemetry event.
```json
{
  "type": "TELEMETRY_UPDATE",
  "timestamp_ms": 1700000000000,
  "source": "remoteid",
  "data": {"state":"ok","last_ts":1700000000000,"contacts_active":1,"mode":"live"}
}
```

### REPLAY_STATE
RemoteID replay state event.
```json
{
  "type": "REPLAY_STATE",
  "timestamp_ms": 1700000000000,
  "source": "remoteid",
  "data": {"state":"running","speed":1.0,"position":20,"total":200,"ts":1700000000000}
}
```

---

## ⚙️ System Controller WS Events
**Endpoint:** `WS /api/v1/ws`

Auth:
- No API key enforcement.

### LOG_EVENT
```json
{
  "type": "LOG_EVENT",
  "timestamp_ms": 1700000000000,
  "source": "system",
  "data": {"message": "HELLO"}
}
```

### SYSTEM_STATUS
```json
{
  "type": "SYSTEM_STATUS",
  "timestamp_ms": 1700000000000,
  "source": "system",
  "data": {"cpu_temp_c": 45.2, "cpu_usage_percent": 12.5}
}
```

### UPS_UPDATE
```json
{
  "type": "UPS_UPDATE",
  "timestamp_ms": 1700000000000,
  "source": "system",
  "data": {"soc_percent": 78, "state": "DISCHARGING"}
}
```

### SERVICE_UPDATE
```json
{
  "type": "SERVICE_UPDATE",
  "timestamp_ms": 1700000000000,
  "source": "system",
  "data": {"services":[{"name":"ndefender-system-controller","active_state":"active","sub_state":"running","restart_count":1}]}
}
```

### NETWORK_UPDATE
```json
{
  "type": "NETWORK_UPDATE",
  "timestamp_ms": 1700000000000,
  "source": "system",
  "data": {"connected": true, "ssid": "MyWiFi", "ip_v4": "192.168.1.100"}
}
```

### AUDIO_UPDATE
```json
{
  "type": "AUDIO_UPDATE",
  "timestamp_ms": 1700000000000,
  "source": "system",
  "data": {"volume_percent": 60, "muted": false}
}
```

### COMMAND_ACK
```json
{
  "type": "COMMAND_ACK",
  "timestamp_ms": 1700000000000,
  "source": "system",
  "data": {"command": "reboot", "ok": true, "reason": null}
}
```

---

## 📡 AntSDR Scan Local WS Events
**Endpoint:** `WS /api/v1/events`

Auth:
- Enforces `X-API-Key` when `api.api_key` is set.

Event types:
- `RF_CONTACT_NEW`
- `RF_CONTACT_UPDATE`
- `RF_CONTACT_LOST`

Example:
```json
{
  "type": "RF_CONTACT_NEW",
  "timestamp": 1700000000000,
  "source": "antsdr",
  "data": {
    "id": "rf:2500000000",
    "freq_hz": 2500000000,
    "bucket_hz": 2500000000,
    "band": "2G4",
    "snr_db": 34.5,
    "peak_db": 120.1,
    "noise_floor_db": 85.0,
    "bandwidth_class": "narrow",
    "confidence": 0.87,
    "features": {
      "prominence_db": 30.0,
      "cluster_size": 12,
      "pattern_hint": "unknown",
      "hop_hint": "none",
      "bandwidth_est_hz": 20.0,
      "burstiness": 0.1,
      "hop_rate_hz": 0.0,
      "control_score": 0.0,
      "class_path": ["Digital","Video","DJI"],
      "classification_confidence": 0.75,
      "control_correlation": false
    }
  }
}
```

---

## 🧾 Event Type Catalog (All Systems)

| Event Type | Source | WS Endpoint |
| --- | --- | --- |
| `SYSTEM_UPDATE` | Backend Aggregator | `/api/v1/ws` |
| `COMMAND_ACK` | Backend Aggregator | `/api/v1/ws` |
| `ESP32_TELEMETRY` | Backend Aggregator | `/api/v1/ws` |
| `LOG_EVENT` | Backend Aggregator | `/api/v1/ws` |
| `CONTACT_NEW` | Backend Aggregator | `/api/v1/ws` |
| `CONTACT_UPDATE` | Backend Aggregator | `/api/v1/ws` |
| `CONTACT_LOST` | Backend Aggregator | `/api/v1/ws` |
| `RF_CONTACT_NEW` | Backend Aggregator | `/api/v1/ws` |
| `RF_CONTACT_UPDATE` | Backend Aggregator | `/api/v1/ws` |
| `RF_CONTACT_LOST` | Backend Aggregator | `/api/v1/ws` |
| `TELEMETRY_UPDATE` | Backend Aggregator | `/api/v1/ws` |
| `REPLAY_STATE` | Backend Aggregator | `/api/v1/ws` |
| `SYSTEM_STATUS` | System Controller | `/api/v1/ws` |
| `UPS_UPDATE` | System Controller | `/api/v1/ws` |
| `SERVICE_UPDATE` | System Controller | `/api/v1/ws` |
| `NETWORK_UPDATE` | System Controller | `/api/v1/ws` |
| `AUDIO_UPDATE` | System Controller | `/api/v1/ws` |
| `LOG_EVENT` | System Controller | `/api/v1/ws` |
| `COMMAND_ACK` | System Controller | `/api/v1/ws` |
| `RF_CONTACT_NEW` | AntSDR Scan | `/api/v1/events` |
| `RF_CONTACT_UPDATE` | AntSDR Scan | `/api/v1/events` |
| `RF_CONTACT_LOST` | AntSDR Scan | `/api/v1/events` |

