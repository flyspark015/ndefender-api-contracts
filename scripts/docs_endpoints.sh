#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python3 - <<'PY'
import yaml
from pathlib import Path
spec = yaml.safe_load(Path("docs/OPENAPI.yaml").read_text())
paths = spec.get("paths", {})
items = []
for p, methods in paths.items():
    for m in methods:
        if m.lower() in {"get","post","put","patch","delete"}:
            items.append((m.upper(), p))
print("OpenAPI endpoints:")
for m,p in sorted(items):
    print(f"{m} {p}")
PY

echo

echo "README API index endpoints:"
awk '/API_INDEX_START/{flag=1;next}/API_INDEX_END/{flag=0}flag{print}' "$ROOT/README.md" | sed -n 's/^-[ ]\+//p'
