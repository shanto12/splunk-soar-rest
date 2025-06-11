import unittest
from unittest.mock import MagicMock, patch
import json

from splunk_soar_rest import SplunkSOARClient, SplunkSOARError

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
        self.client._get = MagicMock(return_value={"r":"ok"})
        self.client._post = MagicMock(return_value={"r":"ok"})
        self.client._delete = MagicMock(return_value={"r":"ok"})

    def test_container_methods(self):
        self.client.create_container(name="n")
        self.client._post.assert_called_with("container", json_data={"name":"n"})
        self.client.get_container(1)
        self.client._get.assert_called_with("container/1")
        self.client.update_container(1, severity="high")
        self.client._post.assert_called_with("container/1", json_data={"severity":"high"})
        self.client.delete_container(1)
        self.client._delete.assert_called_with("container/1")
        self.client.add_container_comment(1, "c")
        self.client._post.assert_called_with("container_comment", json_data={"container_id":1,"comment":"c"})

