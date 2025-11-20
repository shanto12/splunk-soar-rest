# Implementation plan for Splunk SOAR REST repository

## Goals
- Provide a Python SDK and CLI that cover the Splunk SOAR REST API surface (per official docs).
- Keep endpoints data-driven so new endpoints can be added without changing core code.
- Include examples, integration smoke tests (opt-in), and offline doc references.

## Architecture
- `pyproject.toml`: packaging metadata; dependencies `requests`, `typer`, `pydantic`.
- `soar_rest/`
  - `client.py`: shared HTTP client with auth (basic or ph-auth-token), session, retries, SSL controls.
  - `endpoints.py`: load endpoint metadata (from `spec/endpoints.yaml`) and expose a registry.
  - `resources/`: thin wrappers around key endpoint families (containers, artifacts, playbooks, actions, assets, users/roles, audit, indicators, approvals, notes/evidence, lists/vault, system/info).
  - `models.py`: typed request/response helpers using `pydantic` for common payloads (Container, Artifact, RunActionRequest, RunPlaybookRequest, Note/Evidence, Approval, etc.).
  - `errors.py`: custom exceptions, response validation helpers.
  - `cli.py`: Typer-powered CLI surfacing high-value commands (info, containers list/get/create, artifacts create, run-action, run-playbook, vault download/upload, audit search).
- `spec/endpoints.yaml`: normalized endpoint catalog derived from docs; includes method, path template, and short description.
- `examples/`: runnable samples for common tasks.
- `tests/`
  - `test_client_unit.py`: unit tests with mocked responses.
  - `test_registry.py`: ensures registry covers extracted endpoints.
  - `test_integration_smoke.py`: optional live tests gated by env vars (`SOAR_SERVER`, `SOAR_PH_AUTH_TOKEN`, `SOAR_VERIFY_SSL`) hitting only safe GET/POST endpoints (`/rest/info`, `/rest/system/info`, containers list limited page_size=1`).
- `docs/`: research and usage guide; include generated endpoint list (`docs/endpoints_clean.txt`).

## Data-driven endpoint coverage
- Parse `docs/endpoints_clean.txt` into a curated `spec/endpoints.yaml` with sections grouped by families. Each entry stores:
  - `name`: machine-friendly key (e.g., `containers`, `containers-detail`, `run-playbook`).
  - `path`: e.g., `/rest/container/{id}`.
  - `method`: default HTTP verb(s) supported.
  - `description`: short summary from docs.
- `endpoints.py` exposes lookup/iteration; `SoarClient.call(name, **path_params, params=None, json=None)` builds URLs using the registry.
- Resource helpers use the registry and add convenience logic (payload shaping, defaults, pagination helpers).

## Auth and safety
- Support username/password or token (`ph-auth-token` header). Token can be read from env (`SOAR_PH_AUTH_TOKEN`).
- Allow SSL verify toggle and proxy config.
- Safe-by-default integration tests: use `GET` or dry-run endpoints; warn before destructive calls.

## Testing plan
- Unit: mock `requests.Session.request` to verify URL assembly, headers, error handling, pagination.
- Registry sanity: ensure each spec entry produces a URL and maps to recognized method.
- Integration (opt-in): when env vars are set, run the smoke suite against the provided lab instance; only non-destructive calls plus a sample POST/PUT on a temp container with a unique name to avoid collisions.

## Deliverables
- Working Python package and CLI.
- Markdown docs (README, usage, research), examples.
- Endpoint catalog (`spec/endpoints.yaml`) + extraction artifact.
- Tests and instructions to run them locally.

