import requests
import json
import base64

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
            requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

    def _build_url(self, endpoint):
        return f"{self.base_url}/rest/{endpoint}"

    def _handle_response(self, response):
        """Checks response status and returns JSON or raises an error."""
        if response.ok:
            try:
                # Handle empty responses for success codes like 204
                if response.status_code == 204:
                    return None
                return response.json()
            except json.JSONDecodeError:
                return response.content
        else:
            raise SplunkSOARError(
                f"API call to {response.url} failed",
                status_code=response.status_code,
                response_text=response.text
            )

    def _get(self, endpoint, params=None):
        url = self._build_url(endpoint)
        response = self.session.get(url, params=params)
        return self._handle_response(response)

    def _post(self, endpoint, json_data=None, files=None):
        url = self._build_url(endpoint)
        response = self.session.post(url, json=json_data, files=files)
        return self._handle_response(response)

    def _delete(self, endpoint):
        url = self._build_url(endpoint)
        response = self.session.delete(url)
        return self._handle_response(response)

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

    def get_health(self):
        """Gets memory/CPU usage for services."""
        return self._get("health")
        
    def get_app_status(self, params=None):
        """Gets test connectivity status for each asset."""
        return self._get("app_status", params=params)
        
    def get_widget_data(self, widget_name, params=None):
        """Gets data used to populate a specific home page widget."""
        return self._get(f"widget_data/{widget_name}", params=params)

    # --- Administration Endpoints (p.59) ---
    def get_indicator_cef_filters(self, params=None):
        """Lists all indicator_cef_filter records."""
        return self._get("indicator_cef_filter", params=params)

    def get_indicator_cef_filter(self, filter_id):
        """Gets a particular indicator_cef_filter record by ID."""
        return self._get(f"indicator_cef_filter/{filter_id}")

    def update_indicator_cef_filter(self, filter_id, apply_filter):
        """Updates the apply_filter status of an indicator CEF filter."""
        return self._post(f"indicator_cef_filter/{filter_id}", json_data={"apply_filter": apply_filter})

    # --- Aggregation Rules Endpoints (p.62) ---
    def create_aggregation_rule(self, **kwargs):
        """Creates an aggregation rule."""
        return self._post("aggregation_rule", json_data=kwargs)

    def update_aggregation_rule(self, rule_id, **kwargs):
        """Updates an existing aggregation rule."""
        kwargs['id'] = rule_id
        return self._post("aggregation_rule", json_data=kwargs)

    # --- App Endpoints (p.65) ---
    def get_apps(self, params=None):
        """Gets a list of installed apps."""
        return self._get("app", params=params)
    
    def get_app(self, app_id):
        """Gets details for a specific app."""
        return self._get(f"app/{app_id}")

    def install_app(self, app_path):
        """Installs a Splunk SOAR app from a tarball or .rpm file."""
        with open(app_path, 'rb') as f:
            encoded_contents = base64.b64encode(f.read()).decode('utf-8')
        return self._post("app", json_data={"app": encoded_contents})

    def delete_app(self, app_id):
        """Deletes/uninstalls an app."""
        return self._delete(f"app/{app_id}")

    # --- Approval Endpoints (p.69) ---
    def get_approvals(self, params=None):
        """Lists all approvals."""
        return self._get("approval", params=params)
        
    def get_approval(self, approval_id):
        """Gets the data of one approval."""
        return self._get(f"approval/{approval_id}")

    def get_approval_summary(self, approval_id):
        """Lists details of approvals for a particular container."""
        return self._get(f"approval/{approval_id}/detail_summary_view")

    # --- Artifact Endpoints (p.76) ---
    def get_artifacts(self, params=None):
        """Gets a list of artifacts. Supports filtering and pagination."""
        return self._get("artifact", params=params)

    def create_artifact(self, **kwargs):
        """Creates a new artifact."""
        return self._post("artifact", json_data=kwargs)
        
    def get_artifact(self, artifact_id):
        """Gets details for a specific artifact."""
        return self._get(f"artifact/{artifact_id}")

    def update_artifact(self, artifact_id, **kwargs):
        """Updates an existing artifact."""
        return self._post(f"artifact/{artifact_id}", json_data=kwargs)
        
    def delete_artifact(self, artifact_id):
        """Deletes an artifact."""
        return self._delete(f"artifact/{artifact_id}")

    # --- Asset Endpoints (p.82) ---
    def get_assets(self, params=None):
        """Gets a list of assets."""
        return self._get("asset", params=params)

    def create_asset(self, **kwargs):
        """Creates a new asset."""
        return self._post("asset", json_data=kwargs)

    # --- Audit Endpoints (p.86) ---
    def get_audit_events(self, params=None):
        """Lists all audit events, with powerful filtering options."""
        return self._get("audit", params=params)

    # --- Container Endpoints (p.109) ---
    def get_containers(self, params=None):
        """Gets a list of containers."""
        return self._get("container", params=params)

    def create_container(self, **kwargs):
        """Creates a new container."""
        return self._post("container", json_data=kwargs)
        
    def get_container(self, container_id):
        """Gets details for a specific container."""
        return self._get(f"container/{container_id}")

    def update_container(self, container_id, **kwargs):
        """Updates an existing container."""
        return self._post(f"container/{container_id}", json_data=kwargs)
        
    def delete_container(self, container_id):
        """Deletes a container."""
        return self._delete(f"container/{container_id}")

    def get_container_permitted_users(self, container_id):
        """Gets a list of candidates who can be granted authorized user access."""
        return self._get(f"container/{container_id}/permitted_users")

    def add_container_comment(self, container_id, comment):
        """Adds a comment to a container."""
        data = {"container_id": container_id, "comment": comment}
        return self._post("container_comment", json_data=data)
        
    def add_container_attachment(self, container_id, file_name, file_path, metadata=None):
        """Attaches a file to a container."""
        with open(file_path, 'rb') as f:
            file_content = base64.b64encode(f.read()).decode('utf-8')
        data = {
            "container_id": container_id,
            "file_name": file_name,
            "file_content": file_content,
            "metadata": metadata or {"contains": ["vault id"]}
        }
        return self._post("container_attachment", json_data=data)

    # --- List Endpoints (p.152) ---
    def get_lists(self, params=None):
        """Gets all custom lists."""
        return self._get("decided_list", params=params)
        
    def create_list(self, name, content):
        """Creates a new custom list."""
        data = {"name": name, "content": content}
        return self._post("decided_list", json_data=data)
        
    def update_list(self, list_id_or_name, **kwargs):
        """Updates a list with append, delete, or update operations."""
        return self._post(f"decided_list/{list_id_or_name}", json_data=kwargs)
        
    def get_list_formatted_content(self, list_id_or_name, params=None):
        """Gets the contents of a list in a delimited format."""
        return self._get(f"decided_list/{list_id_or_name}/formatted_content", params=params)

    # --- Playbook Endpoints (p.170) ---
    def get_playbook(self, playbook_id):
        """Retrieves a specific playbook by its ID as a gzipped file."""
        return self._get(f"playbook/{playbook_id}")

    def import_playbook(self, playbook_path, scm_id, force=False):
        """Imports a playbook from a gzipped TAR file."""
        with open(playbook_path, 'rb') as f:
            playbook_b64 = base64.b64encode(f.read()).decode('utf-8')
        data = {"playbook": playbook_b64, "scm/scm_id": scm_id, "force": force}
        return self._post("import_playbook", json_data=data)

    def run_playbook(self, **kwargs):
        """Runs a playbook against a container."""
        return self._post("playbook_run", json_data=kwargs)

    def get_playbook_run(self, run_id):
        """Checks the status of a playbook run."""
        return self._get(f"playbook_run/{run_id}")

    # --- Role Management Endpoints (p.178) ---
    def get_roles(self, params=None):
        """Gets a list of roles."""
        return self._get("role", params=params)

    def create_role(self, **kwargs):
        """Creates a new role."""
        return self._post("role", json_data=kwargs)
        
    def get_role(self, role_id):
        """Gets details for a specific role."""
        return self._get(f"role/{role_id}")
        
    def update_role(self, role_id, **kwargs):
        """Updates a role."""
        return self._post(f"role/{role_id}", json_data=kwargs)
        
    def delete_role(self, role_id):
        """Deletes a role."""
        return self._delete(f"role/{role_id}")
        
    # --- Action Run Endpoints (p.182) ---
    def run_action(self, **kwargs):
        """Runs an action against a container."""
        return self._post("action_run", json_data=kwargs)
        
    def get_action_run(self, run_id):
        """Checks the status of an action run."""
        return self._get(f"action_run/{run_id}")
        
    def cancel_action_run(self, run_id):
        """Cancels a running action."""
        return self._post(f"action_run/{run_id}", json_data={"cancel": True})
        
    def get_app_runs_for_action(self, action_run_id):
        """Retrieve the app action results for a given action run."""
        return self._get(f"action_run/{action_run_id}/app_runs")
    
    # --- Feature Flag Endpoints (p.241) ---
    def get_feature_flags(self, params=None):
        """Gets a list of all feature flags."""
        return self._get("feature_flag", params=params)
        
    def get_feature_flag(self, flag_name):
        """Gets a specific feature flag by name."""
        return self._get(f"feature_flag/{flag_name}")
        
    def update_feature_flag(self, flag_name, **kwargs):
        """Turns a feature on/off or modifies its configuration."""
        return self._post(f"feature_flag/{flag_name}", json_data=kwargs)

    # --- Command Run Endpoints (p.239) ---
    def run_command(self, name, args):
        """Runs a system management command."""
        return self._post("command_run", json_data={"name": name, "args": args})
    
    def get_command_runs(self):
        """Gets the status of all command runs."""
        return self._get("command_run")
        
    def get_command_run(self, run_id):
        """Gets the status of a particular command run."""
        return self._get(f"command_run/{run_id}")
