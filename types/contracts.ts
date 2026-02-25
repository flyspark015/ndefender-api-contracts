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
  last_seen_uptime_ms?: number;
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
}

export type Contact = RemoteIdContact | RfContact | FpvContact;

// -----------------------------
// UPS Telemetry
// -----------------------------

export interface UpsTelemetry {
  pack_voltage_v?: number;
  current_a?: number;
  input_vbus_v?: number;
  input_power_w?: number;
  soc_percent?: number;
  time_to_empty_s?: number;
  time_to_full_s?: number;
  per_cell_v?: number[];
  state?: "IDLE" | "CHARGING" | "FAST_CHARGING" | "DISCHARGING" | "UNKNOWN";
  status?: string;
}

// -----------------------------
// Status Snapshot (Aggregator)
// -----------------------------

export interface SystemStats {
  uptime_s?: number;
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
  status?: string;
}

export interface ServiceStatus {
  name: string;
  active_state: string;
  sub_state: string;
  restart_count: number;
}

export interface NetworkStatus {
  connected?: boolean;
  ssid?: string;
  ip_v4?: string;
  ip_v6?: string;
  status?: string;
}

export interface AudioStatus {
  volume_percent?: number;
  muted?: boolean;
  status?: string;
}

export interface RfState {
  last_event_type?: string;
  last_event?: JsonObject;
  last_timestamp_ms?: number;
  scan_active?: boolean;
  status?: string;
  last_error?: string;
}

export interface RemoteIdState {
  last_event_type?: string;
  last_event?: JsonObject;
  last_timestamp_ms?: number;
  state?: string;
  mode?: string;
  capture_active?: boolean;
  last_error?: string;
  last_ts?: number;
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
}

export interface VrxState {
  selected?: number;
  vrx?: VrxItem[];
  led?: LedState;
  sys?: VrxSys;
}

export interface FpvState {
  selected?: number;
  locked_channels?: number[];
  rssi_raw?: number;
  scan_state?: string;
  freq_hz?: number;
}

export interface VideoState {
  selected?: number;
  status?: string;
}

export interface ReplayStateSnapshot {
  active?: boolean;
  source?: string;
}

export interface StatusSnapshot {
  timestamp_ms: number;
  system?: SystemStats;
  power?: UpsTelemetry;
  rf?: RfState;
  remote_id?: RemoteIdState;
  vrx?: VrxState;
  fpv?: FpvState;
  video?: VideoState;
  services?: ServiceStatus[];
  network?: NetworkStatus;
  audio?: AudioStatus;
  contacts?: Contact[];
  replay?: ReplayStateSnapshot;
  overall_ok?: boolean;
}
