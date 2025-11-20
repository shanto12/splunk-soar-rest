from __future__ import annotations

from typing import Any, Dict, Optional, Union

from ..models import Evidence, Note
from .base import Resource


class Notes(Resource):
    def list(self, *, params: Optional[Dict[str, Any]] = None) -> Any:
        return self.client.call("notes-list", params=params)

    def create(self, note: Union[Note, Dict[str, Any]]) -> Any:
        payload = note.to_payload() if isinstance(note, Note) else note
        return self.client.call("note-create", json=payload)


class EvidenceResource(Resource):
    def list(self, *, params: Optional[Dict[str, Any]] = None) -> Any:
        return self.client.call("evidence-list", params=params)

    def create(self, evidence: Union[Evidence, Dict[str, Any]]) -> Any:
        payload = evidence.to_payload() if isinstance(evidence, Evidence) else evidence
        return self.client.call("evidence-create", json=payload)
