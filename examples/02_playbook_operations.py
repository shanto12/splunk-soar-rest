"""Example of interacting with playbooks via the Splunk SOAR REST API."""

from splunk_soar_rest import SOARClient

BASE_URL = "https://soar.example.com"
TOKEN = "YOUR_PHANTOM_TOKEN"

client = SOARClient(BASE_URL, TOKEN)

# List playbooks
playbooks = client.get("/rest/playbook")
print("Playbooks:", playbooks)

# Run a playbook with ID 1 against container 1
run_response = client.post("/rest/playbook_run", json={"playbook_id": 1, "container_id": 1})
print("Playbook run response:", run_response)
