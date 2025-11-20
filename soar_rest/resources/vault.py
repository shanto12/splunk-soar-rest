from __future__ import annotations

from typing import Any, Dict, Optional, Union

from .base import Resource


class Vault(Resource):
    def list(self, *, params: Optional[Dict[str, Any]] = None) -> Any:
        return self.client.call("vault-list", params=params)

    def get(self, document_id: Union[int, str]) -> Any:
        return self.client.call("vault-detail", path_params={"id": document_id})
