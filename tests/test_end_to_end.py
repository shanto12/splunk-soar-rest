import os
import unittest
from splunk_soar_rest import SplunkSOARClient, SplunkSOARError

SOAR_URL = os.getenv("SOAR_URL")
AUTH_TOKEN = os.getenv("SOAR_TOKEN")

class TestEndToEnd(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not SOAR_URL or not AUTH_TOKEN:
            raise unittest.SkipTest("SOAR_URL and SOAR_TOKEN must be set")
        cls.client = SplunkSOARClient(base_url=SOAR_URL, auth_token=AUTH_TOKEN, verify=False)
        cls.container_id = None
        cls.artifact_id = None
        cls.note_id = None

    def test_01_version_system_info(self):
        version = self.client.get_version()
        self.assertIn("version", version)
        info = self.client.get_system_info()
        self.assertIn("time_zone", info)

    def test_02_container_lifecycle(self):
        data = {"name": "Test Container", "label": "events", "severity": "low"}
        container = self.client.create_container(**data)
        self.__class__.container_id = container["id"]
        retrieved = self.client.get_container(self.container_id)
        self.assertEqual(retrieved["name"], data["name"])

        retrieved = self.client.get_container(self.container_id)
        self.assertEqual(retrieved["name"], data["name"])

        self.client.update_container(self.container_id, severity="medium")
        retrieved = self.client.get_container(self.container_id)
        self.assertEqual(retrieved["severity"], "medium")

        comment = self.client.add_container_comment(self.container_id, "Automated test comment")
        self.assertTrue(comment.get("success"))

        note = self.client.create_note(container_id=self.container_id, note_type="general", title="Test Note", content="Body")
        self.__class__.note_id = note["id"]
        fetched = self.client.get_note(self.note_id)
        self.assertEqual(fetched["container"], self.container_id)

        artifact = self.client.create_artifact(container_id=self.container_id, label="event", name="Test Artifact", cef={"foo":"bar"})
        self.__class__.artifact_id = artifact["id"]
        fetched_art = self.client.get_artifact(self.artifact_id)
        self.assertEqual(fetched_art["container"], self.container_id)

        arts = self.client.get_artifacts(params={"_filter_container_id": self.container_id})
        self.assertGreaterEqual(len(arts["data"]), 1)

    def test_03_cleanup(self):
        if not self.container_id:
            self.skipTest("Container not created")
        with self.assertRaises(SplunkSOARError) as cm:
            self.client.delete_container(self.container_id)
        self.assertEqual(cm.exception.status_code, 403)

if __name__ == "__main__":
    unittest.main()

