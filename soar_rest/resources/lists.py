from __future__ import annotations

from typing import Any, Dict, Optional, Union

from .base import Resource


class Lists(Resource):
    def list(self, *, params: Optional[Dict[str, Any]] = None) -> Any:
        return self.client.call("lists", params=params)

    def get(self, list_id_or_name: Union[int, str], *, params: Optional[Dict[str, Any]] = None) -> Any:
        return self.client.call("list-detail", path_params={"id": list_id_or_name}, params=params)
