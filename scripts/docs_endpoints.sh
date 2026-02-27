#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python3 - <<'PY'
import yaml
from pathlib import Path
from urllib.parse import urlparse

spec = yaml.safe_load(Path("docs/OPENAPI.yaml").read_text())
paths = spec.get("paths", {})
servers = spec.get("servers", []) or []
server_paths = []
for s in servers:
    url = s.get("url", "")
    if not url:
        continue
    p = urlparse(url).path.rstrip("/")
    if p:
        server_paths.append(p)
canonical_base = next((p for p in server_paths if p.endswith("/api/v1")), "") or "/api/v1"

raw = []
canon = []
for p, methods in paths.items():
    for m in methods:
        if m.lower() in {"get","post","put","patch","delete"}:
            raw.append((m.upper(), p))
            path = p if p.startswith("/") else f"/{p}"
            canon.append((m.upper(), f"{canonical_base}{path}"))

print("OpenAPI endpoints (RAW):")
for m,p in sorted(raw):
    print(f"{m} {p}")
print()
print(f"OpenAPI endpoints (CANONICAL, base {canonical_base}):")
for m,p in sorted(canon):
    print(f"{m} {p}")
PY

echo
echo "README API index endpoints (CANONICAL):"
awk '/API_INDEX_START/{flag=1;next}/API_INDEX_END/{flag=0}flag{print}' "$ROOT/README.md" | sed -n 's/^-[ ]\+//p'
