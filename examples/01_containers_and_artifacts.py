"""Example of listing containers and artifacts via the Splunk SOAR REST API."""

from splunk_soar_rest import SOARClient

BASE_URL = "https://soar.example.com"
TOKEN = "YOUR_PHANTOM_TOKEN"

client = SOARClient(BASE_URL, TOKEN)

# List the first 10 containers
containers = client.get("/rest/container?page_size=10")
print("Containers:", containers)

# Fetch artifacts for container with ID 1
artifacts = client.get("/rest/container/1/artifact")
print("Artifacts for container 1:", artifacts)
