from __future__ import annotations

import json
import os
from typing import Dict, List, Optional

import typer
from rich import print_json

from .client import AuthConfig, SoarClient
from .models import Artifact, Container, RunActionRequest, RunPlaybookRequest
from .resources import (
    Actions,
    Artifacts,
    Audit,
    Containers,
    Indicators,
    Lists,
    Notes,
    Playbooks,
    System,
    Vault,
)

app = typer.Typer(add_completion=False, help="Splunk SOAR REST CLI")
containers_app = typer.Typer(help="Container operations")
playbooks_app = typer.Typer(help="Playbook operations")
actions_app = typer.Typer(help="Action runs")
artifacts_app = typer.Typer(help="Artifacts")
system_app = typer.Typer(help="System/info")
audit_app = typer.Typer(help="Audit search")
indicators_app = typer.Typer(help="Indicators")

app.add_typer(containers_app, name="containers")
app.add_typer(playbooks_app, name="playbooks")
app.add_typer(actions_app, name="actions")
app.add_typer(artifacts_app, name="artifacts")
app.add_typer(system_app, name="system")
app.add_typer(audit_app, name="audit")
app.add_typer(indicators_app, name="indicators")


def parse_kv_pairs(pairs: List[str]) -> Dict[str, str]:
    data: Dict[str, str] = {}
    for pair in pairs:
        if "=" not in pair:
            raise typer.BadParameter(f"Expected key=value, got {pair}")
        key, value = pair.split("=", 1)
        data[key] = value
    return data


def build_client(
    server: Optional[str],
    token: Optional[str],
    username: Optional[str],
    password: Optional[str],
    verify_ssl: bool,
) -> SoarClient:
    server = server or os.getenv("SOAR_SERVER")
    if not server:
        raise typer.BadParameter("Missing --server or SOAR_SERVER")
    auth = AuthConfig(
        username=username or os.getenv("SOAR_USERNAME"),
        password=password or os.getenv("SOAR_PASSWORD"),
        ph_auth_token=token or os.getenv("SOAR_PH_AUTH_TOKEN"),
    )
    verify_env = os.getenv("SOAR_VERIFY_SSL")
    verify = verify_ssl if verify_env is None else verify_env.lower() not in {"0", "false", "no"}
    return SoarClient(server=server, auth=auth, verify=verify)


@system_app.command("info")
def info(
    server: Optional[str] = typer.Option(None, envvar="SOAR_SERVER"),
    token: Optional[str] = typer.Option(None, envvar="SOAR_PH_AUTH_TOKEN"),
    username: Optional[str] = typer.Option(None, envvar="SOAR_USERNAME"),
    password: Optional[str] = typer.Option(None, envvar="SOAR_PASSWORD"),
    verify_ssl: bool = typer.Option(True, "--verify/--no-verify", envvar="SOAR_VERIFY_SSL"),
) -> None:
    client = build_client(server, token, username, password, verify_ssl)
    system = System(client)
    data = system.info()
    print_json(data=data)


@containers_app.command("list")
def containers_list(
    server: Optional[str] = typer.Option(None, envvar="SOAR_SERVER"),
    token: Optional[str] = typer.Option(None, envvar="SOAR_PH_AUTH_TOKEN"),
    username: Optional[str] = typer.Option(None, envvar="SOAR_USERNAME"),
    password: Optional[str] = typer.Option(None, envvar="SOAR_PASSWORD"),
    verify_ssl: bool = typer.Option(True, "--verify/--no-verify", envvar="SOAR_VERIFY_SSL"),
    filter: List[str] = typer.Option([], "--filter", "-f", help="Query params as key=value"),
    page: int = typer.Option(0),
    page_size: int = typer.Option(10),
) -> None:
    client = build_client(server, token, username, password, verify_ssl)
    params = parse_kv_pairs(filter)
    params.update({"page": page, "page_size": page_size})
    containers = Containers(client)
    data = containers.list(params=params)
    print_json(data=data)


