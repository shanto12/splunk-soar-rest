from __future__ import annotations

from typing import Any

from ..client import SoarClient


class Resource:
    def __init__(self, client: SoarClient) -> None:
        self.client = client

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(base={self.client.base_url})"
