# Live Test Report (Extended)

- Timestamp (UTC): 2025-11-20T18:43:14.638578Z
- Server: https://smatthew-soar.west.buttercup.cloud
- Verify SSL: False
- Tests executed: 18

## Results

### system_info
- Method: GET
- Path: /rest/system_info
- Status: 200
- Response:
```
{
  "base_url": "",
  "time_zone": "UTC",
  "machine_id": "3c82e9922a003876b30ac3eddaa6afde08c98b1f1d053eb13d44f32a217339ba"
}
```

### severity_list
- Method: GET
- Path: /rest/severity
- Status: 200
- Response:
```
{
  "count": 3,
  "num_pages": 1,
  "data": [
    {
      "id": 1,
      "name": "high",
      "is_default": false,
      "color": "red",
      "order": 0,
      "create_time": "2025-11-17T16:05:16.709562Z",
      "modified_time": "2025-11-17T16:05:16.709894Z",
      "disabled": false
    },
    {
      "id": 2,
      "name": "medium",
      "is_default": true,
      "color": "yellow",
      "order": 1,
      "create_time": "2025-11-17T16:05:16.711463Z",
      "modified_time": "2025-11-17T16:05:16.711644Z",
      "disabled": false
    },
    {
      "id": 3,
      "name": "low",
      "is_default": false,
      "color": "green",
      "order": 2,
      "create_time": "2025-11-17T16:05:16.712123Z",
      "modified_time": "2025-11-17T16:05:16.712277Z",
      "disabled": false
    }
  ]
}
```

### apps_list
- Method: GET
- Path: /rest/app
- Status: 200
- Response:
```
{
  "count": 0,
  "num_pages": 0,
  "data": []
}
```

### assets_list
- Method: GET
- Path: /rest/asset
- Status: 200
- Response:
```
{
  "count": 0,
  "num_pages": 0,
  "data": []
}
```

### playbooks_list
- Method: GET
- Path: /rest/playbook
- Status: 200
- Response:
```
{
  "count": 165,
  "num_pages": 17,
  "data": [
    {
      "tags": [
        "user",
        "microsoft_ad_ldap",
        "disable_account",
        "D3-AL",
        "active_directory"
      ],
      "id": 1,
      "active": false,
      "playbook_trigger": "artifact_created",
      "blockly": false,
      "blockly_xml": "<xml></xml>",
      "category": "Account Locking",
      "change": "9465838c8f1a17750118842b81ba3ccfdd922d6b",
      "comment": "AD LDAP Account Locking update\n",
      "create_time": "2023-08-28T13:23:39.000000Z",
      "disabled": false,
      "execute_order": 1,
      "json_change": "580ba997708aa8dd3713c7b843d610a97ad06b91",
      "labels": [
        "*"
      ],
      "log_level": 0,
      "name": "AD_LDAP_Account_Locking",
      "old_name": null,
      "passed_validation": true,
      "previous_versions": [],
      "safe_mode": false,
      "draft_mode": false,
      "scm": 1,
      "scm_user_name": "Lou Stella",
      "scm_email": "ljstella@gmail.com",
      "version": 1,
      "platform_version": "6.0.1.123902",
      "coa_schema_version": "5.0.10",
      "migrated_from_classic": false,
      "effective_user": 2,
      "latest_editor": null,
      "meta
```

### roles_list
- Method: GET
- Path: /rest/role
- Status: 200
- Response:
```
{
  "count": 7,
  "num_pages": 1,
  "data": [
    {
      "id": 1,
      "name": "Administrator",
      "description": "Administrators have full access to the entire system.",
      "disabled": false,
      "immutable": true,
      "version": 1,
      "type": "normal",
      "permissions": [
        {
          "id": 1,
          "edit": "allow",
          "execute": "deny",
          "extra": null,
          "name": "apps",
          "role": 1,
          "view": "allow",
          "delete": "deny",
          "content_type": null,
          "object_id": null
        },
        {
          "id": 2,
          "edit": "allow",
          "execute": "deny",
          "extra": null,
          "name": "assets",
          "role": 1,
          "view": "allow",
          "delete": "allow",
          "content_type": null,
          "object_id": null
        },
        {
          "id": 3,
          "edit": "allow",
          "execute": "deny",
          "extra": null,
          "name": "automation_broker",
          "role": 1,
          "view": "allow",
          "delete": "deny",
          "content_type": null,
          "object_id": null
        },
        {
          "id": 4,
          "ed
```

