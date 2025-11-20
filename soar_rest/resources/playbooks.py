from __future__ import annotations

from typing import Any, Dict, Optional, Union

from ..models import RunPlaybookRequest
from .base import Resource


class Playbooks(Resource):
    def list(self, *, params: Optional[Dict[str, Any]] = None) -> Any:
        return self.client.call("playbooks-list", params=params)

    def get(self, playbook_id: Union[int, str]) -> Any:
        return self.client.call("playbook-detail", path_params={"id": playbook_id})

    def update(self, playbook_id: Union[int, str], payload: Dict[str, Any]) -> Any:
        return self.client.call("playbook-update", path_params={"id": playbook_id}, json=payload)

    def run(self, request: Union[RunPlaybookRequest, Dict[str, Any]]) -> Any:
        payload = request.to_payload() if isinstance(request, RunPlaybookRequest) else request
        return self.client.call("run-playbook", json=payload)
