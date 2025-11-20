from __future__ import annotations

from typing import Any, Dict, Optional, Union

from .base import Resource


class Users(Resource):
    def list(self, *, params: Optional[Dict[str, Any]] = None) -> Any:
        return self.client.call("users", params=params)

    def get(self, user_id: Union[int, str]) -> Any:
        return self.client.call("user-detail", path_params={"id": user_id})

    def tokens(self, user_id: Union[int, str]) -> Any:
        return self.client.call("user-token", path_params={"id": user_id})

    def roles(self) -> Any:
        return self.client.call("roles")

    def role(self, role_id: Union[int, str]) -> Any:
        return self.client.call("role-detail", path_params={"id": role_id})

    def tenants(self) -> Any:
        return self.client.call("tenants")

    def tenant(self, tenant_id: Union[int, str]) -> Any:
        return self.client.call("tenant-detail", path_params={"id": tenant_id})
