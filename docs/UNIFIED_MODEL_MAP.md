# Unified Model Map 🧩

This document consolidates the canonical models across the N-Defender system. It is the bridge between raw subsystem outputs (JSONL, serial telemetry) and the unified backend aggregator REST + WebSocket API.

## Source Of Truth Rules
- JSONL logs are the ground truth for AntSDR and RemoteID events.
- WebSocket is the fast path for UI updates and may be transient.
- REST snapshots are authoritative for UI state rendering.

## Envelope Models

### EventEnvelope (WebSocket)
Used by Backend Aggregator and System Controller WebSocket streams.
- `type` string. Event type name.
- `timestamp_ms` integer. Epoch ms.
- `source` string. Subsystem identifier.
- `data` object. Event payload.

Backend Aggregator envelope source
- `src/ndefender_backend_aggregator/models.py`

System Controller envelope source
- `src/ndefender_system_controller/models.py`

### JsonlEventEnvelope (AntSDR + RemoteID)
Used in JSONL emission and ingestion.
- `type` string.
- `timestamp_ms` integer. Epoch ms.
- `source` string.
- `data` object.

Notes
- Backend Aggregator normalizes JSONL inputs to `timestamp_ms`.

AntSDR schema source
- `src/ndefender_antsdr_scan/events/schema.json`

RemoteID schema source
- `src/ndefender_remoteid_engine/events/schema.json`

## Core Snapshot Models

### StatusSnapshot (Backend Aggregator REST)
Source
- `src/ndefender_backend_aggregator/models.py`

Fields
- `timestamp_ms` integer.
- `overall_ok` boolean.
- `system` object. Source: System Controller `/api/v1/status` → `system`.
- `power` object. Source: System Controller `/api/v1/status` → `ups`.
- `rf` object. Source: AntSDR JSONL tailer state (`last_event_type`, `last_event`, `last_timestamp_ms`).
- `remote_id` object. Source: RemoteID JSONL tailer state (`last_event_type`, `last_event`, `last_timestamp_ms`).
- `vrx` object. Source: ESP32 telemetry.
- `fpv` object. Source: ESP32 telemetry (mirrored selection).
- `video` object. Source: ESP32 telemetry.
- `services` array. Source: System Controller `/api/v1/status` → `services`.
- `network` object. Source: System Controller `/api/v1/status` → `network`.
- `gps` object. Source: System Controller `/api/v1/status` → `gps`.
- `esp32` object. Source: ESP32 heartbeat/telemetry.
- `antsdr` object. Source: AntSDR `/api/v1/device` and sweep state.
- `audio` object. Source: System Controller `/api/v1/status` → `audio`.
- `contacts` array. Source: ContactStore merge of RemoteID + RF + FPV contacts.
- `replay` object. Source: RemoteID replay state tracking.

### StatusSnapshot (System Controller REST)
Source
- `src/ndefender_system_controller/models.py`

Fields
- `timestamp_ms` integer.
- `system` object.
- `ups` object.
- `services` array.
- `network` object.
- `audio` object.

## Contact Model (Unified)
Contact entries are returned by Backend Aggregator `/api/v1/contacts` and embedded in `/api/v1/status`.

Base fields (all contacts)
- `id` string. Unique contact key. RF uses `rf:<freq_hz>` fallback, FPV uses `fpv:<vrx_id>` fallback.
- `type` string. One of `REMOTE_ID`, `RF`, `FPV`.
- `source` string. One of `remoteid`, `antsdr`, `esp32`.
- `last_seen_ts` integer. Epoch ms.
- `severity` string. `critical|high|medium|low|unknown`.

RemoteID contact fields
- `model` string.
- `operator_id` string.
- `lat` number. Degrees.
- `lon` number. Degrees.
- `altitude_m` number.
- `speed_m_s` number.

RF contact fields
- `freq_hz` number.
- `bucket_hz` number.
- `band` string.
- `snr_db` number.
- `peak_db` number.
- `noise_floor_db` number.
- `bandwidth_class` string.
- `confidence` number.
- `features.prominence_db` number.
- `features.cluster_size` integer.
- `features.pattern_hint` string.
- `features.hop_hint` string.
- `features.bandwidth_est_hz` number.
- `features.burstiness` number.
- `features.hop_rate_hz` number.
- `features.control_score` number.
- `features.class_path` array of string.
- `features.classification_confidence` number.
- `features.control_correlation` boolean.

FPV contact fields (ESP32)
- `vrx_id` integer.
- `freq_hz` number.
- `rssi_raw` integer.
- `selected` integer.
- `last_seen_uptime_ms` integer (optional).

