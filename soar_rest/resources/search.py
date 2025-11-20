from __future__ import annotations

from typing import Any, Dict, Optional

from .base import Resource


class Search(Resource):
    def search(self, *, params: Optional[Dict[str, Any]] = None) -> Any:
        return self.client.call("search", params=params)
