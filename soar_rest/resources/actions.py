from __future__ import annotations

from typing import Any, Dict, Optional, Union

from ..models import RunActionRequest
from .base import Resource


class Actions(Resource):
    def run(self, request: Union[RunActionRequest, Dict[str, Any]]) -> Any:
        payload = request.to_payload() if isinstance(request, RunActionRequest) else request
        return self.client.call("run-action", json=payload)

    def get_run(self, action_run_id: Union[int, str]) -> Any:
        return self.client.call("action-run-detail", path_params={"id": action_run_id})

    def app_runs(self, action_run_id: Union[int, str], *, params: Optional[Dict[str, Any]] = None) -> Any:
        return self.client.call("action-run-app-runs", path_params={"id": action_run_id}, params=params)
