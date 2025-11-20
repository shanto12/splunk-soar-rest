import os
import unittest

import time

from soar_rest.client import AuthConfig, SoarClient
from soar_rest.resources import (
    Containers,
    System,
    Artifacts,
    Notes,
    EvidenceResource,
    Indicators,
    Vault,
)
from soar_rest.models import Container as ContainerModel, Artifact as ArtifactModel, Note, Evidence


SERVER = os.getenv("SOAR_SERVER")
TOKEN = os.getenv("SOAR_PH_AUTH_TOKEN")
VERIFY = os.getenv("SOAR_VERIFY_SSL", "True").lower() not in {"0", "false", "no"}


@unittest.skipUnless(SERVER and TOKEN, "Integration env vars not set")
class IntegrationSmokeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        auth = AuthConfig(ph_auth_token=TOKEN)
        cls.client = SoarClient(SERVER, auth=auth, verify=VERIFY, timeout=15)
        cls.created_container_id = None

    def test_info(self):
        system = System(self.client)
        data = system.info()
        self.assertIsInstance(data, dict)
        self.assertTrue("machine_id" in data or "version" in data)

    def test_containers_list_small(self):
        containers = Containers(self.client)
        data = containers.list(params={"page_size": 1, "page": 0})
        self.assertIsInstance(data, dict)

    def test_container_artifact_note_evidence_cycle(self):
        # Create container
        containers = Containers(self.client)
        unique_name = f"codex-auto-{int(time.time())}"
        c_payload = ContainerModel(name=unique_name, label="events", severity="medium")
        c_resp = containers.create(c_payload)
        self.assertIn("id", c_resp)
        self.__class__.created_container_id = c_resp["id"]

        # Create artifact on container
        artifacts = Artifacts(self.client)
        a_payload = ArtifactModel(
            container_id=c_resp["id"],
            name="auto-ip",
            cef={"sourceAddress": "1.1.1.1"},
            label="event",
        )
        a_resp = artifacts.create(a_payload)
        self.assertIn("id", a_resp)

        # Create note
        notes = Notes(self.client)
        n_payload = Note(container_id=c_resp["id"], content="automated note", title="codex")
        n_resp = notes.create(n_payload)
        self.assertIn("id", n_resp)

        # Create evidence linked to artifact
        evidence = EvidenceResource(self.client)
        e_payload = Evidence(container_id=c_resp["id"], content="auto evidence", content_type="artifact", object_id=a_resp["id"])
        e_resp = evidence.create(e_payload)
        self.assertIn("id", e_resp)

    def test_indicators_list(self):
        indicators = Indicators(self.client)
        data = indicators.list(params={"page_size": 1, "page": 0})
        self.assertIsInstance(data, dict)

    def test_vault_list(self):
        vault = Vault(self.client)
        data = vault.list(params={"page_size": 1, "page": 0})
        self.assertIsInstance(data, dict)


if __name__ == "__main__":
    unittest.main()
