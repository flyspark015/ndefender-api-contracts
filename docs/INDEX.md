# N-Defender Docs Index

This index keeps legacy file paths intact while introducing a future-proof structure. The canonical contract remains:

- `docs/ALL_IN_ONE_API.md`

## API (REST + WS)
- Canonical contract: `docs/ALL_IN_ONE_API.md`
- WebSocket event catalog: `docs/WEBSOCKET_EVENTS.md`
- OpenAPI (YAML): `docs/OPENAPI.yaml`

## Endpoints
- Aggregator: `docs/ENDPOINTS/aggregator.md`
- System Controller: `docs/ENDPOINTS/system_controller.md`
- AntSDR Scan: `docs/ENDPOINTS/antsdr_scan.md`
- RemoteID Engine: `docs/ENDPOINTS/remoteid_engine.md`
- Observability: `docs/ENDPOINTS/observability.md`
- WebSocket: `docs/ENDPOINTS/websocket.md`

## Models
- StatusSnapshot: `docs/MODELS/StatusSnapshot.md`
- Contact: `docs/MODELS/Contact.md`
- CommandResult: `docs/MODELS/CommandResult.md`
- EventEnvelope: `docs/MODELS/EventEnvelope.md`
- SystemStats: `docs/MODELS/SystemStats.md`
- GPSState: `docs/MODELS/GPSState.md`
- WifiState: `docs/MODELS/WifiState.md`
- WifiScanResult: `docs/MODELS/WifiScanResult.md`
- BluetoothState: `docs/MODELS/BluetoothState.md`
- BluetoothDeviceList: `docs/MODELS/BluetoothDeviceList.md`
- ESP32State: `docs/MODELS/ESP32State.md`
- ESP32Config: `docs/MODELS/ESP32Config.md`
- AntSDRDeviceState: `docs/MODELS/AntSDRDeviceState.md`
- AntSDRGainState: `docs/MODELS/AntSDRGainState.md`
- AntSDRSweepState: `docs/MODELS/AntSDRSweepState.md`
- AntSDRStats: `docs/MODELS/AntSDRStats.md`
- RemoteIDState: `docs/MODELS/RemoteIDState.md`
- RemoteIDStats: `docs/MODELS/RemoteIDStats.md`
- RemoteIDReplayState: `docs/MODELS/RemoteIDReplayState.md`

## Guides
- Contract gaps: `docs/CONTRACT_GAPS.md`
- Contract sources: `docs/CONTRACT_SOURCES.md`
- Unified model map: `docs/UNIFIED_MODEL_MAP.md`

## Ops / Evidence
- Quickstart: `docs/QUICKSTART.md`
- Evidence pack: `docs/EVIDENCE_POST_DEPLOY_2026-02-27.md`
- Release notes: `docs/RELEASE_NOTES_v1.0.0-api-contracts-green.md`

## New Folder Structure (Aliases)
These folders are forward-looking aliases that point to the canonical files listed above:

- `docs/api/` → API reference index
- `docs/contracts/` → schemas + OpenAPI locations
- `docs/guides/` → integration guides
- `docs/ops/` → deployment / validation
- `docs/evidence/` → evidence packs
- `packages/` → packaging-friendly mirrors (schemas, OpenAPI, examples)
