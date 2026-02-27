#!/usr/bin/env python3
import json
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

import yaml

REPORT = Path('/home/toybook/ndefender-api-contracts/docs/TEST_RESULTS_2026-02-27.md')
OPENAPI = Path('/home/toybook/ndefender-api-contracts/docs/OPENAPI.yaml')

BASE_AGG = 'http://127.0.0.1:8001/api/v1'
BASE_SC = 'http://127.0.0.1:8002/api/v1'
BASE_RF = 'http://127.0.0.1:8890/api/v1'

# Endpoints that are safe to exercise with confirm=false and minimal payload
SKIP_SIDE_EFFECT_POST = {
    '/network/wifi/connect',
    '/network/wifi/enable',
    '/network/wifi/disable',
    '/network/wifi/disconnect',
    '/network/bluetooth/enable',
    '/network/bluetooth/disable',
    '/network/bluetooth/pair',
    '/network/bluetooth/unpair',
    '/network/bluetooth/scan/start',
    '/network/bluetooth/scan/stop',
    '/audio/mute',
    '/audio/volume',
    '/esp32/leds',
    '/esp32/buzzer',
    '/esp32/buttons/simulate',
    '/esp32/config',
}

DANGEROUS_POST = {
    '/system/reboot',
    '/system/shutdown',
    '/system-controller/system/reboot',
    '/system-controller/system/shutdown',
    '/antsdr/device/reset',
    '/antsdr/device/calibrate',
}

# If a path contains a services/{name}/restart, treat as dangerous

def is_dangerous(path: str) -> bool:
    if path in DANGEROUS_POST:
        return True
    if '/services/' in path and path.endswith('/restart'):
        return True
    return False

def is_service_specific(path: str) -> bool:
    return path.startswith('/system-controller/') or path.startswith('/antsdr-scan/') or path.startswith('/remoteid-engine/') or path.startswith('/observability/')


def run(cmd: str, timeout: int = 60) -> Tuple[int, str]:
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    out = (p.stdout or '') + (p.stderr or '')
    return p.returncode, out.strip()


def redact(s: str) -> str:
    s = re.sub(r"https://[^\s/]+@github\.com", "https://REDACTED@github.com", s)
    s = re.sub(r"ghp_[A-Za-z0-9]{10,}", "REDACTED_TOKEN", s)
    s = re.sub(r"github_pat_[A-Za-z0-9_]{10,}", "REDACTED_TOKEN", s)
    return s


def write_section(title: str, body: str) -> None:
    with REPORT.open('a') as f:
        f.write(f"\n## {title}\n\n{body}\n")


def code_block(cmd: str, out: str) -> str:
    return f"**Command:**\n\n```\n{cmd}\n```\n\n**Output:**\n\n```\n{out}\n```\n"


def parse_openapi() -> List[Tuple[str, str, List[str]]]:
    spec = yaml.safe_load(OPENAPI.read_text())
    paths = spec.get('paths', {})
    endpoints = []
    for path, methods in paths.items():
        if not isinstance(methods, dict):
            continue
        for method, info in methods.items():
            if method.lower() not in ('get', 'post'):
                continue
            tags = info.get('tags', []) or []
            endpoints.append((method.lower(), path, tags))
    return endpoints


def owner_base(tags: List[str], path: str) -> str:
    # Prefer namespace-based ownership for upstream services
    if path.startswith('/network') or path.startswith('/gps') or path.startswith('/audio') or path.startswith('/system') or path.startswith('/services') or path.startswith('/power'):
        return BASE_SC
    if path.startswith('/antsdr') or path.startswith('/antsdr-scan') or path.startswith('/rf'):
        return BASE_RF
    if path.startswith('/remote_id') or path.startswith('/remoteid'):
        # RemoteID engine not exposed on a dedicated port in this deployment
        return ''
    # Fallback to OpenAPI tags
    tag = tags[0] if tags else ''
    if tag == 'Aggregator':
        return BASE_AGG
    if tag == 'System Controller':
        return BASE_SC
    if tag == 'AntSDR Scan':
        return BASE_RF
    if tag == 'RemoteID Engine':
        return ''
    if tag == 'Observability':
        return ''
    return BASE_AGG


