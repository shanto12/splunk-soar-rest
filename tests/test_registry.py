import unittest

from soar_rest.endpoints import EndpointRegistry


class RegistryTests(unittest.TestCase):
    def test_loads_default(self):
        registry = EndpointRegistry.load_default()
        self.assertGreater(len(registry.names()), 5)
        self.assertIn("containers-list", registry.names())

    def test_render(self):
        registry = EndpointRegistry.load_default()
        ep = registry.get("container-detail")
        path = ep.render({"id": 1})
        self.assertEqual("/rest/container/1", path)


if __name__ == "__main__":
    unittest.main()
