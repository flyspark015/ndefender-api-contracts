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
  "timestamp_ms": 1700000000000,
  "source": "antsdr",
  "data": {}
}
```

Notes:
- Backend Aggregator, System Controller, and AntSDR REST/WS events use `timestamp_ms`.

---

## 🔌 Reconnect + Snapshot Behavior

### Backend Aggregator
- On connect, server may send a **HELLO** (contract gap) followed by **SYSTEM_UPDATE** with the full snapshot.
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

## ❤️ Liveness Requirement
- Clients and tests expect **≥3 messages within 10 seconds**.
- Backend Aggregator should send `HELLO` + `SYSTEM_UPDATE` on connect, then periodic liveness events.
- If `HEARTBEAT` is used, it must follow the canonical WS envelope and is documented as a **CONTRACT GAP**.

---

## 🌐 Backend Aggregator WS Events (Primary)
**Endpoint:** `WS /api/v1/ws`

Auth:
- No API key enforcement in code. Deploy behind network controls or proxy if required.

### HELLO *(CONTRACT GAP)*
Optional connection acknowledgement.
```json
{"type":"HELLO","timestamp_ms":1700000000000,"source":"aggregator","data":{"timestamp_ms":1700000000000}}
```

### SYSTEM_UPDATE
Full system snapshot.
```json
{
  "type": "SYSTEM_UPDATE",
  "timestamp_ms": 1700000000000,
  "source": "aggregator",
  "data": {
    "timestamp_ms": 1700000000000,
    "system": {"status":"degraded","cpu_temp_c":36.9,"cpu_usage_percent":15.8,"ram_used_mb":1931,"ram_total_mb":16215,"disk_used_gb":70,"disk_total_gb":117,"uptime_s":4671},
    "power": {"status":"ok","pack_voltage_v":16.62,"current_a":-0.01,"soc_percent":98,"state":"IDLE"},
    "rf": {"status":"offline","last_error":"antsdr_unreachable","scan_active":false,"last_event_type":"RF_SCAN_OFFLINE","last_timestamp_ms":1700000000000,"last_event":{"reason":"antsdr_unreachable"}},
    "remote_id": {"state":"DEGRADED","mode":"live","capture_active":true,"last_error":"no_odid_frames","last_event_type":"REMOTEID_STALE","last_timestamp_ms":1700000000000,"last_event":{"reason":"no_odid_frames"}},
    "vrx": {"selected":1,"scan_state":"idle","vrx":[{"id":1,"freq_hz":5740000000,"rssi_raw":632}]},
    "fpv": {"selected":1,"scan_state":"idle","freq_hz":5740000000,"rssi_raw":632},
    "video": {"selected": 1, "status": "ok"},
    "services": [],
    "network": {"status":"ok","connected":true,"ip_v4":"192.168.1.35","ssid":"example"},
    "audio": {"status":"ok","muted":false,"volume_percent":100},
    "contacts": [],
    "replay": {"active":false,"source":"none"},
    "overall_ok": false
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
    "timestamp_ms": 1700000000000,
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
  "data": {"type":"log_event","timestamp_ms":1700000000000,"message":"boot"}
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
  "timestamp_ms": 1700000000000,
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
| `HELLO` *(CONTRACT GAP)* | Backend Aggregator | `/api/v1/ws` |
| `HEARTBEAT` *(CONTRACT GAP)* | Backend Aggregator | `/api/v1/ws` |
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

> CONTRACT GAP: `HEARTBEAT` is emitted by production WS to keep clients live but is not formalized in the core contract. See `docs/CONTRACT_GAPS.md`.
