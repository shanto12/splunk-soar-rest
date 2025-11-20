# Testing Guide

## Prerequisites
- Python 3.9+
- Install dependencies: `pip install -e .`
- Environment variables for live tests:
  - `SOAR_SERVER` (e.g., `https://smatthew-soar.west.buttercup.cloud`)
  - `SOAR_PH_AUTH_TOKEN` (use lab token)
  - Optional: `SOAR_VERIFY_SSL=false` (lab only; production should verify TLS)
  - Alternatively, copy `.env.example` to `.env` and fill these values.

## Unit and registry tests
```
python -m unittest tests.test_client_unit tests.test_registry
```

## Live smoke tests (lab)
```
SOAR_SERVER=... SOAR_PH_AUTH_TOKEN=... SOAR_VERIFY_SSL=false python -m unittest tests.test_integration_smoke
```
Exercises container/artifact/note/evidence, system info, indicators, vault list.

## Extended live sweep (lab)
```
SOAR_SERVER=... SOAR_PH_AUTH_TOKEN=... SOAR_VERIFY_SSL=false python scripts/run_live_tests_full.py
```
Attempts discovery (apps/assets/playbooks/roles/users/tenants), creates container, artifact, note, evidence, and hits list endpoints. Results saved to `docs/test_report_full.md`.

## Focused report run
```
SOAR_SERVER=... SOAR_PH_AUTH_TOKEN=... SOAR_VERIFY_SSL=false python scripts/run_live_tests.py
```
Produces `docs/test_report.md` with a shorter set of calls.

> Note: Both live runners disable TLS verification when `SOAR_VERIFY_SSL=false`; this is acceptable for the provided lab but not recommended for production. Update the env var to enforce verification in real deployments.
