from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class CommandRequest:
    payload: dict[str, Any]
    confirm: bool = False


def parse_command_request(body: Any) -> CommandRequest:
    if not isinstance(body, dict):
        return CommandRequest(payload={}, confirm=False)
    payload = body.get("payload")
    if not isinstance(payload, dict):
        payload = {}
    confirm = bool(body.get("confirm", False))
    return CommandRequest(payload=payload, confirm=confirm)
