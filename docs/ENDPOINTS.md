# Covered REST endpoints (curated)

Total: 67

| Name | Method | Path | Description |
| --- | --- | --- | --- |
| system-info | GET | `/rest/system_info` | System info (license, version, uptime). |
| status | GET | `/rest/status` | System status and configuration (may not be available on Cloud). |
| severity | GET | `/rest/severity` | List severity values. |
| feature-flags | GET | `/rest/feature_flag` | Enabled feature flags. |
| hud-config | GET | `/rest/hud_config` | HUD configuration and widget metadata. |
| containers-list | GET | `/rest/container` | List containers with filters and pagination. |
| container-detail | GET | `/rest/container/{id}` | Get a specific container by id. |
| container-create | POST | `/rest/container` | Create one or more containers. |
| container-update | POST | `/rest/container/{id}` | Update an existing container. |
| container-delete | DELETE | `/rest/container/{id}` | Delete a container. |
| artifacts-list | GET | `/rest/artifact` | List artifacts with filters. |
| artifact-detail | GET | `/rest/artifact/{id}` | Get artifact by id. |
| artifact-create | POST | `/rest/artifact` | Create an artifact. |
| artifact-delete | DELETE | `/rest/artifact/{id}` | Delete an artifact. |
| evidence-list | GET | `/rest/evidence` | List evidence records. |
| evidence-create | POST | `/rest/evidence` | Create evidence associated with a container or artifact. |
| notes-list | GET | `/rest/note` | List notes. |
| note-create | POST | `/rest/note` | Create a note on a container. |
| approvals-list | GET | `/rest/approval` | List approvals. |
| approval-detail | GET | `/rest/approval/{id}` | Get approval detail. |
| approval-create | POST | `/rest/approval` | Create an approval request. |
| approval-update | POST | `/rest/approval/{id}` | Update an approval (status/decision). |
| approval-summary | GET | `/rest/approval/{id}/detail_summary_view` | Summary view of an approval. |
| run-action | POST | `/rest/run_action` | Trigger an action on one or more assets. |
| action-run-detail | GET | `/rest/action_run/{id}` | Inspect an action run. |
| action-run-app-runs | GET | `/rest/action_run/{id}/app_runs` | List app runs for a given action run. |
| run-playbook | POST | `/rest/run_playbook` | Trigger a playbook on a container/scope. |
| playbooks-list | GET | `/rest/playbook` | List playbooks. |
| playbook-detail | GET | `/rest/playbook/{id}` | Get a specific playbook’s metadata. |
| playbook-update | POST | `/rest/playbook/{id}` | Update a playbook (enable/disable/labels). |
| custom-functions | GET | `/rest/custom_function` | List custom functions. |
| custom-function-detail | GET | `/rest/custom_function/{id}` | Get a custom function. |
| assets-list | GET | `/rest/asset` | List configured assets. |
| asset-detail | GET | `/rest/asset/{id}` | Get asset configuration. |
| asset-create | POST | `/rest/asset` | Create an asset. |
| asset-update | POST | `/rest/asset/{id}` | Update an asset. |
| asset-delete | DELETE | `/rest/asset/{id}` | Delete an asset. |
| apps-list | GET | `/rest/app` | List apps installed on the cluster. |
| app-detail | GET | `/rest/app/{id}` | App metadata. |
| app-status | GET | `/rest/app_status` | App runtime status. |
| app-run | GET | `/rest/app_run` | List app runs. |
| app-run-detail | GET | `/rest/app_run/{id}` | Inspect a specific app run. |
| app-run-action-result | GET | `/rest/app_run/{id}/action_result` | Action results for an app run. |
| cef-to-raw | POST | `/rest/cef` | Convert CEF to human-friendly form. |
| command-run | GET | `/rest/command_run` | List command runs. |
| command-run-detail | GET | `/rest/command_run/{id}` | Inspect command run details. |
| lists | GET | `/rest/decided_list` | List decision lists. |
| list-detail | GET | `/rest/decided_list/{id}` | Retrieve a list by id or name. |
| vault-list | GET | `/rest/vault_document` | List vault documents. |
| vault-detail | GET | `/rest/vault_document/{id}` | Get vault document metadata. |
| aggregation-rules | GET | `/rest/aggregation_rule` | List aggregation rules. |
| aggregation-rule-detail | GET | `/rest/aggregation_rule/{id}` | Get aggregation rule. |
| indicators | GET | `/rest/indicator` | List indicators with filtering. |
| indicator-detail | GET | `/rest/indicator/{id}` | Indicator by id. |
| indicator-by-value | GET | `/rest/indicator_by_value` | Lookup indicator by value. |
| users | GET | `/rest/ph_user` | List users. |
| user-detail | GET | `/rest/ph_user/{id}` | User detail and preferences. |
| user-token | GET | `/rest/ph_user/{id}/token` | User tokens. |
| roles | GET | `/rest/role` | List roles. |
| role-detail | GET | `/rest/role/{id}` | Role detail. |
| tenants | GET | `/rest/tenant` | List tenants. |
| tenant-detail | GET | `/rest/tenant/{id}` | Get tenant detail. |
| audit | GET | `/rest/audit` | Audit log search with filters. |
| search | GET | `/rest/search` | Search across objects with Lucene-like syntax. |
| workbook | GET | `/rest/workbook` | Workbook definitions. |
| workbook-phase | GET | `/rest/workbook_phase` | Workbook phases. |
| workbook-phase-template | GET | `/rest/workbook_phase_template` | Workbook phase templates. |