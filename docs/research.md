# Splunk SOAR REST API research

Source: pages under `https://docs.splunk.com/Documentation/SOAR/latest/PlatformAPI/…`. Pages were downloaded into `docs/raw/*.html` for offline reference. A regex extraction of endpoint paths is stored in `docs/endpoints_clean.txt`.

## Authentication
- Basic auth (`username:password`) or token auth by passing `ph-auth-token` as the username with an empty password. Example: `curl -u ":<ph-auth-token>" https://<host>/rest/container/1`.
- TLS verification can be disabled with `-k` (not recommended outside lab).

## Common patterns
- Base URL: `https://<host>/rest`.
- CRUD pattern for many entities: `GET /rest/<resource>`, `GET /rest/<resource>/<id>`, `POST /rest/<resource>`, `POST /rest/<resource>/<id>` for updates, `DELETE /rest/<resource>/<id>`.
- Filtering: `_filter_<field>__<operator>=<value>` (operators include `icontains`, `contains`, `iexact`, `gt`, `gte`, `lt`, `lte`). Combine with query params like `page`, `page_size`, `sort`, `pretty`, `include_expensive`.
- Bulk create/update endpoints accept lists in the POST body (e.g., `/rest/container` with an array of objects).
- Pagination: `page` (0-based) and `page_size` (default 10) on list endpoints.

## Endpoint families (high level)
- **System/info**: `/rest/system/info`, `/rest/info`, `/rest/hud_config`, `/rest/status`, `/rest/severity`, `/rest/feature_flag`, `/rest/app_status`, `/rest/app_run`, `/rest/app_run/<id>/action_result`.
- **Administration**: `/rest/role`, `/rest/user`, `/rest/users_roles`, `/rest/user_settings`, `/rest/tenant`, `/rest/forwarder_group`, `/rest/scm`, `/rest/automation_broker`, `/rest/notification`.
- **Assets & apps**: `/rest/asset`, `/rest/app`, `/rest/app_run`, `/rest/app_status`, `/rest/cef` (CEF parser), `/rest/command_run` (configure custom command runs).
- **Containers & artifacts**: `/rest/container`, `/rest/artifact`, `/rest/evidence`, `/rest/note`, `/rest/list`, `/rest/vault`, `/rest/search`, `/rest/cefvault`, plus optional query params like `_annotation_authorized_users`.
- **Playbooks & automation**: `/rest/playbook`, `/rest/custom_function`, `/rest/run_playbook`, `/rest/run_action`, `/rest/action_run`, `/rest/aggregation_rule`, `/rest/workbook`, `/rest/external_prompt`.
- **Approvals & workflow**: `/rest/approval`, `/rest/approval/<id>/detail_summary_view`.
- **Security / indicators**: `/rest/indicator`, `/rest/indicator/<id>`, `/rest/status`, `/rest/severity`.
- **Audit & logs**: `/rest/audit` (filter by `user`, `role`, `playbook`, `container`, `tenant`).

## Example calls pulled from docs
- Get container by ID: `curl -u "user:pass" https://<host>/rest/container/1`.
- List containers with filters: `curl -G -u token: https://<host>/rest/container?_filter_name__icontains=phish&page=0&page_size=20`.
- Create containers (bulk): `curl -u token: https://<host>/rest/container -d '[{"name":"Example","label":"events"}]'`.
- Create artifact on a container: `curl -u token: https://<host>/rest/artifact -d '{"container_id":123,"name":"ip","cef":{"sourceAddress":"1.1.1.1"}}'`.
- Run action: `curl -u token: https://<host>/rest/run_action -d '{"action":"geolocate ip","parameters":[{"ip":"1.1.1.1"}],"assets":["maxmind"]}'`.
- Run playbook: `curl -u token: https://<host>/rest/run_playbook -d '{"playbook_id":42,"container_id":100,"scope":"all","run":true}'`.
- Get system info: `curl -u token: https://<host>/rest/info`.
- Create note/evidence: `POST /rest/note` with `{"container_id":1,"content":"Investigation note"}`; `POST /rest/evidence` with `{"container_id":1,"content":"Artifact linked","artifact_id":55}`.
- Approvals: `POST /rest/approval` with `{"summary":"Approve action","status":"pending","container_id":1}` then `POST /rest/approval/<id>` to update or `/detail_summary_view` to retrieve.

## Extracted endpoint list
See `docs/endpoints_clean.txt` (311 unique paths/patterns extracted from the official docs) for the full set referenced across the Splunk SOAR REST API documentation set.

