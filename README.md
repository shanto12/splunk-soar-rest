# Splunk SOAR REST API Python Client

A Python client for interacting with the Splunk® SOAR (Cloud and On-Premises) REST API. This library provides a structured, object-oriented approach to making API calls for all major endpoints.

**Disclaimer:** This client is based on the "REST API Reference for Splunk SOAR (Cloud) current" document (Generated: 5/28/2025). This is not an officially supported Splunk product.

## Features

- Simple and intuitive client for all major REST API actions.
- Support for both token-based (`ph-auth-token`) and user/password authentication.
- Logical grouping of API calls based on endpoint categories (Containers, Artifacts, Playbooks, etc.).
- Built-in handling of HTTP requests, responses, and errors with a custom exception class.
- Comprehensive coverage of endpoints.

## Installation

```bash
pip install splunk-soar-rest
```

## Basic Usage

```python
from splunk_soar_rest import SplunkSOARClient

client = SplunkSOARClient(
    base_url="https://your.soar.instance",
    auth_token="your_ph_auth_token",
    verify=False
)
version_info = client.get_version()
print(version_info)
```

## Running Tests

The project includes integration tests that exercise container, artifact, and note operations. These tests require access to a Splunk SOAR instance. Set the following environment variables before running:

```
export SOAR_URL="https://your.soar.instance"
export SOAR_TOKEN="your_ph_auth_token"
```

Then execute:

```
python -m unittest -v
```
