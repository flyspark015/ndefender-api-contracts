// N-Defender Unified API Contracts (TypeScript)
// This file mirrors the JSON Schemas in /schemas exactly.

export type Severity = "critical" | "high" | "medium" | "low" | "unknown";

export type JsonObject = Record<string, unknown>;

// -----------------------------
// Event Envelopes
// -----------------------------

export interface EventEnvelope<T = JsonObject> {
  type: string;
  timestamp_ms: number;
  source: string;
  data: T;
}

// -----------------------------
// Command ACK
// -----------------------------

export interface Esp32CommandAckData {
  id: string;
  ok: boolean;
  err?: string | null;
  data?: {
    cmd: string;
  };
}

export interface SystemCommandAckData {
  command: string;
  ok: boolean;
  reason?: string | null;
  name?: string;
}

export type CommandAckEvent = EventEnvelope<Esp32CommandAckData | SystemCommandAckData> & {
  type: "COMMAND_ACK";
  source: "esp32" | "system";
};

// -----------------------------
// RemoteID Events
// -----------------------------

export interface RemoteIdContactEventData {
  id: string;
  type: "REMOTE_ID";
  model?: string;
  operator_id?: string;
  lat?: number;
  lon?: number;
  altitude_m?: number;
  speed_m_s?: number;
  last_seen_ts: number;
}

export interface RemoteIdContactLostEventData {
  id: string;
  type: "REMOTE_ID";
  last_seen_ts: number;
}

export type ContactNewEvent = EventEnvelope<RemoteIdContactEventData> & {
  type: "CONTACT_NEW";
  source: "remoteid";
};

export type ContactUpdateEvent = EventEnvelope<RemoteIdContactEventData> & {
  type: "CONTACT_UPDATE";
  source: "remoteid";
};

export type ContactLostEvent = EventEnvelope<RemoteIdContactLostEventData> & {
  type: "CONTACT_LOST";
  source: "remoteid";
};

export interface TelemetryUpdateData {
  state: "offline" | "ok" | "degraded" | "replay";
  last_ts: number;
  contacts_active: number;
  mode: "live" | "replay";
}

export type TelemetryUpdateEvent = EventEnvelope<TelemetryUpdateData> & {
  type: "TELEMETRY_UPDATE";
  source: "remoteid";
};

export interface ReplayStateData {
  state: string;
  speed: number;
  position?: number;
  total?: number;
  ts?: number;
}

export type ReplayStateEvent = EventEnvelope<ReplayStateData> & {
  type: "REPLAY_STATE";
  source: "remoteid";
};

// -----------------------------
// Contact Models (Unified)
// -----------------------------

export interface ContactBase {
  id: string;
  type: string;
  source: string;
  last_seen_ts: number;
  severity: Severity;
}

export interface RemoteIdContact extends ContactBase {
  type: "REMOTE_ID";
  source: "remoteid";
  model?: string;
  operator_id?: string;
  lat?: number;
  lon?: number;
  altitude_m?: number;
  speed_m_s?: number;
}

export interface RfFeatures {
  prominence_db: number;
  cluster_size: number;
  pattern_hint: string;
  hop_hint: string;
  bandwidth_est_hz: number;
  burstiness: number;
  hop_rate_hz: number;
  control_score: number;
  class_path: string[];
  classification_confidence: number;
  control_correlation: boolean;
}

export interface RfContact extends ContactBase {
  type: "RF";
  source: "antsdr";
  freq_hz: number;
  bucket_hz: number;
  band: string;
  snr_db: number;
  peak_db: number;
  noise_floor_db: number;
  bandwidth_class: string;
  confidence: number;
  features: RfFeatures;
}

export interface FpvContact extends ContactBase {
  type: "FPV";
  source: "esp32";
  vrx_id: number;
  freq_hz: number;
  rssi_raw: number;
  selected: number;
  last_seen_uptime_ms?: number;
}

