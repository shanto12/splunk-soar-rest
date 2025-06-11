"""Simple client for interacting with the Splunk SOAR REST API."""

import requests

__all__ = ["SOARClient"]
__version__ = "0.1.0"


class SOARClient:
    """Basic wrapper around the Splunk SOAR REST endpoints."""

    def __init__(self, base_url: str, token: str):
        self.base_url = base_url.rstrip("/")
        self.headers = {"ph-auth-token": token}

    def get(self, endpoint: str):
        response = requests.get(f"{self.base_url}{endpoint}", headers=self.headers)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint: str, json=None):
        response = requests.post(f"{self.base_url}{endpoint}", headers=self.headers, json=json)
        response.raise_for_status()
        return response.json()
