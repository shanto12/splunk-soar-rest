from __future__ import annotations

from typing import Any, Dict, Optional, Union

from .base import Resource


class Indicators(Resource):
    def list(self, *, params: Optional[Dict[str, Any]] = None) -> Any:
        return self.client.call("indicators", params=params)

    def get(self, indicator_id: Union[int, str], *, params: Optional[Dict[str, Any]] = None) -> Any:
        return self.client.call("indicator-detail", path_params={"id": indicator_id}, params=params)

    def find_by_value(self, value: str, *, params: Optional[Dict[str, Any]] = None) -> Any:
        params = dict(params or {})
        params.setdefault("indicator_value", value)
        return self.client.call("indicator-by-value", params=params)
