from __future__ import annotations

import asyncio
import time
from typing import Any


def envelope(event_type: str, data: dict[str, Any], source: str = "aggregator") -> dict[str, Any]:
    return {
        "type": event_type,
        "timestamp_ms": int(time.time() * 1000),
        "source": source,
        "data": data,
    }


async def send_hello(ws, source: str = "aggregator") -> None:
    # CONTRACT GAP: HELLO is not yet formalized in canonical contract.
    await ws.send_json(envelope("HELLO", {"timestamp_ms": int(time.time() * 1000)}, source=source))


async def send_system_update(ws, snapshot: dict[str, Any], source: str = "aggregator") -> None:
    await ws.send_json(envelope("SYSTEM_UPDATE", snapshot, source=source))


async def heartbeat_loop(ws, interval_s: float = 3.0, source: str = "aggregator") -> None:
    # CONTRACT GAP: HEARTBEAT is not yet formalized in canonical contract.
    while True:
        await ws.send_json(envelope("HEARTBEAT", {"timestamp_ms": int(time.time() * 1000)}, source=source))
        await asyncio.sleep(interval_s)
