# Contract Sources 📚

This file lists the authoritative source locations for the N-Defender unified API contract. Each entry maps to the repository and file paths that define the canonical behavior, payloads, and event envelopes.

## Backend Aggregator (Primary REST + WS)
- Repo: `ndefender-backend-aggregator`
- REST routes and dependencies: `src/ndefender_backend_aggregator/main.py`
- Core models: `src/ndefender_backend_aggregator/models.py`
- Contact unification rules: `src/ndefender_backend_aggregator/contacts.py`
- Command request/response contracts: `src/ndefender_backend_aggregator/commands/contracts.py`
- WebSocket envelope and system update: `src/ndefender_backend_aggregator/ws.py`
- System Controller integration mapping: `src/ndefender_backend_aggregator/integrations/system_controller.py`
- ESP32 serial ingestion and ACK events: `src/ndefender_backend_aggregator/integrations/esp32_serial.py`
- AntSDR JSONL ingestion: `src/ndefender_backend_aggregator/ingest/antsdr_ingest.py`
- RemoteID JSONL ingestion: `src/ndefender_backend_aggregator/ingest/remoteid_ingest.py`
- Rate limits (commands + dangerous): `src/ndefender_backend_aggregator/rate_limit.py`
- Auth + RBAC configs: `config/default.yaml`
- API contract overview: `docs/API.md`

## System Controller (Device Status + Power + Services)
- Repo: `ndefender-system-controller`
- REST routes: `src/ndefender_system_controller/api/routes_status.py`
- REST routes: `src/ndefender_system_controller/api/routes_system.py`
- REST routes: `src/ndefender_system_controller/api/routes_ups.py`
- REST routes: `src/ndefender_system_controller/api/routes_services.py`
- REST routes: `src/ndefender_system_controller/api/routes_network.py`
- REST routes: `src/ndefender_system_controller/api/routes_audio.py`
- WebSocket endpoint and envelope: `src/ndefender_system_controller/api/ws.py`
- Data models: `src/ndefender_system_controller/models.py`
- Auth config (API key): `src/ndefender_system_controller/config.py`
- Auth enforcement: `src/ndefender_system_controller/util/auth.py`
- Cooldown rate-limit utility: `src/ndefender_system_controller/util/rate_limit.py`
- API reference: `docs/API.md`

## ESP32 Panel (Serial Protocol + Telemetry)
- Repo: `ndefender-esp32-panel`
- Serial protocol reference: `docs/SERIAL_PROTOCOL.md`
- Firmware telemetry/ACK formatting: `esp32_firmware/src/esp32.ino`
- Example telemetry and commands: `esp32_firmware/README.md`

## AntSDR Scan (RF Events + Local API)
- Repo: `ndefender-antsdr-scan`
- RF event JSON Schema: `src/ndefender_antsdr_scan/events/schema.json`
- Event envelope helper: `src/ndefender_antsdr_scan/api/contract.py`
- JSONL emission path: `src/ndefender_antsdr_scan/io/emit.py`
- Local API server (aiohttp): `src/ndefender_antsdr_scan/api/server.py`
- API reference: `docs/api.md`

## RemoteID Engine (Contact + Telemetry + Replay Events)
- Repo: `Ndefender-Remoteid-Engine`
- RemoteID event JSON Schema: `src/ndefender_remoteid_engine/events/schema.json`
- Event constants: `src/ndefender_remoteid_engine/api/contract.py`
- JSONL emission path: `src/ndefender_remoteid_engine/io/emit.py`
- Local status HTTP server: `src/ndefender_remoteid_engine/api/http_server.py`
- Status snapshot model: `src/ndefender_remoteid_engine/api/status.py`
- Tracking fields: `src/ndefender_remoteid_engine/tracking/models.py`
- System overview: `docs/REMOTEID_SYSTEM.md`

## Observability (Health + Metrics)
- Repo: `ndefender-observability`
- REST API endpoints: `src/ndefender_observability/main.py`
- Health computation model: `src/ndefender_observability/health/model.py`
- Health computation logic: `src/ndefender_observability/health/compute.py`
- Observability state model: `src/ndefender_observability/state.py`
- Diagnostics bundle payload: `src/ndefender_observability/diagnostics.py`
- Config + auth + rate limits: `src/ndefender_observability/config.py`

