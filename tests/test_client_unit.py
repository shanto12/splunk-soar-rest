import json
import types
import unittest
from unittest.mock import patch

from soar_rest.client import AuthConfig, SoarClient
from soar_rest.errors import SoarError


class FakeResponse:
    def __init__(self, status_code=200, payload=None, headers=None):
        self.status_code = status_code
        self.headers = headers or {"Content-Type": "application/json"}
        self._payload = payload
        self.text = json.dumps(payload or {})
        self.content = self.text.encode()

    def json(self):
        return self._payload


class ClientTests(unittest.TestCase):
    def test_builds_urls(self):
        client = SoarClient("https://example", auth=AuthConfig(username="u", password="p"))
        url = client._build_url("/rest/info")
        self.assertEqual("https://example/rest/info", url)

    def test_request_success(self):
        client = SoarClient("https://example", auth=AuthConfig(username="u", password="p"))
        with patch.object(client.session, "request", return_value=FakeResponse(payload={"ok": True})) as mock_req:
            resp = client.get("/rest/info")
            self.assertEqual({"ok": True}, resp)
            mock_req.assert_called_once()

    def test_request_error_raises(self):
        client = SoarClient("https://example", auth=AuthConfig(username="u", password="p"))
        with patch.object(client.session, "request", return_value=FakeResponse(status_code=500, payload={"error": "x"})):
            with self.assertRaises(SoarError):
                client.get("/rest/info")


if __name__ == "__main__":
    unittest.main()