Sources
- Contact merge logic: `src/ndefender_backend_aggregator/contacts.py`
- RemoteID schema: `src/ndefender_remoteid_engine/events/schema.json`
- AntSDR schema: `src/ndefender_antsdr_scan/events/schema.json`
- ESP32 telemetry: `esp32_firmware/src/esp32.ino`

## Command Models

### CommandRequest (Backend Aggregator REST)
Source
- `src/ndefender_backend_aggregator/main.py`

Fields
- `payload` object. Command-specific arguments.
- `confirm` boolean. Required for dangerous operations.

### CommandResult (Backend Aggregator REST)
Source
- `src/ndefender_backend_aggregator/commands/contracts.py`

Fields
- `command` string.
- `command_id` string.
- `accepted` boolean.
- `detail` string or null.
- `timestamp_ms` integer.

### COMMAND_ACK (WebSocket Event)
Sources
- ESP32 serial → aggregator: `src/ndefender_backend_aggregator/integrations/esp32_serial.py`
- System Controller REST → aggregator clients: `src/ndefender_system_controller/api/routes_system.py`
- System Controller services restart: `src/ndefender_system_controller/api/routes_services.py`

ESP32 ACK payload shape
- `id` string.
- `ok` boolean.
- `err` string or null.
- `data.cmd` string.

System Controller ACK payload shape
- `command` string.
- `ok` boolean.
- `reason` string or null.
- `name` string. Present on service restart.

## Telemetry + Replay Models (RemoteID)

### TELEMETRY_UPDATE
Source
- `src/ndefender_remoteid_engine/events/schema.json`

Fields
- `state` enum. `offline|ok|degraded|replay`.
- `last_ts` integer.
- `contacts_active` integer.
- `mode` enum. `live|replay`.

### REPLAY_STATE
Source
- `src/ndefender_remoteid_engine/events/schema.json`

Fields
- `state` string.
- `speed` number.
- `position` integer.
- `total` integer.
- `ts` integer.

## UPS Telemetry Model
Source
- `src/ndefender_system_controller/models.py`

Fields
- `pack_voltage_v` number.
- `current_a` number.
- `input_vbus_v` number.
- `input_power_w` number.
- `soc_percent` integer.
- `time_to_empty_s` integer.
- `time_to_full_s` integer.
- `per_cell_v` array of number.
- `state` enum. `IDLE|CHARGING|FAST_CHARGING|DISCHARGING|UNKNOWN`.

## ESP32 Serial Protocol Models

### Telemetry Message
Source
- `esp32_firmware/src/esp32.ino`
- `docs/SERIAL_PROTOCOL.md`

Fields
- `type` string. `telemetry`.
- `timestamp_ms` integer.
- `sel` integer.
- `vrx` array of objects with `id`, `freq_hz`, `rssi_raw`.
- `video.selected` integer.
- `led.r` integer.
- `led.y` integer.
- `led.g` integer.
- `sys.uptime_ms` integer.
- `sys.heap` integer.

### Command Ack Message
Source
- `esp32_firmware/src/esp32.ino`

Fields
- `type` string. `command_ack`.
- `timestamp_ms` integer.
- `id` string.
- `ok` boolean.
- `err` string or null.
- `data.cmd` string.

## Observability Models

### Health
Source
- `src/ndefender_observability/main.py`

Fields
- `status` string. `ok`.

### Health Detail
Source
- `src/ndefender_observability/health/compute.py`

Fields
- `generated_ts` integer.
- `subsystems` array of objects.
- `subsystems.subsystem` string.
- `subsystems.state` enum. `OK|DEGRADED|OFFLINE|REPLAY`.
- `subsystems.updated_ts` integer or null.
- `subsystems.last_error` string or null.
- `subsystems.last_error_ts` integer or null.
- `subsystems.last_response_ago_ms` integer or null.
- `subsystems.reasons` array of string.
- `subsystems.evidence` object.

### Status
Source
- `src/ndefender_observability/health/compute.py`

Fields
- `generated_ts` integer.
- `overall_state` enum. `OK|DEGRADED|OFFLINE|REPLAY`.
- `state_counts` object mapping state string to integer.
- `subsystems` array of objects.
- `subsystems.subsystem` string.
- `subsystems.state` enum.
- `subsystems.last_update_age_ms` integer or null.
- `subsystems.last_error_ts` integer or null.

### Version
Source
- `src/ndefender_observability/main.py`

Fields
- `version` string.
- `git_sha` string.

### Config
Source
- `src/ndefender_observability/config.py`

Fields
- Sanitized config object. `auth.api_key` is masked as `***` if set.

### Diagnostics Bundle
Source
- `src/ndefender_observability/diagnostics.py`

Fields
- `path` string.
- `size_bytes` integer.
- `created_ts` integer.
