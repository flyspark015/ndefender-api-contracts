# Progress Tracker

Status legend: ✅ done, 🟡 in progress, ❌ blocked.

## Steps
| Step | Status | Notes |
| --- | --- | --- |
| 1. Bootstrap repo structure + ROADMAP.md + progress.md | ✅ | Base folders created and tracking docs added. |
| 2. Extract contracts from source repos + unified model map | ✅ | Source file map + unified model map documented. |
| 3. Write docs/ALL_IN_ONE_API.md | ✅ | Complete unified all-in-one API spec. |
| 4. Write docs/WEBSOCKET_EVENTS.md | ✅ | Complete WS event catalog + examples + reconnect behavior. |
| 5. Generate schemas/ JSON Schema + validate | ✅ | Schemas generated and Draft2020-12 validation passed. |
| 6. Generate types/contracts.ts | 🟡 | Pending. |
| 7. Generate docs/OPENAPI.yaml + validate | 🟡 | Pending. |
| 8. Add examples/ + postman/ | 🟡 | Pending. |
| 9. Add CI checks | 🟡 | Pending. |
| 10. Tag v1.0.0-api-contracts-green + release notes | 🟡 | Pending. |

## Verification Evidence
Step 1:
```
$ ls -F ndefender-api-contracts
README.md
ci/
docs/
examples/
postman/
schemas/
types/
```

Step 2:
```
$ ls ndefender-api-contracts/docs
CONTRACT_SOURCES.md
UNIFIED_MODEL_MAP.md
```

Step 3:
```
$ rg -n \"Backend Aggregator API\" ndefender-api-contracts/docs/ALL_IN_ONE_API.md
120:## 🌐 Backend Aggregator API (Primary)
```

Step 4:
```
$ rg -n \"Event Type Catalog\" ndefender-api-contracts/docs/WEBSOCKET_EVENTS.md
347:## 🧾 Event Type Catalog (All Systems)
```

Step 5:
```
$ python3 - <<'PY'
import json
from pathlib import Path
import jsonschema
root = Path(\"ndefender-api-contracts/schemas\")
for path in sorted(root.glob(\"*.json\")):
    jsonschema.Draft202012Validator.check_schema(json.loads(path.read_text()))
print(\"all schemas valid\")
PY
all schemas valid
```
