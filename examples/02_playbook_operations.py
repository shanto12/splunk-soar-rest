import os
from splunk_soar_rest import SplunkSOARClient, SplunkSOARError

# --- Configuration ---
SOAR_URL = os.getenv("SOAR_URL", "https://your.soar.instance")
AUTH_TOKEN = os.getenv("SOAR_TOKEN", "your_ph_auth_token")

# !!! IMPORTANT: Replace with a valid container ID and playbook path from your instance !!!
CONTAINER_ID_TO_RUN_ON = 1
PLAYBOOK_ID_TO_RUN = "local/investigate" 

def main():
    """Demonstrates playbook operations."""
    if not AUTH_TOKEN or "your_ph_auth_token" in AUTH_TOKEN:
        print("Please set the SOAR_URL and SOAR_TOKEN environment variables.")
        return

    print("Initializing client...")
    client = SplunkSOARClient(base_url=SOAR_URL, auth_token=AUTH_TOKEN, verify=False)

    try:
        # --- Run a Playbook ---
        print(f"\n--- Running playbook '{PLAYBOOK_ID_TO_RUN}' on container {CONTAINER_ID_TO_RUN_ON} ---")
        playbook_run_data = {
            "container_id": CONTAINER_ID_TO_RUN_ON,
            "playbook_id": PLAYBOOK_ID_TO_RUN,
            "scope": "all",
            "run": True
        }
        run_response = client.run_playbook(**playbook_run_data)
        playbook_run_id = run_response['playbook_run_id']
        print(f"Playbook queued to run. Run ID: {playbook_run_id}")

        # --- Check Playbook Run Status ---
        print(f"\n--- Checking status of playbook run {playbook_run_id} ---")
        # In a real scenario, you would poll this endpoint until status is 'success' or 'failed'
        status_response = client.get_playbook_run(playbook_run_id)
        print(f"Status: {status_response['status']}")
        print(f"Message: {status_response.get('message', 'No message yet.')}")

    except SplunkSOARError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
