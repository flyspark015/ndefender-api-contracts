#!/usr/bin/env python3
from pathlib import Path
import sys
import re
from urllib.parse import urlparse
import yaml

root = Path(__file__).resolve().parents[1]
openapi_path = root / "docs" / "OPENAPI.yaml"
readme_path = root / "README.md"

spec = yaml.safe_load(openapi_path.read_text(encoding="utf-8"))
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

canonical_base = next((p for p in server_paths if p.endswith("/api/v1")), "")
if not canonical_base:
    canonical_base = "/api/v1"

openapi_endpoints = set()
for path, methods in paths.items():
    for method in methods:
        m = method.lower()
        if m in {"get", "post", "put", "patch", "delete"}:
            if not path.startswith("/"):
                path = f"/{path}"
            full_path = f"{canonical_base}{path}"
            openapi_endpoints.add(f"{m.upper()} {full_path}")

readme = readme_path.read_text(encoding="utf-8")
start = readme.find("<!-- API_INDEX_START -->")
end = readme.find("<!-- API_INDEX_END -->")
if start == -1 or end == -1 or end <= start:
    print("README API index markers missing")
    sys.exit(1)

index_block = readme[start:end]
lines = [ln.strip() for ln in index_block.splitlines()]
pattern = re.compile(r"^-\s+(GET|POST|PUT|PATCH|DELETE)\s+(/\S+)$")
readme_endpoints = set()
for ln in lines:
    m = pattern.match(ln)
    if not m:
        continue
    method = m.group(1)
    path = m.group(2)
    readme_endpoints.add(f"{method} {path}")

missing_in_readme = sorted(openapi_endpoints - readme_endpoints)
extra_in_readme = sorted(readme_endpoints - openapi_endpoints)

if missing_in_readme or extra_in_readme:
    if missing_in_readme:
        print(f"Missing in README (present in OpenAPI, canonical base {canonical_base}):")
        for item in missing_in_readme:
            print(f"  - {item}")
    if extra_in_readme:
        print(f"Extra in README (not in OpenAPI, canonical base {canonical_base}):")
        for item in extra_in_readme:
            print(f"  - {item}")
    sys.exit(1)

print(f"README endpoint index matches OpenAPI paths (canonical base {canonical_base})")