@containers_app.command("get")
def containers_get(
    container_id: int,
    server: Optional[str] = typer.Option(None, envvar="SOAR_SERVER"),
    token: Optional[str] = typer.Option(None, envvar="SOAR_PH_AUTH_TOKEN"),
    username: Optional[str] = typer.Option(None, envvar="SOAR_USERNAME"),
    password: Optional[str] = typer.Option(None, envvar="SOAR_PASSWORD"),
    verify_ssl: bool = typer.Option(True, "--verify/--no-verify", envvar="SOAR_VERIFY_SSL"),
) -> None:
    client = build_client(server, token, username, password, verify_ssl)
    data = Containers(client).get(container_id)
    print_json(data=data)


@containers_app.command("create")
def containers_create(
    name: str,
    label: str = typer.Option("events"),
    severity: Optional[str] = typer.Option(None),
    description: Optional[str] = typer.Option(None),
    server: Optional[str] = typer.Option(None, envvar="SOAR_SERVER"),
    token: Optional[str] = typer.Option(None, envvar="SOAR_PH_AUTH_TOKEN"),
    username: Optional[str] = typer.Option(None, envvar="SOAR_USERNAME"),
    password: Optional[str] = typer.Option(None, envvar="SOAR_PASSWORD"),
    verify_ssl: bool = typer.Option(True, "--verify/--no-verify", envvar="SOAR_VERIFY_SSL"),
) -> None:
    client = build_client(server, token, username, password, verify_ssl)
    payload = Container(name=name, label=label, severity=severity, description=description)
    data = Containers(client).create(payload)
    print_json(data=data)


@artifacts_app.command("create")
def artifacts_create(
    container_id: int,
    name: str,
    cef: str = typer.Option(..., help="CEF JSON payload"),
    label: Optional[str] = typer.Option(None),
    server: Optional[str] = typer.Option(None, envvar="SOAR_SERVER"),
    token: Optional[str] = typer.Option(None, envvar="SOAR_PH_AUTH_TOKEN"),
    username: Optional[str] = typer.Option(None, envvar="SOAR_USERNAME"),
    password: Optional[str] = typer.Option(None, envvar="SOAR_PASSWORD"),
    verify_ssl: bool = typer.Option(True, "--verify/--no-verify", envvar="SOAR_VERIFY_SSL"),
) -> None:
    client = build_client(server, token, username, password, verify_ssl)
    cef_payload = json.loads(cef)
    artifact = Artifact(container_id=container_id, name=name, label=label, cef=cef_payload)
    data = Artifacts(client).create(artifact)
    print_json(data=data)


@actions_app.command("run")
def actions_run(
    action: str,
    asset: List[str] = typer.Option(..., "--asset", "-a"),
    parameter: List[str] = typer.Option([], "--param", "-p", help="parameter=value"),
    container_id: Optional[int] = typer.Option(None, help="Optional container id"),
    server: Optional[str] = typer.Option(None, envvar="SOAR_SERVER"),
    token: Optional[str] = typer.Option(None, envvar="SOAR_PH_AUTH_TOKEN"),
    username: Optional[str] = typer.Option(None, envvar="SOAR_USERNAME"),
    password: Optional[str] = typer.Option(None, envvar="SOAR_PASSWORD"),
    verify_ssl: bool = typer.Option(True, "--verify/--no-verify", envvar="SOAR_VERIFY_SSL"),
) -> None:
    client = build_client(server, token, username, password, verify_ssl)
    parameters = parse_kv_pairs(parameter)
    request = RunActionRequest(action=action, parameters=[parameters], assets=asset, container_id=container_id)
    data = Actions(client).run(request)
    print_json(data=data)


