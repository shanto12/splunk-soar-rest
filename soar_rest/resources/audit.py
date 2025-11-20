from __future__ import annotations

from typing import Any, Dict, Optional

from .base import Resource


class Audit(Resource):
    def search(self, *, params: Optional[Dict[str, Any]] = None) -> Any:
        """Search audit records using query params (user, role, playbook, container, tenant, etc.)."""
        return self.client.call("audit", params=params)