export type Contact = RemoteIdContact | RfContact | FpvContact;

// -----------------------------
// UPS Telemetry
// -----------------------------

export interface UpsTelemetry {
  timestamp_ms?: number;
  status?: "ok" | "degraded" | "offline";
  pack_voltage_v?: number;
  current_a?: number;
  input_vbus_v?: number;
  input_power_w?: number;
  soc_percent?: number;
  time_to_empty_s?: number;
  time_to_full_s?: number;
  per_cell_v?: number[];
  state?: "IDLE" | "CHARGING" | "FAST_CHARGING" | "DISCHARGING" | "UNKNOWN";
  last_error?: string;
}

// -----------------------------
// Status Snapshot (Aggregator)
// -----------------------------

export interface SystemStats {
  timestamp_ms?: number;
  status?: "ok" | "degraded" | "offline";
  uptime_s?: number;
  version?: {
    app?: string;
    git_sha?: string;
    build_ts?: number;
  };
  cpu?: {
    temp_c?: number;
    load1?: number;
    load5?: number;
    load15?: number;
    usage_percent?: number;
  };
  ram?: {
    total_mb?: number;
    used_mb?: number;
    free_mb?: number;
  };
  storage?: {
    root?: { total_gb?: number; used_gb?: number; free_gb?: number };
    logs?: { total_gb?: number; used_gb?: number; free_gb?: number };
  };
  last_error?: string;
  cpu_temp_c?: number;
  cpu_usage_percent?: number;
  load_1m?: number;
  load_5m?: number;
  load_15m?: number;
  ram_used_mb?: number;
  ram_total_mb?: number;
  disk_used_gb?: number;
  disk_total_gb?: number;
  throttled_flags?: number;
}

export interface ServiceStatus {
  name: string;
  active_state: string;
  sub_state: string;
  restart_count: number;
  uptime_s?: number;
  last_restart_ms?: number;
  last_error?: string;
}

export interface NetworkStatus {
  connected?: boolean;
  ssid?: string;
  ip_v4?: string;
  ip_v6?: string;
  wifi?: WifiState;
  bluetooth?: BluetoothState;
}

export interface AudioStatus {
  timestamp_ms?: number;
  status?: "ok" | "degraded" | "offline";
  volume_percent?: number;
  muted?: boolean;
  last_error?: string;
}

export interface WifiState {
  timestamp_ms?: number;
  enabled?: boolean;
  connected?: boolean;
  ssid?: string;
  bssid?: string;
  ip?: string;
  rssi_dbm?: number;
  link_quality?: number;
  last_update_ms?: number;
  last_error?: string;
}

export interface WifiScanResult {
  timestamp_ms?: number;
  networks?: Array<{
    ssid?: string;
    bssid?: string;
    security?: string;
    signal_dbm?: number;
    channel?: number;
    frequency_mhz?: number;
    known?: boolean;
  }>;
}

export interface BluetoothState {
  timestamp_ms?: number;
  enabled?: boolean;
  scanning?: boolean;
  paired_count?: number;
  connected_devices?: Array<{ addr: string; name?: string; rssi_dbm?: number }>;
  last_update_ms?: number;
  last_error?: string;
}

export interface BluetoothDeviceList {
  timestamp_ms?: number;
  devices?: Array<{ addr: string; name?: string; rssi_dbm?: number; paired?: boolean; connected?: boolean }>;
}

export interface GPSState {
  timestamp_ms?: number;
  fix?: "NO_FIX" | "FIX_2D" | "FIX_3D";
  satellites?: { in_view?: number; in_use?: number };
  hdop?: number;
  vdop?: number;
  pdop?: number;
  latitude?: number;
  longitude?: number;
  altitude_m?: number;
  speed_m_s?: number;
  heading_deg?: number;
  last_update_ms?: number;
  age_ms?: number;
  source?: string;
  last_error?: string;
}

