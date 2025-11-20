import json
import os
import time
from datetime import datetime, timezone
from typing import Any, Dict, List

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
        resp = sess.request(method, url, verify=verify, **kwargs)
        try:
            payload = resp.json()
        except Exception:
            payload = resp.text
        entry = {
            "name": name,
            "method": method,
            "path": path,
            "status": resp.status_code,
            "response": payload,
        }
        results.append(entry)
        return entry

    # Phase 1: read-only info
    record("system_info", "GET", "/rest/system_info")
    record("severity_list", "GET", "/rest/severity")

    # Phase 2: create container, artifact, note, evidence
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

    # Phase 3: list indicators and vault
    record("indicators_list", "GET", "/rest/indicator", params={"page_size": 1, "page": 0})
    record("vault_list", "GET", "/rest/vault_document", params={"page_size": 1, "page": 0})

    # Write report
    ts = datetime.now(timezone.utc).isoformat()
    report_lines = []
    report_lines.append(f"# Live Test Report\n")
    report_lines.append(f"- Timestamp (UTC): {ts}")
    report_lines.append(f"- Server: {server}")
    report_lines.append(f"- Verify SSL: {verify}")
    report_lines.append(f"- Tests executed: {len(results)}\n")
    report_lines.append("## Results\n")
    for entry in results:
        resp = entry["response"]
        if isinstance(resp, dict):
            snippet = json.dumps(resp, indent=2)[:800]
        else:
            snippet = str(resp)[:800]
        report_lines.append(f"### {entry['name']}")
        report_lines.append(f"- Method: {entry['method']}")
        report_lines.append(f"- Path: {entry['path']}")
        report_lines.append(f"- Status: {entry['status']}")
        report_lines.append(f"- Response:\n```\n{snippet}\n```\n")

    report_path = os.path.join("docs", "test_report.md")
    os.makedirs("docs", exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
    print(f"wrote {report_path}")


if __name__ == "__main__":
    main()
