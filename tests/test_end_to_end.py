import os
import unittest
import json
from unittest.mock import MagicMock, patch
from splunk_soar_rest import SplunkSOARClient, SplunkSOARError

SOAR_URL = os.getenv("SOAR_URL")
AUTH_TOKEN = os.getenv("SOAR_TOKEN")

class TestClientBasics(unittest.TestCase):
    def test_init_missing_base_url(self):
        with self.assertRaises(ValueError):
            SplunkSOARClient(base_url=None, auth_token="t")

    def test_init_missing_credentials(self):
        with self.assertRaises(ValueError):
            SplunkSOARClient(base_url="https://soar", verify=False)

    def test_build_url(self):
        client = SplunkSOARClient(base_url="https://soar/", auth_token="t")
        self.assertEqual(client._build_url("test"), "https://soar/rest/test")

    @patch("splunk_soar_rest.requests.Session")
    def test_get_post_delete(self, mock_session_cls):
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.json.return_value = {"ok": True}
        mock_session.get.return_value = mock_response
        mock_session.post.return_value = mock_response
        mock_session.delete.return_value = mock_response
        mock_session_cls.return_value = mock_session

        client = SplunkSOARClient(base_url="https://soar", auth_token="t")
        self.assertEqual(client._get("foo"), {"ok": True})
        mock_session.get.assert_called_with("https://soar/rest/foo", params=None)

        self.assertEqual(client._post("bar", json_data={"a":1}), {"ok": True})
        mock_session.post.assert_called_with("https://soar/rest/bar", json={"a":1})

        self.assertEqual(client._delete("baz"), {"ok": True})
        mock_session.delete.assert_called_with("https://soar/rest/baz")

class TestHandleResponse(unittest.TestCase):
    def setUp(self):
        self.client = SplunkSOARClient(base_url="https://soar", auth_token="t")

    def test_handle_json(self):
        resp = MagicMock()
        resp.ok = True
        resp.status_code = 200
        resp.json.return_value = {"x": 1}
        self.assertEqual(self.client._handle_response(resp), {"x": 1})

    def test_handle_no_content(self):
        resp = MagicMock()
        resp.ok = True
        resp.status_code = 204
        self.assertIsNone(self.client._handle_response(resp))

    def test_handle_invalid_json(self):
        resp = MagicMock()
        resp.ok = True
        resp.status_code = 200
        resp.json.side_effect = json.JSONDecodeError("bad", "", 0)
        resp.content = b"binary"
        self.assertEqual(self.client._handle_response(resp), b"binary")

    def test_handle_error(self):
        resp = MagicMock()
        resp.ok = False
        resp.url = "u"
        resp.status_code = 400
        resp.text = "bad"
        with self.assertRaises(SplunkSOARError) as cm:
            self.client._handle_response(resp)
        self.assertEqual(cm.exception.status_code, 400)
        self.assertEqual(cm.exception.response_text, "bad")

class TestEndpointWrappers(unittest.TestCase):
    def setUp(self):
        self.client = SplunkSOARClient(base_url="https://soar", auth_token="t")
        self.client._get = MagicMock(return_value={"r": "ok"})
        self.client._post = MagicMock(return_value={"r": "ok"})
        self.client._delete = MagicMock(return_value={"r": "ok"})

    def test_container_methods(self):
        self.client.create_container(name="n")
        self.client._post.assert_called_with("container", json_data={"name": "n"})
        self.client.get_container(1)
        self.client._get.assert_called_with("container/1")
        self.client.update_container(1, severity="high")
        self.client._post.assert_called_with("container/1", json_data={"severity": "high"})
        self.client.delete_container(1)
        self.client._delete.assert_called_with("container/1")
        self.client.add_container_comment(1, "c")
        self.client._post.assert_called_with("container_comment", json_data={"container_id": 1, "comment": "c"})

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

