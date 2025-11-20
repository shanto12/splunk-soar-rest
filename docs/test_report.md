# Live Test Report

- Timestamp (UTC): 2025-11-20T17:42:19.156808Z
- Server: https://smatthew-soar.west.buttercup.cloud
- Verify SSL: False
- Tests executed: 8

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

### container_create
- Method: POST
- Path: /rest/container
- Status: 200
- Response:
```
{
  "success": true,
  "id": 20,
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
  "id": 16
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
  "id": 8
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
  "id": 3
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
