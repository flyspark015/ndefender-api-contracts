# PROGRESS TRACKER — N-Defender (Global)

Last updated: 2026-02-27

Latest evidence: docs/TEST_RESULTS_2026-02-27.md — Total endpoints 84 / PASS 48 / FAIL 4 / SKIP 32.

## Repo Status

| Repo | Status | Notes |
| --- | --- | --- |
| ndefender-api-contracts | IN_PROGRESS | Evidence ran 2026-02-27; tracker added; needs evidence classification fixes and PROGRESS.md alignment. |
| ndefender-backend-aggregator | IN_PROGRESS | /antsdr/sweep/stop precondition failure; remaining AntSDR command failures. |
| ndefender-system-controller | PENDING | /ups proxy gap (aggregator proxy or contract alignment). |
| ndefender-antsdr-scan | PENDING | Aggregator proxy gaps for /version, /stats, /device, /sweep/state, /gain, /config; sweep/gain endpoints failing. |
| ndefender-remoteid-engine | BLOCKED_EXTERNAL | Optional runtime; not running; aggregator returns 502 remoteid_service_unreachable. |
| UI repo (unknown name) | PENDING | Repo not found in /home/toybook; needs identification. |

## Evidence P0/P1/P2 Focus (from 2026-02-27 run)
- UI blockers now pass with deterministic 502 on /remote_id/monitor/*.
- WS: /ws PASS in evidence; must validate node+python WS clients per harness rules.
- Remaining FAILs: AntSDR command endpoints (/sweep/start, /sweep/stop, /gain/set) and /antsdr/sweep/stop precondition.
