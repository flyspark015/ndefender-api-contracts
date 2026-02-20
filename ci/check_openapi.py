#!/usr/bin/env python3
from pathlib import Path
import sys
import yaml

try:
    from openapi_spec_validator import validate_spec
except Exception as exc:
    print(f"openapi-spec-validator unavailable: {exc}")
    sys.exit(1)

root = Path(__file__).resolve().parents[1]
path = root / "docs" / "OPENAPI.yaml"

spec = yaml.safe_load(path.read_text(encoding="utf-8"))

schemas_dir = root / "schemas"


def _normalize_ref(ref: str) -> str:
    if ref.startswith("../schemas/"):
        target = schemas_dir / ref.replace("../schemas/", "")
        return target.resolve().as_uri()
    if ref.startswith("file:../schemas/"):
        target = schemas_dir / ref.replace("file:../schemas/", "")
        return target.resolve().as_uri()
    return ref


def _walk(obj):
    if isinstance(obj, dict):
        for key, value in list(obj.items()):
            if key == "$ref" and isinstance(value, str):
                obj[key] = _normalize_ref(value)
            else:
                _walk(value)
    elif isinstance(obj, list):
        for item in obj:
            _walk(item)


_walk(spec)
validate_spec(spec, spec_url=path.as_uri())
print("openapi ok")
