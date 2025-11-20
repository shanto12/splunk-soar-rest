from __future__ import annotations

from typing import Any, Dict, Iterable, Optional, Union

from ..models import Container
from .base import Resource


class Containers(Resource):
    def list(self, *, params: Optional[Dict[str, Any]] = None) -> Any:
        return self.client.call("containers-list", params=params)

    def iterate(
        self, *, params: Optional[Dict[str, Any]] = None, page_size: int = 100, limit: Optional[int] = None
    ) -> Iterable[Any]:
        return self.client.paginate("/rest/container", params=params, page_size=page_size, limit=limit)

    def get(self, container_id: Union[int, str]) -> Any:
        return self.client.call("container-detail", path_params={"id": container_id})

    def create(self, container: Union[Container, Dict[str, Any]]) -> Any:
        payload = container.to_payload() if isinstance(container, Container) else container
        return self.client.call("container-create", json=payload)

    def bulk_create(self, containers: Iterable[Union[Container, Dict[str, Any]]]) -> Any:
        payload = [c.to_payload() if isinstance(c, Container) else c for c in containers]
        return self.client.call("container-create", json=payload)

    def update(self, container_id: Union[int, str], payload: Dict[str, Any]) -> Any:
        return self.client.call("container-update", path_params={"id": container_id}, json=payload)

    def delete(self, container_id: Union[int, str]) -> Any:
        return self.client.call("container-delete", path_params={"id": container_id})
