"""
Best-effort live test runner against a SOAR instance using ph-auth-token.
Discovers playbooks/assets/etc. and attempts representative calls.
All calls are logged to docs/test_report_full.md with status/responses.

TLS verification is disabled by default to match lab use.
"""

import json
import os
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import requests


def main() -> None:
    server = os.environ.get("SOAR_SERVER")
    token = os.environ.get("SOAR_PH_AUTH_TOKEN")
    verify_env = os.environ.get("SOAR_VERIFY_SSL", "false").lower()
    verify = not (verify_env in {"0", "false", "no"})

    if not server or not token:
        raise SystemExit("SOAR_SERVER and SOAR_PH_AUTH_TOKEN must be set")

    sess = requests.Session()
    sess.headers.update({"ph-auth-token": token})

    results: List[Dict[str, Any]] = []

    def record(name: str, method: str, path: str, **kwargs: Any) -> Dict[str, Any]:
        url = f"{server}{path}"
        try:
            resp = sess.request(method, url, verify=verify, timeout=30, **kwargs)
            status = resp.status_code
            try:
                payload = resp.json()
            except Exception:
                payload = resp.text
        except Exception as exc:  # network or other
            status = -1
            payload = str(exc)
        entry = {
            "name": name,
            "method": method,
            "path": path,
            "status": status,
            "response": payload,
        }
        results.append(entry)
        return entry

    def first_id(resp: Dict[str, Any], key: str = "data") -> Optional[int]:
        data = resp.get("response")
        if isinstance(data, dict):
            items = data.get(key) or data.get("objects") or data.get("results") or []
            if items and isinstance(items, list):
                if isinstance(items[0], dict) and "id" in items[0]:
                    return items[0]["id"]
        return None

    # System/info endpoints
    system_info = record("system_info", "GET", "/rest/system_info")
    severity = record("severity_list", "GET", "/rest/severity")

    # Discovery endpoints
    apps = record("apps_list", "GET", "/rest/app")
    assets = record("assets_list", "GET", "/rest/asset")
    playbooks = record("playbooks_list", "GET", "/rest/playbook")
    roles = record("roles_list", "GET", "/rest/role")
    users = record("users_list", "GET", "/rest/ph_user")
    tenants = record("tenants_list", "GET", "/rest/tenant")
    indicators = record("indicators_list", "GET", "/rest/indicator", params={"page_size": 1, "page": 0})
    vault_docs = record("vault_list", "GET", "/rest/vault_document", params={"page_size": 1, "page": 0})
    lists_resp = record("decided_list", "GET", "/rest/decided_list", params={"page_size": 1, "page": 0})

    # Container + children
    c_name = f"codex-auto-{int(time.time())}"
    c_resp = record(
        "container_create",
        "POST",
        "/rest/container",
        json={"name": c_name, "label": "events", "severity": "medium"},
    )
    cid = c_resp["response"].get("id") if isinstance(c_resp["response"], dict) else None

    a_resp = record(
        "artifact_create",
        "POST",
        "/rest/artifact",
        json={
            "container_id": cid,
            "name": "auto-ip",
            "cef": {"sourceAddress": "1.1.1.1"},
            "label": "event",
        },
    )
    aid = a_resp["response"].get("id") if isinstance(a_resp["response"], dict) else None

    record(
        "note_create",
        "POST",
        "/rest/note",
        json={"container_id": cid, "content": "automated note", "title": "codex", "note_type": "general"},
    )

    record(
        "evidence_create",
        "POST",
        "/rest/evidence",
        json={
            "container_id": cid,
            "content": "auto evidence",
            "content_type": "artifact",
            "object_id": aid,
        },
    )

    # Approval
    record(
        "approval_create",
        "POST",
        "/rest/approval",
        json={"container_id": cid, "summary": "auto approval", "status": "pending"},
    )

    # Run playbook on this container if available
    pb_id = first_id(playbooks)
    if pb_id and cid:
        record(
            "run_playbook",
            "POST",
            "/rest/run_playbook",
            json={"playbook_id": pb_id, "container_id": cid, "scope": "all", "run": True},
        )
    else:
        results.append(
            {
                "name": "run_playbook",
                "method": "POST",
                "path": "/rest/run_playbook",
                "status": 0,
                "response": "skipped (no playbook id or container id)",
            }
        )

    # Audit log query (small page)
    record("audit_list", "GET", "/rest/audit", params={"page_size": 1, "page": 0})

    # Compile report
    ts = datetime.now(timezone.utc).isoformat()
    report_lines = []
    report_lines.append(f"# Live Test Report (Extended)\n")
    report_lines.append(f"- Timestamp (UTC): {ts}")
    report_lines.append(f"- Server: {server}")
    report_lines.append(f"- Verify SSL: {verify}")
    report_lines.append(f"- Tests executed: {len(results)}\n")
    report_lines.append("## Results\n")
    for entry in results:
        resp = entry["response"]
        if isinstance(resp, dict):
            snippet = json.dumps(resp, indent=2)[:1200]
        else:
            snippet = str(resp)[:1200]
        report_lines.append(f"### {entry['name']}")
        report_lines.append(f"- Method: {entry['method']}")
        report_lines.append(f"- Path: {entry['path']}")
        report_lines.append(f"- Status: {entry['status']}")
        report_lines.append(f"- Response:\n```\n{snippet}\n```\n")

    report_path = os.path.join("docs", "test_report_full.md")
    os.makedirs("docs", exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
    print(f"wrote {report_path}")


if __name__ == "__main__":
    main()
