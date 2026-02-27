# PROGRESS TRACKER — N-Defender (Global)

Last updated: 2026-02-27

Latest evidence: docs/TEST_RESULTS_2026-02-27.md — Total endpoints 84 / PASS 37 / FAIL 15 / SKIP 32.

## Repo Status

| Repo | Status | Notes |
| --- | --- | --- |
| ndefender-api-contracts | IN_PROGRESS | Evidence ran 2026-02-27; tracker added; needs evidence classification fixes and PROGRESS.md alignment. |
| ndefender-backend-aggregator | IN_PROGRESS | UI blockers: /remote_id/monitor/start + /remote_id/monitor/stop; /antsdr/sweep/stop precondition failure. |
| ndefender-system-controller | PENDING | /ups proxy gap (aggregator proxy or contract alignment). |
| ndefender-antsdr-scan | PENDING | Aggregator proxy gaps for /version, /stats, /device, /sweep/state, /gain, /config; sweep/gain endpoints failing. |
| ndefender-remoteid-engine | BLOCKED_EXTERNAL | Optional runtime; not running; aggregator returns 502 remoteid_service_unreachable. |
| UI repo (unknown name) | PENDING | Repo not found in /home/toybook; needs identification. |

## Evidence P0/P1/P2 Focus (from 2026-02-27 run)
- UI blockers failing: /remote_id/monitor/start, /remote_id/monitor/stop.
- WS: /ws PASS in evidence; must validate node+python WS clients per harness rules.
- Misclassification: 502 remoteid_service_unreachable currently marked FAIL (should be PASS for deterministic 502).