def substitute_params(path: str) -> str:
    return re.sub(r"\{[^/]+\}", "dummy", path)


def default_payload_for(path: str) -> Dict:
    payload = {"payload": {}, "confirm": False}
    if path.endswith('/network/wifi/connect'):
        payload = {"payload": {"ssid": "TEST_SSID", "password": "TEST_PASS", "hidden": False}, "confirm": False}
    elif path.endswith('/network/wifi/enable'):
        payload = {"payload": {"enabled": True}, "confirm": False}
    elif path.endswith('/network/wifi/disable'):
        payload = {"payload": {}, "confirm": False}
    elif path.endswith('/network/bluetooth/enable'):
        payload = {"payload": {"enabled": True}, "confirm": False}
    elif path.endswith('/network/bluetooth/disable'):
        payload = {"payload": {}, "confirm": False}
    elif '/network/bluetooth/pair' in path:
        payload = {"payload": {"addr": "00:11:22:33:44:55"}, "confirm": False}
    elif '/network/bluetooth/unpair' in path:
        payload = {"payload": {"addr": "00:11:22:33:44:55"}, "confirm": False}
    elif path.endswith('/audio/mute'):
        payload = {"payload": {"muted": True}, "confirm": False}
    elif path.endswith('/audio/volume'):
        payload = {"payload": {"volume_percent": 50}, "confirm": False}
    elif path.endswith('/vrx/tune'):
        payload = {"payload": {"vrx_id": 1, "freq_hz": 5740000000}, "confirm": False}
    elif path.endswith('/video/select'):
        payload = {"payload": {"sel": 1}, "confirm": False}
    elif path.endswith('/scan/start'):
        payload = {"payload": {}, "confirm": False}
    elif path.endswith('/scan/stop'):
        payload = {"payload": {}, "confirm": False}
    elif path.endswith('/gps/restart'):
        payload = {"payload": {}, "confirm": False}
    elif '/antsdr/sweep/start' in path:
        payload = {"payload": {"plan": "default"}, "confirm": False}
    elif '/antsdr/sweep/stop' in path:
        payload = {"payload": {}, "confirm": False}
    elif '/antsdr/gain/set' in path:
        payload = {"payload": {"mode": "auto"}, "confirm": False}
    elif '/antsdr/device/reset' in path:
        payload = {"payload": {}, "confirm": False}
    elif '/antsdr/device/calibrate' in path:
        payload = {"payload": {"kind": "rf_dc"}, "confirm": False}
    elif '/remote_id/monitor/start' in path or '/remote_id/monitor/stop' in path:
        payload = {"payload": {}, "confirm": False}
    elif '/remote_id/replay/start' in path:
        payload = {"payload": {"source": "test"}, "confirm": False}
    elif '/remote_id/replay/stop' in path:
        payload = {"payload": {}, "confirm": False}
    elif '/esp32/buzzer' in path:
        payload = {"payload": {"mode": "beep", "duration_ms": 100}, "confirm": False}
    elif '/esp32/leds' in path:
        payload = {"payload": {"red": False, "yellow": False, "green": True}, "confirm": False}
    elif '/esp32/buttons/simulate' in path:
        payload = {"payload": {"button": "mute", "action": "press"}, "confirm": False}
    elif '/esp32/config' in path:
        payload = {"payload": {"config": {}}, "confirm": False}
    elif '/services/' in path and path.endswith('/restart'):
        payload = {"payload": {}, "confirm": False}
    elif path.endswith('/system/reboot'):
        payload = {"payload": {}, "confirm": False}
    elif path.endswith('/system/shutdown'):
        payload = {"payload": {}, "confirm": False}
    return payload


def curl(method: str, url: str, payload: Dict = None, timeout: int = 30) -> Tuple[int, str, str]:
    if method == 'get':
        cmd = f"curl -sS -w '\\nHTTP_STATUS:%{{http_code}}' {url}"
    else:
        data = json.dumps(payload or {"payload": {}, "confirm": False})
        cmd = f"curl -sS -w '\\nHTTP_STATUS:%{{http_code}}' -X POST {url} -H 'Content-Type: application/json' -d '{data}'"
    code, out = run(cmd, timeout=timeout)
    out = redact(out)
    m = re.search(r"HTTP_STATUS:(\d+)", out)
    http_code = int(m.group(1)) if m else None
    body = out.replace(m.group(0), '').strip() if m else out
    return http_code or 0, body, cmd