### users_list
- Method: GET
- Path: /rest/ph_user
- Status: 200
- Response:
```
{
  "count": 2,
  "num_pages": 1,
  "data": [
    {
      "last_login": null,
      "id": 1,
      "username": "soar_local_admin",
      "first_name": "",
      "last_name": "",
      "email": "root@localhost",
      "is_active": true,
      "is_staff": true,
      "is_superuser": true,
      "date_joined": "2025-11-17T16:06:55.300267Z",
      "prevent_login": false,
      "type": "normal",
      "default_label": null,
      "externally_managed": false,
      "default_tenant": null,
      "last_updated": "2025-11-17T16:10:11.372095Z",
      "splunk_external_user_type": null,
      "roles": [
        "Administrator"
      ],
      "location": null,
      "time_zone": null,
      "title": null,
      "show_onboarding": true,
      "onboarding_state": {}
    },
    {
      "last_login": "2025-11-19T16:14:40.820580Z",
      "id": 3,
      "username": "smatthew",
      "first_name": "s",
      "last_name": "matthew",
      "email": "smatthew@splunk.com",
      "is_active": true,
      "is_staff": true,
      "is_superuser": true,
      "date_joined": "2025-11-17T16:10:31.951776Z",
      "prevent_login": false,
      "type": "normal",
      "default_label": null,
      "externally_manage
```

### tenants_list
- Method: GET
- Path: /rest/tenant
- Status: 200
- Response:
```
{
  "count": 1,
  "num_pages": 1,
  "data": [
    {
      "id": 0,
      "name": "_default_",
      "description": "This is the default system tenant.",
      "contact": " ",
      "disabled": false,
      "slas": {
        "high": 60,
        "medium": 720,
        "low": 1440
      },
      "executive_approvers": null,
      "sla_expiry_warning_in_mins": null,
      "environment_variables": {}
    }
  ]
}
```

### indicators_list
- Method: GET
- Path: /rest/indicator
- Status: 200
- Response:
```
{
  "count": 3,
  "num_pages": 3,
  "data": [
    {
      "tags": [],
      "id": 1,
      "value": "192.168.1.100",
      "value_hash": "2a39f1eedcd9f986327b5e4da842426f4f05b8f16f0ef385639dbec0db70eaae",
      "tenant": 0,
      "earliest_time": "2025-11-18T21:29:06.125502Z",
      "latest_time": "2025-11-18T21:31:01.920153Z",
      "open_events": 4,
      "total_events": 4,
      "severity_counts": [
        {
          "name": "high",
          "count": 0
        },
        {
          "name": "medium",
          "count": 4
        },
        {
          "name": "low",
          "count": 0
        }
      ]
    }
  ]
}
```

### vault_list
- Method: GET
- Path: /rest/vault_document
- Status: 200
- Response:
```
{
  "count": 0,
  "num_pages": 0,
  "data": []
}
```

### decided_list
- Method: GET
- Path: /rest/decided_list
- Status: 200
- Response:
```
{
  "count": 0,
  "num_pages": 0,
  "data": []
}
```

### container_create
- Method: POST
- Path: /rest/container
- Status: 200
- Response:
```
{
  "success": true,
  "id": 22,
  "new_artifact_ids": []
}
```

### artifact_create
- Method: POST
- Path: /rest/artifact
- Status: 200
- Response:
```
{
  "success": true,
  "id": 18
}
```

### note_create
- Method: POST
- Path: /rest/note
- Status: 200
- Response:
```
{
  "success": true,
  "id": 10
}
```

### evidence_create
- Method: POST
- Path: /rest/evidence
- Status: 200
- Response:
```
{
  "success": true,
  "id": 5
}
```

### approval_create
- Method: POST
- Path: /rest/approval
- Status: 405
- Response:
```
{
  "failed": true,
  "message": "Method not allowed"
}
```

### run_playbook
- Method: POST
- Path: /rest/run_playbook
- Status: 404
- Response:
```
{
  "failed": true,
  "message": "not found run_playbook"
}
```

### audit_list
- Method: GET
- Path: /rest/audit
- Status: 200
- Response:
```
{
  "count": 0,
  "num_pages": 0,
  "data": []
}
```
