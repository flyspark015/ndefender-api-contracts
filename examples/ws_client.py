#!/usr/bin/env python3
import argparse
import asyncio
import json
from typing import Any

try:
    import websockets  # type: ignore
except Exception as exc:  # pragma: no cover
    raise SystemExit("Missing dependency: websockets") from exc


def validate_envelope(msg: dict[str, Any]) -> None:
    required = {"type", "timestamp_ms", "source", "data"}
    missing = required - set(msg.keys())
    if missing:
        raise ValueError(f"Missing envelope fields: {sorted(missing)}")
    if not isinstance(msg.get("type"), str):
        raise ValueError("type must be string")
    if not isinstance(msg.get("timestamp_ms"), int):
        raise ValueError("timestamp_ms must be integer")
    if not isinstance(msg.get("source"), str):
        raise ValueError("source must be string")
    if not isinstance(msg.get("data"), dict):
        raise ValueError("data must be object")


async def main() -> None:
    parser = argparse.ArgumentParser(description="N-Defender WS client")
    parser.add_argument("--url", default="ws://127.0.0.1:8001/api/v1/ws")
    args = parser.parse_args()

    async with websockets.connect(args.url) as ws:
        print(f"connected: {args.url}")
        while True:
            msg = await ws.recv()
            try:
                payload = json.loads(msg)
            except json.JSONDecodeError:
                print("invalid json:", msg)
                continue
            try:
                validate_envelope(payload)
            except Exception as exc:
                print("invalid envelope:", exc, payload)
                continue
            print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
