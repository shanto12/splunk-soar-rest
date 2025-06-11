# splunk_soar_rest/__init__.py

import requests
import json
import base64
import warnings

class SplunkSOARError(Exception):
    """Custom exception for Splunk SOAR API errors."""
    def __init__(self, message, status_code=None, response_text=None):
        super().__init__(message)
        self.status_code = status_code
        self.response_text = response_text

    def __str__(self):
        return f"{super().__str__()} (Status Code: {self.status_code}): {self.response_text}"

class SplunkSOARClient:
    """A Python client for the Splunk SOAR REST API."""

    def __init__(self, base_url, username=None, password=None, auth_token=None, verify=True):
        """
        Initializes the Splunk SOAR Client.

        Args:
            base_url (str): The base URL of the Splunk SOAR instance (e.g., https://soar.example.com).
            username (str, optional): Username for basic authentication.
            password (str, optional): Password for basic authentication.
            auth_token (str, optional): Automation token for ph-auth-token header authentication.
            verify (bool, optional): Whether to verify SSL certificates. Defaults to True.
        """
        if not base_url:
            raise ValueError("base_url must be provided.")
        
        self.base_url = base_url.rstrip('/')
        self.verify = verify
        
        self.session = requests.Session()
        self.session.verify = self.verify
        
        if auth_token:
            self.session.headers.update({"ph-auth-token": auth_token})
        elif username and password:
            self.session.auth = (username, password)
        else:
            raise ValueError("Either auth_token or username/password must be provided.")

        if not self.verify:
            warnings.filterwarnings("ignore", "Unverified HTTPS request")

    def _build_url(self, endpoint):
        return f"{self.base_url}/rest/{endpoint}"

    def _handle_response(self, response):
        """Checks response status and returns JSON or raises an error."""
        if response.ok:
            try:
                if response.status_code == 204: return None
                return response.json()
            except json.JSONDecodeError:
                return response.content
        else:
            raise SplunkSOARError(f"API call to {response.url} failed", response.status_code, response.text)

    def _get(self, endpoint, params=None):
        return self._handle_response(self.session.get(self._build_url(endpoint), params=params))

    def _post(self, endpoint, json_data=None):
        return self._handle_response(self.session.post(self._build_url(endpoint), json=json_data))

    def _delete(self, endpoint):
        return self._handle_response(self.session.delete(self._build_url(endpoint)))

    # --- Generic Querying (p.11) ---
    def query(self, endpoint, params=None):
        """Generic GET method for any endpoint."""
        return self._get(endpoint, params=params)

    # --- System Info Endpoints (p.19) ---
    def get_version(self):
        """Gets the Splunk SOAR product version."""
        return self._get("version")

    def get_system_info(self):
        """Gets the system timezone and base URL."""
        return self._get("system_info")

    def get_license(self):
        """Gets license configuration and usage."""
        return self._get("license")

    def upload_license(self, license_string):
        """Automates loading a Splunk SOAR license."""
        return self._post("license", json_data={"license": license_string})

    # --- Administration Endpoints (p.55) ---
    def get_indicator_cef_filters(self, params=None):
        return self._get("indicator_cef_filter", params=params)

    def update_indicator_cef_filter(self, filter_id, apply_filter):
        return self._post(f"indicator_cef_filter/{filter_id}", json_data={"apply_filter": apply_filter})

    # --- App Endpoints (p.61) ---
    def get_apps(self, params=None):
        return self._get("app", params=params)
    
    def get_app(self, app_id):
        return self._get(f"app/{app_id}")

    def install_app_from_path(self, app_path):
        """Installs an app from a local file path."""
        with open(app_path, 'rb') as f:
            encoded_contents = base64.b64encode(f.read()).decode('utf-8')
        return self._post("app", json_data={"app": encoded_contents})

    def delete_app(self, app_id):
        return self._delete(f"app/{app_id}")

    # --- Artifact Endpoints (p.72) ---
    def get_artifacts(self, params=None):
        return self._get("artifact", params=params)

    def create_artifact(self, **kwargs):
        return self._post("artifact", json_data=kwargs)
        
    def get_artifact(self, artifact_id):
        return self._get(f"artifact/{artifact_id}")

    def update_artifact(self, artifact_id, **kwargs):
        return self._post(f"artifact/{artifact_id}", json_data=kwargs)
        
    def delete_artifact(self, artifact_id):
        return self._delete(f"artifact/{artifact_id}")

    # --- Asset Endpoints (p.78) ---
    def get_assets(self, params=None):
        return self._get("asset", params=params)

    def create_asset(self, **kwargs):
        return self._post("asset", json_data=kwargs)
        
    def update_asset(self, asset_id, **kwargs):
        return self._post(f"asset/{asset_id}", json_data=kwargs)
        
    def delete_asset(self, asset_id):
        return self._delete(f"asset/{asset_id}")

    # --- Audit Endpoints (p.82) ---
    def get_audit_events(self, params=None):
        return self._get("audit", params=params)

    def get_user_audit(self, user_id, params=None):
        return self._get(f"ph_user/{user_id}/audit", params=params)

    def get_role_audit(self, role_id, params=None):
        return self._get(f"role/{role_id}/audit", params=params)

    def get_playbook_audit(self, playbook_id, params=None):
        return self._get(f"playbook/{playbook_id}/audit", params=params)

    def get_container_audit(self, container_id, params=None):
        return self._get(f"container/{container_id}/audit", params=params)

    # --- CEF Endpoints (p.99) ---
    def get_cefs(self, params=None):
        return self._get("cef", params=params)

    def create_cef(self, name, data_type):
        return self._post("cef", json_data={"name": name, "data_type": data_type})

    def update_cef(self, cef_id, name, data_type):
        return self._post(f"cef/{cef_id}", json_data={"name": name, "data_type": data_type})

    def delete_cef(self, cef_id):
        return self._delete(f"cef/{cef_id}")

    # --- Container Endpoints (p.105) ---
    def get_containers(self, params=None):
        return self._get("container", params=params)

    def create_container(self, **kwargs):
        return self._post("container", json_data=kwargs)
        
    def get_container(self, container_id):
        return self._get(f"container/{container_id}")

    def update_container(self, container_id, **kwargs):
        return self._post(f"container/{container_id}", json_data=kwargs)
        
    def delete_container(self, container_id):
        return self._delete(f"container/{container_id}")

    def add_container_comment(self, container_id, comment):
        return self._post("container_comment", json_data={"container_id": container_id, "comment": comment})
        
    def add_container_attachment_from_path(self, container_id, file_path, file_name, metadata=None):
        with open(file_path, 'rb') as f:
            file_content = base64.b64encode(f.read()).decode('utf-8')
        data = {"container_id": container_id, "file_name": file_name, "file_content": file_content, "metadata": metadata or {"contains": ["vault id"]}}
        return self._post("container_attachment", json_data=data)

    # --- Evidence Endpoints (p.130) ---
    def add_evidence(self, container_id, object_id, content_type):
        return self._post("evidence", json_data={"container_id": container_id, "object_id": object_id, "content_type": content_type})
        
    def get_evidence(self, params=None):
        return self._get("evidence", params=params)
        
    def delete_evidence(self, evidence_id):
        return self._delete(f"evidence/{evidence_id}")

    # --- HUD (Heads Up Display) Endpoints (p.136) ---
    def create_pin_template(self, **kwargs):
        return self._post("container_pin_settings", json_data=kwargs)
        
    def add_pin_to_container(self, **kwargs):
        return self._post("container_pin", json_data=kwargs)

    # --- Notes Endpoints (p.152) ---
    def create_note(self, **kwargs):
        return self._post("note", json_data=kwargs)
    
    def get_notes(self, params=None):
        return self._get("note", params=params)
        
    def get_note(self, note_id):
        return self._get(f"note/{note_id}")
        
    def delete_note(self, note_id):
        return self._delete(f"note/{note_id}")

    # --- Playbook Endpoints (p.166) ---
    def get_playbook(self, playbook_id):
        """Retrieves a specific playbook by its ID as a gzipped file."""
        return self._get(f"playbook/{playbook_id}")

    def run_playbook(self, **kwargs):
        """Runs a playbook against a container."""
        return self._post("playbook_run", json_data=kwargs)

    def get_playbook_run(self, run_id):
        """Checks the status of a playbook run."""
        return self._get(f"playbook_run/{run_id}")

    # --- Role Management Endpoints (p.174) ---
    def get_roles(self, params=None):
        return self._get("role", params=params)

    def create_role(self, **kwargs):
        return self._post("role", json_data=kwargs)
        
    def get_role(self, role_id):
        return self._get(f"role/{role_id}")
        
    def update_role(self, role_id, **kwargs):
        return self._post(f"role/{role_id}", json_data=kwargs)
        
    def delete_role(self, role_id):
        return self._delete(f"role/{role_id}")
        
    # --- Action Run Endpoints (p.178) ---
    def run_action(self, **kwargs):
        return self._post("action_run", json_data=kwargs)
        
    def get_action_run(self, run_id):
        return self._get(f"action_run/{run_id}")
        
    def cancel_action_run(self, run_id):
        return self._post(f"action_run/{run_id}", json_data={"cancel": True})
        
    def get_app_runs_for_action(self, action_run_id, params=None):
        return self._get(f"action_run/{action_run_id}/app_runs", params=params)

    # --- Severity Endpoints (p.192) ---
    def get_severities(self, params=None):
        return self._get("severity", params=params)

    def create_severity(self, **kwargs):
        return self._post("severity", json_data=kwargs)

    def update_severity(self, severity_id, **kwargs):
        return self._post(f"severity/{severity_id}", json_data=kwargs)
        
    # --- Status Endpoints (p.197) ---
    def get_container_statuses(self, params=None):
        return self._get("container_status", params=params)

    def create_container_status(self, name, status_type, is_default=False):
        return self._post("container_status", json_data={"name": name, "status_type": status_type, "is_default": is_default})

    def delete_container_status(self, status_id):
        return self._delete(f"container_status/{status_id}")

    # --- System Settings Endpoints (p.202) ---
    def update_system_settings(self, auth_settings):
        """Replaces the entire authentication provider configuration."""
        return self._post("system_settings", json_data={"auth_settings": auth_settings})
        
    def update_system_labels(self, add_label=None, remove_label=None, label_name=None):
        data = {}
        if add_label: data['add_label'] = True
        if remove_label: data['remove_label'] = True
        if label_name: data['label_name'] = label_name
        return self._post("system_settings/events", json_data=data)

    # --- User Management Endpoints (p.212) ---
    def get_users(self, params=None):
        return self._get("ph_user", params=params)

    def create_user(self, **kwargs):
        return self._post("ph_user", json_data=kwargs)

    def get_user(self, user_id):
        return self._get(f"ph_user/{user_id}")

    def update_user(self, user_id, **kwargs):
        return self._post(f"ph_user/{user_id}", json_data=kwargs)

    def delete_user(self, user_id):
        return self._delete(f"ph_user/{user_id}")
        
    def get_user_token(self, user_id):
        return self._get(f"ph_user/{user_id}/token")
        
    # --- User Settings Endpoints (p.218) ---
    def get_user_settings(self):
        """Gets settings for the current user."""
        return self._get("user_settings")
        
    def update_user_settings(self, **kwargs):
        """Updates settings for the current user."""
        return self._post("user_settings", json_data=kwargs)

    # --- Search Endpoints (p.221) ---
    def search(self, query, categories=None, tenant=None, params=None):
        search_params = params or {}
        search_params['query'] = query
        if categories: search_params['categories'] = categories
        if tenant: search_params['tenant'] = tenant
        return self._get("search", params=search_params)
        
    # --- Vault Endpoints (p.223) ---
    def get_vault_documents(self, params=None):
        return self._get("vault_document", params=params)

    def get_vault_document(self, vault_id):
        return self._get(f"vault_document/{vault_id}")

    # --- Workbook Endpoints (p.226) ---
    def get_workbook_tasks(self, params=None):
        return self._get("workbook_task", params=params)
        
    def create_workbook_template(self, **kwargs):
        return self._post("workbook_template", json_data=kwargs)
        
    def add_phase_to_workbook(self, **kwargs):
        return self._post("workbook_phase_template", json_data=kwargs)
        
    def get_workbook_phases(self, template_id):
        return self._get("workbook_phase_template", params={"_filter_template": template_id})
        
    def add_task_to_workbook_phase(self, **kwargs):
        return self._post("workbook_task_template", json_data=kwargs)
