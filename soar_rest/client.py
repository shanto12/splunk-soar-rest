from __future__ import annotations

import json as jsonlib
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Optional, Tuple, Union
from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter, Retry

from .endpoints import EndpointRegistry
from .errors import SoarError


Json = Dict[str, Any]
Params = Dict[str, Any]


@dataclass
class AuthConfig:
    username: Optional[str] = None
    password: Optional[str] = None
    ph_auth_token: Optional[str] = None


class SoarClient:
    """HTTP client for Splunk SOAR REST APIs."""

    def __init__(
        self,
        server: str,
        *,
        auth: Optional[AuthConfig] = None,
        verify: Union[bool, str] = True,
        timeout: int = 30,
        proxies: Optional[Dict[str, str]] = None,
        max_retries: int = 3,
        backoff_factor: float = 0.2,
        registry: Optional[EndpointRegistry] = None,
        user_agent: str = "splunk-soar-rest/0.1.0",
    ) -> None:
        if not server.startswith("http"):
            server = f"https://{server}"
        self.base_url = server.rstrip("/") + "/"
        self.verify = verify
        self.timeout = timeout
        self.registry = registry or EndpointRegistry.load_default()

        self.session = requests.Session()
        retry = Retry(
            total=max_retries,
            backoff_factor=backoff_factor,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=None,  # retry on any method
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        self.session.headers.update(
            {
                "Accept": "application/json",
                "User-Agent": user_agent,
            }
        )
        if proxies:
            self.session.proxies.update(proxies)

        auth = auth or AuthConfig()
        if auth.ph_auth_token:
            # Token header; avoid setting basic auth to prevent 401 on some deployments
            self.session.headers["ph-auth-token"] = auth.ph_auth_token
        elif auth.username:
            self.session.auth = (auth.username, auth.password or "")

    def _build_url(self, path: str) -> str:
        clean_path = path[1:] if path.startswith("/") else path
        return urljoin(self.base_url, clean_path)

    def request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Params] = None,
        json: Optional[Any] = None,
        data: Optional[Any] = None,
        files: Optional[Any] = None,
        expected_status: Iterable[int] = (200, 201, 202, 204),
    ) -> Any:
        url = self._build_url(path)
        resp = self.session.request(
            method=method.upper(),
            url=url,
            params=params,
            json=json,
            data=data,
            files=files,
            verify=self.verify,
            timeout=self.timeout,
        )

        if resp.status_code not in expected_status:
            try:
                payload = resp.json()
            except Exception:
                payload = {"text": resp.text}
            raise SoarError(
                f"Unexpected status {resp.status_code}",
                status_code=resp.status_code,
                response=payload,
                url=url,
            )

        if resp.content:
            content_type = resp.headers.get("Content-Type", "")
            if "json" in content_type:
                return resp.json()
            return resp.text
        return None

    def get(self, path: str, **kwargs: Any) -> Any:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> Any:
        return self.request("POST", path, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> Any:
        return self.request("DELETE", path, **kwargs)

    def call(
        self,
        name: str,
        *,
        path_params: Optional[Dict[str, Any]] = None,
        params: Optional[Params] = None,
        json: Optional[Any] = None,
        data: Optional[Any] = None,
        method: Optional[str] = None,
        expected_status: Iterable[int] = (200, 201, 202, 204),
    ) -> Any:
        """Call a named endpoint from the registry."""
        endpoint = self.registry.get(name)
        resolved_path = endpoint.render(path_params or {})
        method_to_use = method or endpoint.method
        return self.request(
            method_to_use,
            resolved_path,
            params=params,
            json=json,
            data=data,
            expected_status=expected_status,
        )

    def paginate(
        self,
        path: str,
        *,
        params: Optional[Params] = None,
        page_size: int = 100,
        limit: Optional[int] = None,
    ) -> Iterable[Any]:
        """Helper for list endpoints with page/page_size semantics."""
        params = dict(params or {})
        page = 0
        yielded = 0
        while True:
            params.update({"page": page, "page_size": page_size})
            result = self.get(path, params=params)
            if not isinstance(result, dict):
                break
            data = result.get("data") or result.get("objects") or result.get("results") or []
            for item in data:
                yield item
                yielded += 1
                if limit is not None and yielded >= limit:
                    return
            if not data or len(data) < page_size:
                return
            page += 1
