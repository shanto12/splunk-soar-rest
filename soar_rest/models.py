from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class Model(BaseModel):
    """Base model with a helper to dict without None."""

    def to_payload(self) -> Dict:
        return self.model_dump(exclude_none=True)


class Container(Model):
    name: str
    label: Optional[str] = None
    description: Optional[str] = None
    severity: Optional[str] = None
    status: Optional[str] = None
    owner: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    run_automation: bool = True
    source_data_identifier: Optional[str] = None


class Artifact(Model):
    container_id: int
    name: str
    cef: Dict
    label: Optional[str] = None
    source_data_identifier: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    severity: Optional[str] = None
    type: Optional[str] = None


class RunActionRequest(Model):
    action: str
    parameters: List[Dict]
    assets: List[str]
    name: Optional[str] = None
    callback: Optional[str] = None
    parent_name: Optional[str] = None
    container_id: Optional[int] = None


class RunPlaybookRequest(Model):
    playbook_id: Optional[int] = None
    playbook: Optional[str] = None
    container_id: int
    scope: Optional[str] = None  # e.g., all, new, custom
    inputs: Optional[Dict] = None
    run: bool = True


class Note(Model):
    container_id: int
    content: str
    note_type: str = "general"
    title: Optional[str] = None


class Evidence(Model):
    container_id: int
    content: str
    object_id: Optional[int] = None  # artifact/note/etc id
    content_type: Optional[str] = "artifact"
