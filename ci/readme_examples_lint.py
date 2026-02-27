#!/usr/bin/env python3
from pathlib import Path
import sys
import re

readme = Path("README.md").read_text(encoding="utf-8")

required_sections = [
    "## WebSocket (RX Events)",
    "## Confirm‑Gating Lifecycle (Dangerous Commands)",
    "## API Index",
]

missing = [s for s in required_sections if s not in readme]
if missing:
    print("Missing required sections:")
    for s in missing:
        print(f"  - {s}")
    sys.exit(1)

# WS envelope check
if "{\"type\":\"EVENT_TYPE\",\"timestamp_ms\":" not in readme:
    print("Missing WS envelope example")
    sys.exit(1)

# Ensure at least one curl example exists per endpoint group
groups = [
    "### Backend Aggregator API",
    "### System Controller API",
    "### RFScan (AntSDR Scan) API",
    "### RemoteID Engine API",
    "### Observability API",
]

for i, g in enumerate(groups):
    start = readme.find(g)
    if start == -1:
        print(f"Missing endpoint group: {g}")
        sys.exit(1)
    end = len(readme)
    for g2 in groups[i+1:]:
        pos = readme.find(g2, start + 1)
        if pos != -1:
            end = min(end, pos)
    block = readme[start:end]
    if "Curl:" not in block:
        print(f"Missing curl example in group: {g}")
        sys.exit(1)

print("README examples lint ok")