def result_label_direct(http_code: int, body: str, method: str, path: str) -> str:
    if method == 'get':
        return 'PASS' if http_code == 200 else 'FAIL'
    if is_dangerous(path):
        return 'PASS' if http_code == 400 and 'confirm_required' in body else 'FAIL'
    return 'PASS' if http_code and http_code < 400 else 'FAIL'


def main():
    # overwrite report
    REPORT.write_text('')

    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z')
    header = f"# N-Defender Test Results — 2026-02-27 (Revision 2)\n\nGenerated: {now}\n\n**IMPORTANT:** This repo contains contracts/docs/validation only; tests were run on the Raspberry Pi against deployed services (not a local setup guide).\n\nCanonical base: `/api/v1`\nPorts: 8001 (Aggregator), 8002 (System Controller), 8890 (RFScan). Legacy 8000 must be absent.\n"
    REPORT.write_text(header + "\n")

    what_wrong = (
        "The previous report was incomplete because it executed many endpoints only via the Aggregator base, which produced 404s for upstream-owned routes. "
        "It also lacked direct-owner comparisons and field-level contract checks for UI readiness, and did not clearly classify gaps as upstream vs proxy."
    )
    write_section('0) What Was Wrong With the Previous Report', what_wrong)

    # Baseline snapshot
    baseline_cmds = [
        ('uname -a', 'uname -a'),
        ('hostname', 'hostname'),
        ('date (IST)', 'TZ=Asia/Kolkata date'),
        ('ports', "ss -lntp | egrep '(:8000|:8001|:8002|:8890)\\b' || true"),
        ('systemctl is-active', 'systemctl is-active ndefender-backend-aggregator ndefender-system-controller ndefender-rfscan ndefender-remoteid-engine'),
        ('systemctl is-enabled', 'systemctl is-enabled ndefender-backend-aggregator ndefender-system-controller ndefender-rfscan ndefender-remoteid-engine'),
        ('git status -sb', 'git -C /home/toybook/ndefender-api-contracts status -sb'),
        ('git rev-parse --short HEAD', 'git -C /home/toybook/ndefender-api-contracts rev-parse --short HEAD'),
        ('node -v', 'node -v'),
        ('npm -v', 'npm -v'),
        ('python3 --version', 'python3 --version'),
    ]
    lines = []
    for title, cmd in baseline_cmds:
        code, out = run(cmd)
        out = redact(out)
        status = 'PASS' if code == 0 else 'FAIL'
        lines.append(f"### {title}\n\n" + code_block(cmd, out) + f"\n**Result:** {status}\n")
    write_section('1) Baseline Snapshot', "\n".join(lines))

    # Repo validation
    val_lines = []
    for title, cmd in [('scripts/validate.sh', 'cd /home/toybook/ndefender-api-contracts && scripts/validate.sh'),
                       ('npm run ci', 'cd /home/toybook/ndefender-api-contracts && npm run ci')]:
        code, out = run(cmd, timeout=300)
        out = redact(out)
        status = 'PASS' if code == 0 else 'FAIL'
        val_lines.append(f"### {title}\n\n" + code_block(cmd, out) + f"\n**Result:** {status}\n")
    write_section('2) Repo Validation', "\n".join(val_lines))

    # Endpoint coverage
    endpoints = parse_openapi()
    get_endpoints = [e for e in endpoints if e[0] == 'get']
    post_endpoints = [e for e in endpoints if e[0] == 'post']

    summary_lines = [
        f"Total GET endpoints: {len(get_endpoints)}",
        f"Total POST endpoints: {len(post_endpoints)}",
        "",
    ]

    rows = []
    failure_rows = []

    for method, path, tags in endpoints:
        owner = owner_base(tags, path)
        owner_tag = tags[0] if tags else 'Unknown'
        logical_path = substitute_params(path)

        owner_base_label = owner if owner else "N/A (owner not exposed)"
        section = [f"### {method.upper()} {path}", f"**Owner tag:** {owner_tag}", f"**Owner base:** {owner_base_label}"]

        # direct-owner check
        if owner:
            url = owner + logical_path
            if method == 'post' and path in SKIP_SIDE_EFFECT_POST:
                skip_payload = '{\"payload\":{},\"confirm\":false}'
                cmd = f"curl -sS -X POST {url} -H 'Content-Type: application/json' -d '{skip_payload}'"
                out = "SKIPPED (NEEDS REAL INPUT / OPERATOR APPROVAL)"
                status = "SKIP"
                direct_http = None
            else:
                http_code, body, cmd = curl(method, url, default_payload_for(path))
                status = result_label_direct(http_code, body, method, path)
                out = body + (f"\nHTTP_STATUS:{http_code}" if http_code else '')
                direct_http = http_code
            section.append("\n**Direct-owner check:**\n\n" + code_block(cmd, out) + f"\n**Result:** {status}\n")
        else:
            status = "SKIP"
            direct_http = None
            section.append("\n**Direct-owner check:**\n\nSKIPPED (DIRECT OWNER NOT EXPOSED IN PORT LIST)\n")

        # aggregator proxy check
        agg_url = BASE_AGG + logical_path
        if is_service_specific(path):
            section.append("\n**Aggregator proxy check:** N/A (service-specific endpoint; no proxy expected)\n")
            agg_status = "SKIP"
            agg_http = None
        elif owner == BASE_AGG and owner_tag == 'Aggregator':
            section.append("\n**Aggregator proxy check:** N/A (Aggregator owns endpoint)\n")
            agg_status = "PASS" if status == "PASS" else status
            agg_http = direct_http
        else:
            if method == 'post' and path in SKIP_SIDE_EFFECT_POST:
                skip_payload = '{\"payload\":{},\"confirm\":false}'
                agg_cmd = f"curl -sS -X POST {agg_url} -H 'Content-Type: application/json' -d '{skip_payload}'"
                agg_out = "SKIPPED (NEEDS REAL INPUT / OPERATOR APPROVAL)"
                agg_status = "SKIP"
                agg_http = None
            else:
                agg_http, agg_body, agg_cmd = curl(method, agg_url, default_payload_for(path))
                agg_status = result_label_direct(agg_http, agg_body, method, path)
                agg_out = agg_body + (f"\nHTTP_STATUS:{agg_http}" if agg_http else '')
            section.append("\n**Aggregator proxy check:**\n\n" + code_block(agg_cmd, agg_out) + f"\n**Result:** {agg_status}\n")

        # classification
        classification = "PASS"
        if status == 'FAIL':
            classification = 'FAIL (UPSTREAM BUG)'
        elif status == 'PASS' and agg_status == 'FAIL':
            classification = 'FAIL (AGGREGATOR PROXY GAP)'
        elif status == 'SKIP' and agg_status == 'FAIL':
            classification = 'FAIL (AGGREGATOR PROXY GAP)'
        elif status == 'SKIP' and agg_status == 'SKIP':
            classification = 'SKIP (NEEDS REAL INPUT/OWNER NOT EXPOSED)'

        rows.append((method.upper(), path, classification))
        if classification.startswith('FAIL'):
            failure_rows.append((path, status, agg_status, classification, owner_tag))

        section.append(f"\n**Classification:** {classification}\n")
        write_section(f"3) Endpoint Coverage — {method.upper()} {path}", "\n".join(section))

    write_section('3A) Endpoint Coverage Summary', "\n".join(summary_lines))

    # Field-level contract checks
    checks = [
        ("/status", f"curl -sS {BASE_AGG}/status | jq '.timestamp_ms, .overall_ok, .system.status, .network.connected, .gps.latitude, .gps.longitude, .remote_id.state, .rf.status'"),
        ("/gps", f"curl -sS {BASE_AGG}/gps | jq '.fix, .satellites.in_view, .satellites.in_use, .latitude, .longitude'"),
        ("/network/wifi/state", f"curl -sS {BASE_AGG}/network/wifi/state | jq '.enabled, .connected, .ssid'"),
        ("/network/wifi/scan", f"curl -sS {BASE_AGG}/network/wifi/scan | jq '.networks|length'"),
        ("/network/bluetooth/state", f"curl -sS {BASE_AGG}/network/bluetooth/state | jq '.enabled, .scanning, .paired_count'"),
        ("/network/bluetooth/devices", f"curl -sS {BASE_AGG}/network/bluetooth/devices | jq '.devices|length'"),
        ("/contacts", f"curl -sS {BASE_AGG}/contacts | jq '.contacts[0].id, .contacts[0].type, .contacts[0].source, .contacts[0].last_seen_ts'"),
        ("/esp32", f"curl -sS {BASE_AGG}/esp32 | jq '.connected, .heartbeat.ok, .capabilities'"),
        ("/antsdr", f"curl -sS {BASE_AGG}/antsdr | jq '.connected, .uri'"),
        ("/remote_id/status", f"curl -sS {BASE_AGG}/remote_id/status | jq '.state, .mode, .capture_active, .contacts_active, .last_error'"),
        ("RFScan /health", f"curl -sS {BASE_RF}/health | jq '.timestamp_ms'"),
        ("RFScan /stats", f"curl -sS {BASE_RF}/stats | jq '.timestamp_ms'"),
        ("RFScan /config", f"curl -sS {BASE_RF}/config | jq '.timestamp_ms'"),
    ]
    check_lines = []
    for title, cmd in checks:
        code, out = run(cmd, timeout=30)
        out = redact(out)
        status = 'PASS' if code == 0 else 'FAIL'
        check_lines.append(f"### {title}\n\n" + code_block(cmd, out) + f"\n**Result:** {status}\n")
    write_section('4) Field-Level Contract Verification', "\n".join(check_lines))

    # Confirm-gating proof
    cmd = f"curl -sS -i -X POST {BASE_AGG}/system/reboot -H 'Content-Type: application/json' -d '{{\"payload\":{{}},\"confirm\":false}}' | sed -n '1,25p'"
    code, out = run(cmd)
    out = redact(out)
    status = 'PASS' if 'confirm_required' in out and '400' in out else 'FAIL'
    write_section('5) Confirm-Gating Proof', code_block(cmd, out) + f"\n**Result:** {status}\n")

    # WS proof
    ws_cmd = 'cd /home/toybook/ndefender-api-contracts && WS_URL=ws://127.0.0.1:8001/api/v1/ws timeout 5s python3 packages/examples/ws/ws_client_python.py'
    code, out = run(ws_cmd, timeout=10)
    out = redact(out)
    status = 'PASS' if 'connected' in out else 'FAIL'
    write_section('6) WebSocket Proof', code_block(ws_cmd, out) + f"\n**Result:** {status}\n")

    # Summary table
    total = len(endpoints)
    fail_count = len([r for r in rows if r[2].startswith('FAIL')])
    skip_count = len([r for r in rows if r[2].startswith('SKIP')])
    pass_count = total - fail_count - skip_count

    summary_table = [
        '| Metric | Value |',
        '|---|---|',
        f'| Total endpoints | {total} |',
        f'| PASS | {pass_count} |',
        f'| FAIL | {fail_count} |',
        f'| SKIP | {skip_count} |',
    ]
    write_section('7) Summary Table', "\n".join(summary_table))

    # Failure analysis
    if failure_rows:
        lines = ['| Endpoint | Direct-owner | Aggregator | Classification | Owning Repo | Suggested Fix |',
                 '|---|---|---|---|---|---|']
        for path, direct_status, agg_status, classification, owner_tag in failure_rows:
            repo = 'ndefender-backend-aggregator'
            if owner_tag == 'System Controller':
                repo = 'ndefender-system-controller'
            elif owner_tag == 'AntSDR Scan':
                repo = 'ndefender-antsdr-scan'
            elif owner_tag == 'RemoteID Engine':
                repo = 'Ndefender-Remoteid-Engine'
            lines.append(f'| {path} | {direct_status} | {agg_status} | {classification} | {repo} | Add/fix endpoint or proxy; align contract |')
        write_section('8) Failure Analysis + Next Fix Repo', "\n".join(lines))
    else:
        write_section('8) Failure Analysis + Next Fix Repo', 'No failures detected.')


if __name__ == '__main__':
    main()
