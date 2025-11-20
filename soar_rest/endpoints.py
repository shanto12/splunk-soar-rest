from __future__ import annotations

import importlib.resources as pkg_resources
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional

import yaml

from .errors import SoarError


@dataclass
class Endpoint:
    name: str
    path: str
    method: str
    description: str = ""

    def render(self, path_params: Dict[str, object]) -> str:
        resolved = self.path
        for key, value in path_params.items():
            resolved = resolved.replace(f"{{{key}}}", str(value))
        return resolved


class EndpointRegistry:
    def __init__(self, endpoints: Iterable[Endpoint]) -> None:
        self._items: Dict[str, Endpoint] = {e.name: e for e in endpoints}

    def get(self, name: str) -> Endpoint:
        try:
            return self._items[name]
        except KeyError as exc:
            raise SoarError(f"Unknown endpoint '{name}'") from exc

    def names(self) -> List[str]:
        return sorted(self._items.keys())

    @classmethod
    def load_default(cls) -> "EndpointRegistry":
        try:
            spec_path = pkg_resources.files("soar_rest.spec").joinpath("endpoints.yaml")
            data = yaml.safe_load(spec_path.read_text())
        except FileNotFoundError as exc:
            raise SoarError("Missing endpoint spec") from exc
        endpoints = [
            Endpoint(
                name=item["name"],
                path=item["path"],
                method=item.get("method", "GET").upper(),
                description=item.get("description", ""),
            )
            for item in data.get("endpoints", [])
        ]
        # Optionally augment with docs/endpoints_clean.txt if present in the workspace
        try:
            extra_path = pkg_resources.files("soar_rest.spec").joinpath("endpoints_full.yaml")
            extra_data = yaml.safe_load(extra_path.read_text())
            for item in extra_data.get("endpoints", []):
                name = item.get("name")
                if name not in [e.name for e in endpoints]:
                    endpoints.append(
                        Endpoint(
                            name=name,
                            path=item["path"],
                            method=item.get("method", "GET").upper(),
                            description=item.get("description", ""),
                        )
                    )
        except FileNotFoundError:
            # full list is optional; continue with base endpoints
            pass
        return cls(endpoints)
