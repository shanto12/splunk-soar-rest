# Splunk SOAR REST SDK & CLI

Python toolkit and Typer CLI for the Splunk SOAR REST API with a data-driven endpoint registry, resource helpers, and live test runners.

## Quick start
1. Install (editable): `pip install -e .`
2. Export creds (token preferred):
   - `SOAR_SERVER=https://your-soar-host`
   - `SOAR_PH_AUTH_TOKEN=<ph-auth-token>` (or `SOAR_USERNAME`/`SOAR_PASSWORD`)
   - Optional lab-only: `SOAR_VERIFY_SSL=false` to skip TLS verification.
   - You can also copy `.env.example` to `.env` and fill these values for local runs.
3. CLI samples:
   - `python -m soar_rest.cli system info`
   - `python -m soar_rest.cli containers list -f _filter_name__icontains=phish --page-size 5`
   - `python -m soar_rest.cli containers create "Example" --label events --severity high`
   - `python -m soar_rest.cli artifacts create --container-id 1 --name ip --cef '{"sourceAddress":"1.1.1.1"}'`
   - `python -m soar_rest.cli actions run --action "geolocate ip" --asset maxmind --param ip=1.1.1.1`
   - `python -m soar_rest.cli playbooks run --container-id 1 --playbook-id 42`

## Library usage
```python
from soar_rest.client import SoarClient, AuthConfig
from soar_rest.resources import Containers, Actions
from soar_rest.models import Container, RunActionRequest

client = SoarClient("https://soar.lab.local", auth=AuthConfig(ph_auth_token="..."), verify=False)

# List containers
containers = Containers(client).list(params={"page_size": 5})

# Create a container
new_container = Containers(client).create(Container(name="Example", label="events"))

# Run an action
req = RunActionRequest(action="whois ip", parameters=[{"ip": "1.1.1.1"}], assets=["whois"], container_id=new_container["id"])
result = Actions(client).run(req)
```

## Endpoint registry
- Primary catalog: `soar_rest/spec/endpoints.yaml` (curated common endpoints).
- Full doc-derived list (311 patterns): `soar_rest/spec/endpoints_full.yaml` (auto-merged by the registry loader).
- Extracted raw list from docs: `docs/endpoints_clean.txt`. Research summary: `docs/research.md`.

## Testing
- Unit/registry: `python -m unittest tests.test_client_unit tests.test_registry`
- Live smoke (lab): `SOAR_SERVER=... SOAR_PH_AUTH_TOKEN=... SOAR_VERIFY_SSL=false python -m unittest tests.test_integration_smoke`
- Live reports:
  - Short run: `python scripts/run_live_tests.py` -> `docs/test_report.md`
  - Extended run: `python scripts/run_live_tests_full.py` -> `docs/test_report_full.md`
- See `docs/TESTING.md` for full details.

## Repo contents
- `soar_rest/`: client, resources, models, endpoint specs.
- `scripts/`: live test runners.
- `tests/`: unit + integration smoke tests.
- `docs/`: research, plans, endpoint extraction, endpoint list, testing guide, and live test reports.
