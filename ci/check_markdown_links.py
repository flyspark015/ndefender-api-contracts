#!/usr/bin/env python3
import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]

md_files = list(root.rglob("*.md"))
if not md_files:
    print("no markdown files found", file=sys.stderr)
    sys.exit(1)

link_re = re.compile(r"\[[^\]]*\]\(([^)]+)\)")

missing = []
for md in md_files:
    text = md.read_text(encoding="utf-8")
    for match in link_re.findall(text):
        if match.startswith("http://") or match.startswith("https://"):
            continue
        if match.startswith("#"):
            continue
        target = match.split("#", 1)[0]
        if not target:
            continue
        # Skip mailto
        if target.startswith("mailto:"):
            continue
        # Resolve relative paths
        target_path = (md.parent / target).resolve()
        if not target_path.exists():
            missing.append((md, match))

if missing:
    for md, link in missing:
        print(f"missing link target: {md} -> {link}")
    sys.exit(1)

print(f"markdown links ok: {len(md_files)} files")
