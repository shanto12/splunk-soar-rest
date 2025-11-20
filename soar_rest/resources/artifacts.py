from __future__ import annotations

from typing import Any, Dict, Iterable, Optional, Union

from ..models import Artifact
from .base import Resource


class Artifacts(Resource):
    def list(self, *, params: Optional[Dict[str, Any]] = None) -> Any:
        return self.client.call("artifacts-list", params=params)

    def iterate(
        self, *, params: Optional[Dict[str, Any]] = None, page_size: int = 100, limit: Optional[int] = None
    ) -> Iterable[Any]:
        return self.client.paginate("/rest/artifact", params=params, page_size=page_size, limit=limit)

    def get(self, artifact_id: Union[int, str]) -> Any:
        return self.client.call("artifact-detail", path_params={"id": artifact_id})

    def create(self, artifact: Union[Artifact, Dict[str, Any]]) -> Any:
        payload = artifact.to_payload() if isinstance(artifact, Artifact) else artifact
        return self.client.call("artifact-create", json=payload)

    def delete(self, artifact_id: Union[int, str]) -> Any:
        return self.client.call("artifact-delete", path_params={"id": artifact_id})
