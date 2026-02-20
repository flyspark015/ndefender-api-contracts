#!/usr/bin/env python3
import json
from pathlib import Path
import sys

import jsonschema

root = Path(__file__).resolve().parents[1]
schemas_dir = root / "schemas"

paths = sorted(schemas_dir.glob("*.json"))
if not paths:
    print("no schemas found", file=sys.stderr)
    sys.exit(1)

for path in paths:
    data = json.loads(path.read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator.check_schema(data)

print(f"schemas ok: {len(paths)}")
