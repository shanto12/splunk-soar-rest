from __future__ import annotations

from typing import Any

from .base import Resource


class System(Resource):
    def info(self) -> Any:
        # Cloud instances expose /rest/system_info (not /rest/info)
        return self.client.call("system-info")

    def system_info(self) -> Any:
        return self.client.call("system-info")

    def status(self) -> Any:
        return self.client.call("status")

    def severity(self) -> Any:
        return self.client.call("severity")

    def feature_flags(self) -> Any:
        return self.client.call("feature-flags")

    def hud_config(self) -> Any:
        return self.client.call("hud-config")
