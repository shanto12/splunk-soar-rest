from __future__ import annotations

from typing import Any, Dict, Optional, Union

from .base import Resource


class Approvals(Resource):
    def list(self, *, params: Optional[Dict[str, Any]] = None) -> Any:
        return self.client.call("approvals-list", params=params)

    def get(self, approval_id: Union[int, str]) -> Any:
        return self.client.call("approval-detail", path_params={"id": approval_id})

    def summary(self, approval_id: Union[int, str]) -> Any:
        return self.client.call("approval-summary", path_params={"id": approval_id})

    def create(self, payload: Dict[str, Any]) -> Any:
        return self.client.call("approval-create", json=payload)

    def update(self, approval_id: Union[int, str], payload: Dict[str, Any]) -> Any:
        return self.client.call("approval-update", path_params={"id": approval_id}, json=payload)
