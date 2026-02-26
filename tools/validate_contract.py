#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import time
from typing import Any
from urllib.request import urlopen, Request

import asyncio

try:
    import websockets  # type: ignore
except Exception as exc:  # pragma: no cover
    websockets = None  # type: ignore
    _WEBSOCKETS_ERROR = exc

REQUIRED_STATUS_KEYS = [
    "timestamp_ms",
    "system",
    "power",
    "rf",
    "remote_id",
    "vrx",
    "fpv",
    "video",
    "services",
    "network",
    "audio",
    "contacts",
    "replay",
    "overall_ok",
]

FORBIDDEN_TIMESTAMP_KEYS = {"timestamp"}
EPOCH_MS_MIN = 946684800000  # 2000-01-01


def http_get(url: str) -> dict[str, Any]:
    req = Request(url, headers={"Accept": "application/json"})
    with urlopen(req, timeout=10) as resp:
        data = resp.read().decode("utf-8")
    return json.loads(data)

def find_forbidden_timestamp_keys(obj: Any, path: str = "") -> list[str]:
    errors: list[str] = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            next_path = f"{path}.{key}" if path else key
            if key in FORBIDDEN_TIMESTAMP_KEYS:
                errors.append(f"forbidden key '{key}' at {next_path}")
            errors.extend(find_forbidden_timestamp_keys(value, next_path))
    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            next_path = f"{path}[{idx}]"
            errors.extend(find_forbidden_timestamp_keys(item, next_path))
    return errors


def find_invalid_freq_hz(obj: Any, path: str = "") -> list[str]:
    errors: list[str] = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            next_path = f"{path}.{key}" if path else key
            if key == "freq_hz" and not isinstance(value, (int, float)):
                errors.append(f"freq_hz not number at {next_path}")
            errors.extend(find_invalid_freq_hz(value, next_path))
    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            next_path = f"{path}[{idx}]"
            errors.extend(find_invalid_freq_hz(item, next_path))
    return errors


def find_invalid_timestamp_ms(obj: Any, path: str = "") -> list[str]:
    errors: list[str] = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            next_path = f"{path}.{key}" if path else key
            if key in ("timestamp_ms", "last_seen_ts") or key.endswith("_timestamp_ms"):
                if not isinstance(value, int):
                    errors.append(f"{key} not int at {next_path}")
                elif value < EPOCH_MS_MIN:
                    errors.append(f"{key} not epoch ms at {next_path}")
            errors.extend(find_invalid_timestamp_ms(value, next_path))
    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            next_path = f"{path}[{idx}]"
            errors.extend(find_invalid_timestamp_ms(item, next_path))
    return errors


def validate_health(payload: dict[str, Any]) -> list[str]:
    errors = []
    if "status" in payload:
        if not isinstance(payload.get("timestamp_ms"), int):
            errors.append("health.timestamp_ms missing or not int")
        elif payload.get("timestamp_ms") < EPOCH_MS_MIN:
            errors.append("health.timestamp_ms not epoch ms")
    if "ok" in payload:
        if not isinstance(payload.get("timestamp_ms"), int):
            errors.append("health.timestamp_ms missing or not int")
        elif payload.get("timestamp_ms") < EPOCH_MS_MIN:
            errors.append("health.timestamp_ms not epoch ms")
    errors.extend(find_forbidden_timestamp_keys(payload))
    errors.extend(find_invalid_timestamp_ms(payload))
    return errors


