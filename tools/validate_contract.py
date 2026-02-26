#!/usr/bin/env python3
from __future__ import annotations

import argparse
import asyncio
import json
import sys
import time
import urllib.request
from typing import Any, Dict, List, Tuple

try:
    import websockets  # type: ignore
except Exception:  # pragma: no cover
    websockets = None


def fetch_json(url: str) -> Tuple[int, Dict[str, Any]]:
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = resp.read().decode("utf-8")
            return resp.getcode(), json.loads(body) if body else {}
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8")
        try:
            return exc.code, json.loads(body) if body else {}
        except json.JSONDecodeError:
            return exc.code, {}


def post_json(url: str, payload: dict) -> Tuple[int, Dict[str, Any]]:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = resp.read().decode("utf-8")
            return resp.getcode(), json.loads(body) if body else {}
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8")
        try:
            return exc.code, json.loads(body) if body else {}
        except json.JSONDecodeError:
            return exc.code, {}


def find_plain_timestamp(obj: Any, path: str = "") -> List[str]:
    found: List[str] = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "timestamp":
                found.append(f"{path}/timestamp")
            found.extend(find_plain_timestamp(v, f"{path}/{k}"))
    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            found.extend(find_plain_timestamp(item, f"{path}[{idx}]"))
    return found


def is_epoch_ms(value: Any) -> bool:
    try:
        v = int(value)
    except (TypeError, ValueError):
        return False
    return v >= 1_000_000_000_00


def check_required_status_fields(status: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    if "timestamp_ms" not in status:
        errors.append("/status missing timestamp_ms")
    for key in ["system", "power", "rf", "remote_id", "vrx", "video", "services", "network", "audio", "contacts", "replay"]:
        if key in status and status[key] == {}:
            errors.append(f"/status {key} is empty object")
    return errors


async def ws_check(ws_url: str, seconds: int) -> Tuple[bool, int, str]:
    if websockets is None:
        return False, 0, "websockets_not_installed"
    msgs = 0
    first_type = ""
    start = time.time()
    async with websockets.connect(ws_url, ping_interval=None) as ws:
        while time.time() - start < seconds:
            try:
                raw = await asyncio.wait_for(ws.recv(), timeout=seconds)
            except asyncio.TimeoutError:
                break
            msgs += 1
            try:
                payload = json.loads(raw)
                if not first_type:
                    first_type = str(payload.get("type"))
                if set(payload.keys()) >= {"type", "timestamp_ms", "source", "data"}:
                    if not is_epoch_ms(payload.get("timestamp_ms")):
                        return False, msgs, "timestamp_ms_not_epoch"
                else:
                    return False, msgs, "missing_envelope_keys"
            except json.JSONDecodeError:
                return False, msgs, "invalid_json"
            if msgs >= 3:
                break
    return msgs >= 3, msgs, first_type


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--local", required=True)
    parser.add_argument("--public")
    parser.add_argument("--ws-seconds", type=int, default=10)
    parser.add_argument("--skip-commands", action="store_true")
    args = parser.parse_args()

    bases = [("local", args.local)]
    if args.public:
        bases.append(("public", args.public))

    failures: List[str] = []

    for label, base in bases:
        code, health = fetch_json(f"{base}/health")
        if code != 200:
            failures.append(f"{label} /health status {code}")
        if "timestamp_ms" not in health:
            failures.append(f"{label} /health missing timestamp_ms")
        if find_plain_timestamp(health):
            failures.append(f"{label} /health contains timestamp")

        code, status = fetch_json(f"{base}/status")
        if code != 200:
            failures.append(f"{label} /status status {code}")
        failures.extend([f"{label} {e}" for e in check_required_status_fields(status)])
        if find_plain_timestamp(status):
            failures.append(f"{label} /status contains timestamp")

        # Optional subsystem endpoints should still exist and return timestamp_ms
        for path in [
            "/network/wifi/state",
            "/network/wifi/scan",
            "/network/bluetooth/state",
            "/network/bluetooth/devices",
            "/gps",
            "/esp32",
            "/antsdr",
            "/remote_id",
        ]:
            code, body = fetch_json(f"{base}{path}")
            if code != 200:
                failures.append(f"{label} {path} status {code}")
                continue
            if "timestamp_ms" not in body:
                failures.append(f"{label} {path} missing timestamp_ms")
            if find_plain_timestamp(body):
                failures.append(f"{label} {path} contains timestamp")

        if not args.skip_commands:
            # confirm-required check
            code, body = post_json(f"{base}/system/reboot", {"payload": {}, "confirm": False})
            if code != 400:
                failures.append(f"{label} /system/reboot confirm_required expected 400, got {code}")

        # WS check
        ws_url = base.replace("http://", "ws://").replace("https://", "wss://") + "/ws"
        ok, msgs, first_type = asyncio.get_event_loop().run_until_complete(ws_check(ws_url, args.ws_seconds))
        if not ok:
            failures.append(f"{label} WS msgs_received={msgs} first_type={first_type}")

    if failures:
        print("FAIL")
        for item in failures:
            print("-", item)
        return 1

    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
