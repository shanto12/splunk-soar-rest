import os
from splunk_soar_rest import SplunkSOARClient, SplunkSOARError

# --- Configuration ---
# Best practice: Use environment variables or a config file for credentials
SOAR_URL = os.getenv("SOAR_URL", "https://your.soar.instance")
AUTH_TOKEN = os.getenv("SOAR_TOKEN", "your_ph_auth_token")

def main():
    """Demonstrates container and artifact management."""
    if not AUTH_TOKEN or "your_ph_auth_token" in AUTH_TOKEN:
        print("Please set the SOAR_URL and SOAR_TOKEN environment variables.")
        return

    print("Initializing client...")
    client = SplunkSOARClient(base_url=SOAR_URL, auth_token=AUTH_TOKEN, verify=False)
    
    try:
        # --- Create Container ---
        print("\n--- Creating a new container ---")
        container_data = {
            "name": "API Test - Phishing Email Reported",
            "label": "events",
            "severity": "high",
            "owner_id": "admin"
        }
        new_container = client.create_container(**container_data)
        container_id = new_container['id']
        print(f"Container created with ID: {container_id}")

        # --- Add Artifacts ---
        print("\n--- Adding artifacts to the container ---")
        artifacts_to_add = [
            {"name": "Suspicious Sender", "cef": {"sourceAddress": "10.20.30.40"}, "container_id": container_id, "label": "event"},
            {"name": "Malicious URL", "cef": {"requestURL": "http://malicious-site.bad/login.php"}, "container_id": container_id, "label": "event"},
            {"name": "Malware Hash", "cef": {"fileHash": "d41d8cd98f00b204e9800998ecf8427e"}, "container_id": container_id, "label": "event"}
        ]
        for art_data in artifacts_to_add:
            client.create_artifact(**art_data)
            print(f"Added artifact: {art_data['name']}")
        
        # --- Retrieve and Display Container and its Artifacts ---
        print(f"\n--- Retrieving details for container {container_id} ---")
        retrieved_container = client.get_container(container_id)
        print(f"Retrieved Container Name: {retrieved_container['name']}")
        print(f"Artifact Count: {retrieved_container['artifact_count']}")
        
        print(f"\n--- Listing artifacts for container {container_id} ---")
        artifact_params = {"_filter_container_id": container_id, "page_size": 10}
        artifacts = client.get_artifacts(params=artifact_params)
        for artifact in artifacts['data']:
            print(f"  - Artifact ID: {artifact['id']}, Name: {artifact['name']}, CEF: {artifact.get('cef')}")

    except SplunkSOARError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