def validate_status(payload: dict[str, Any]) -> list[str]:
    errors = []
    for key in REQUIRED_STATUS_KEYS:
        if key not in payload:
            errors.append(f"status missing key: {key}")
    if not isinstance(payload.get("timestamp_ms"), int):
        errors.append("status.timestamp_ms not int")
    if payload.get("timestamp_ms") is not None and isinstance(payload.get("timestamp_ms"), int):
        if payload.get("timestamp_ms") < EPOCH_MS_MIN:
            errors.append("status.timestamp_ms not epoch ms")
    for key in ("system", "power", "rf", "remote_id", "vrx", "fpv", "video", "network", "audio"):
        if payload.get(key) == {}:
            errors.append(f"status.{key} is empty object")
    if "overall_ok" in payload and not isinstance(payload.get("overall_ok"), bool):
        errors.append("status.overall_ok not bool")
    if "services" in payload and not isinstance(payload.get("services"), list):
        errors.append("status.services not list")
    if "contacts" in payload and not isinstance(payload.get("contacts"), list):
        errors.append("status.contacts not list")
    errors.extend(find_forbidden_timestamp_keys(payload))
    errors.extend(find_invalid_timestamp_ms(payload))
    contacts = payload.get("contacts")
    if isinstance(contacts, list):
        for c in contacts:
            if not isinstance(c, dict):
                continue
            if not isinstance(c.get("last_seen_ts"), int):
                errors.append("contact.last_seen_ts not int")
            if "freq_hz" in c and not isinstance(c.get("freq_hz"), (int, float)):
                errors.append("contact.freq_hz not number")
    vrx = payload.get("vrx")
    if isinstance(vrx, dict):
        vrx_list = vrx.get("vrx")
        if isinstance(vrx_list, list):
            for item in vrx_list:
                if not isinstance(item, dict):
                    continue
                if "freq_hz" in item and not isinstance(item.get("freq_hz"), (int, float)):
                    errors.append("vrx.freq_hz not number")
    errors.extend(find_invalid_freq_hz(payload))
    return errors


async def ws_check(url: str, seconds: int) -> list[str]:
    errors = []
    msgs = []
    if websockets is None:
        return ["ws dependency missing: pip install websockets"]
    try:
        async with websockets.connect(url) as ws:
            start = time.time()
            while time.time() - start < seconds and len(msgs) < 10:
                try:
                    msg = await asyncio.wait_for(ws.recv(), timeout=seconds - (time.time() - start))
                except asyncio.TimeoutError:
                    break
                msgs.append(msg)
    except Exception as exc:
        return [f"ws error: {exc}"]
    if len(msgs) < 3:
        errors.append(f"ws messages < 3 (got {len(msgs)})")
    for raw in msgs:
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            errors.append("ws message is not valid JSON")
            continue
        missing = {"type", "timestamp_ms", "source", "data"} - set(payload.keys())
        if missing:
            errors.append(f"ws envelope missing fields: {sorted(missing)}")
            continue
        if "timestamp" in payload:
            errors.append("ws envelope contains forbidden 'timestamp' field")
        if not isinstance(payload.get("timestamp_ms"), int):
            errors.append("ws envelope timestamp_ms not int")
        elif payload.get("timestamp_ms") < EPOCH_MS_MIN:
            errors.append("ws envelope timestamp_ms not epoch ms")
        if not isinstance(payload.get("type"), str):
            errors.append("ws envelope type not string")
        if not isinstance(payload.get("source"), str):
            errors.append("ws envelope source not string")
        if not isinstance(payload.get("data"), dict):
            errors.append("ws envelope data not object")
        errors.extend(find_forbidden_timestamp_keys(payload))
        errors.extend(find_invalid_timestamp_ms(payload))
        errors.extend(find_invalid_freq_hz(payload))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--local", default="http://127.0.0.1:8001/api/v1")
    parser.add_argument("--public", default="https://n.flyspark.in/api/v1")
    parser.add_argument("--ws-seconds", type=int, default=10)
    args = parser.parse_args()

    errors: list[str] = []
    for base in (args.local.rstrip("/"), args.public.rstrip("/")):
        health = http_get(f"{base}/health")
        errors += [f"{base}: {e}" for e in validate_health(health)]
        status = http_get(f"{base}/status")
        errors += [f"{base}: {e}" for e in validate_status(status)]

    if args.ws_seconds > 0:
        ws_url = args.public.rstrip("/").replace("https://", "wss://") + "/ws"
        errors += [f"{ws_url}: {e}" for e in asyncio.run(ws_check(ws_url, args.ws_seconds))]

    if errors:
        for e in errors:
            print("FAIL:", e)
        return 1
    print("PASS: contract checks ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