export interface ESP32State {
  timestamp_ms?: number;
  connected?: boolean;
  last_seen_ms?: number;
  rtt_ms?: number;
  fw_version?: string;
  heartbeat?: { ok?: boolean; interval_ms?: number; last_heartbeat_ms?: number };
  capabilities?: {
    buttons?: boolean;
    leds?: boolean;
    buzzer?: boolean;
    vrx?: boolean;
    video_switch?: boolean;
    config?: boolean;
  };
  last_error?: string;
}

export interface ESP32Config {
  timestamp_ms: number;
  schema_version?: string;
  config: JsonObject;
}

export interface AntSDRDeviceState {
  timestamp_ms?: number;
  connected?: boolean;
  uri?: string;
  temperature_c?: number;
  last_error?: string;
}

export interface AntSDRSweepState {
  timestamp_ms?: number;
  running?: boolean;
  active_plan?: string;
  plans?: Array<{ name: string; start_hz: number; end_hz: number; step_hz: number }>;
  last_update_ms?: number;
  last_error?: string;
}

export interface AntSDRGainState {
  timestamp_ms?: number;
  mode?: "manual" | "auto";
  gain_db?: number;
  limits?: { min_db?: number; max_db?: number };
}

export interface AntSDRStats {
  timestamp_ms?: number;
  frames_processed?: number;
  events_emitted?: number;
  last_event_timestamp_ms?: number;
  noise_floor_db?: number;
  peaks?: number;
  last_error?: string;
}

export interface RemoteIDState {
  timestamp_ms?: number;
  state?: "ok" | "degraded" | "offline" | "replay";
  mode?: "live" | "replay" | "off";
  capture_active?: boolean;
  contacts_active?: number;
  last_update_ms?: number;
  last_error?: string;
}

export interface RemoteIDStats {
  timestamp_ms?: number;
  frames?: number;
  decoded?: number;
  dropped?: number;
  dedupe_hits?: number;
  last_error?: string;
}

export interface RemoteIDReplayState {
  timestamp_ms?: number;
  active?: boolean;
  source?: string;
  state?: string;
  speed?: number;
  position?: number;
  total?: number;
}

export interface IngestState {
  status?: "ok" | "degraded" | "offline" | "unknown";
  scan_active?: boolean;
  capture_active?: boolean;
  mode?: "live" | "replay" | "off";
  contacts_active?: number;
  last_update_ms?: number;
  last_error?: string;
  last_event_type?: string;
  last_event?: JsonObject;
  last_timestamp_ms?: number;
}

export interface VrxItem {
  id: number;
  freq_hz: number;
  rssi_raw: number;
}

export interface LedState {
  r?: number;
  y?: number;
  g?: number;
}

export interface VrxSys {
  uptime_ms?: number;
  heap?: number;
  status?: string;
  last_error?: string;
}

export interface VrxState {
  selected?: number;
  scan_state?: string;
  vrx?: VrxItem[];
  led?: LedState;
  sys?: VrxSys;
}

export interface FpvState {
  selected?: number;
  scan_state?: string;
  freq_hz?: number;
  rssi_raw?: number;
  locked_channels?: number[];
}

export interface VideoState {
  selected?: number;
  status?: "ok" | "offline" | "unknown";
}

export interface ReplayStateSnapshot {
  active?: boolean;
  source?: string;
}

export interface StatusSnapshot {
  timestamp_ms: number;
  overall_ok?: boolean;
  system?: SystemStats;
  power?: UpsTelemetry;
  rf?: IngestState;
  remote_id?: IngestState;
  vrx?: VrxState;
  fpv?: FpvState;
  video?: VideoState;
  services?: ServiceStatus[];
  network?: NetworkStatus;
  gps?: GPSState;
  esp32?: ESP32State;
  antsdr?: AntSDRDeviceState;
  audio?: AudioStatus;
  contacts?: Contact[];
  replay?: ReplayStateSnapshot;
}