@playbooks_app.command("run")
def playbook_run(
    container_id: int,
    playbook_id: Optional[int] = typer.Option(None, help="Playbook id"),
    playbook: Optional[str] = typer.Option(None, help="Playbook FQDN"),
    scope: Optional[str] = typer.Option("all"),
    inputs: Optional[str] = typer.Option(None, help="JSON string of inputs"),
    server: Optional[str] = typer.Option(None, envvar="SOAR_SERVER"),
    token: Optional[str] = typer.Option(None, envvar="SOAR_PH_AUTH_TOKEN"),
    username: Optional[str] = typer.Option(None, envvar="SOAR_USERNAME"),
    password: Optional[str] = typer.Option(None, envvar="SOAR_PASSWORD"),
    verify_ssl: bool = typer.Option(True, "--verify/--no-verify", envvar="SOAR_VERIFY_SSL"),
) -> None:
    client = build_client(server, token, username, password, verify_ssl)
    inputs_payload = json.loads(inputs) if inputs else None
    request = RunPlaybookRequest(
        container_id=container_id, playbook_id=playbook_id, playbook=playbook, scope=scope, inputs=inputs_payload
    )
    data = Playbooks(client).run(request)
    print_json(data=data)


@audit_app.command("search")
def audit_search(
    filter: List[str] = typer.Option([], "--filter", "-f", help="key=value"),
    server: Optional[str] = typer.Option(None, envvar="SOAR_SERVER"),
    token: Optional[str] = typer.Option(None, envvar="SOAR_PH_AUTH_TOKEN"),
    username: Optional[str] = typer.Option(None, envvar="SOAR_USERNAME"),
    password: Optional[str] = typer.Option(None, envvar="SOAR_PASSWORD"),
    verify_ssl: bool = typer.Option(True, "--verify/--no-verify", envvar="SOAR_VERIFY_SSL"),
) -> None:
    client = build_client(server, token, username, password, verify_ssl)
    params = parse_kv_pairs(filter)
    data = Audit(client).search(params=params)
    print_json(data=data)


@indicators_app.command("list")
def indicators_list(
    filter: List[str] = typer.Option([], "--filter", "-f", help="key=value"),
    server: Optional[str] = typer.Option(None, envvar="SOAR_SERVER"),
    token: Optional[str] = typer.Option(None, envvar="SOAR_PH_AUTH_TOKEN"),
    username: Optional[str] = typer.Option(None, envvar="SOAR_USERNAME"),
    password: Optional[str] = typer.Option(None, envvar="SOAR_PASSWORD"),
    verify_ssl: bool = typer.Option(True, "--verify/--no-verify", envvar="SOAR_VERIFY_SSL"),
) -> None:
    client = build_client(server, token, username, password, verify_ssl)
    params = parse_kv_pairs(filter)
    data = Indicators(client).list(params=params)
    print_json(data=data)


@app.command("lists")
def lists(
    filter: List[str] = typer.Option([], "--filter", "-f", help="key=value"),
    server: Optional[str] = typer.Option(None, envvar="SOAR_SERVER"),
    token: Optional[str] = typer.Option(None, envvar="SOAR_PH_AUTH_TOKEN"),
    username: Optional[str] = typer.Option(None, envvar="SOAR_USERNAME"),
    password: Optional[str] = typer.Option(None, envvar="SOAR_PASSWORD"),
    verify_ssl: bool = typer.Option(True, "--verify/--no-verify", envvar="SOAR_VERIFY_SSL"),
) -> None:
    client = build_client(server, token, username, password, verify_ssl)
    params = parse_kv_pairs(filter)
    data = Lists(client).list(params=params)
    print_json(data=data)


@app.command("vault")
def vault(
    server: Optional[str] = typer.Option(None, envvar="SOAR_SERVER"),
    token: Optional[str] = typer.Option(None, envvar="SOAR_PH_AUTH_TOKEN"),
    username: Optional[str] = typer.Option(None, envvar="SOAR_USERNAME"),
    password: Optional[str] = typer.Option(None, envvar="SOAR_PASSWORD"),
    verify_ssl: bool = typer.Option(True, "--verify/--no-verify", envvar="SOAR_VERIFY_SSL"),
) -> None:
    client = build_client(server, token, username, password, verify_ssl)
    data = Vault(client).list()
    print_json(data=data)


if __name__ == "__main__":
    app()
