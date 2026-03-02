# API Reference

Base URL: `http://localhost:8000/api/v1`

## Endpoints

### GET /pipelines

Get all monitored pipelines.

**Query Parameters:**
- `skip` (int): Number of records to skip (default: 0)
- `limit` (int): Maximum records to return (default: 100)

**Response:**
```json
[
  {
    "id": 1,
    "platform": "github",
    "repository": "user/repo",
    "branch": "main",
    "commit_sha": "abc123...",
    "pipeline_id": "12345",
    "status": "failure",
    "started_at": "2024-01-01T00:00:00Z",
    "completed_at": "2024-01-01T00:05:00Z"
  }
]
```

### GET /pipelines/{pipeline_id}

Get specific pipeline details.

**Response:**
```json
{
  "id": 1,
  "platform": "github",
  "repository": "user/repo",
  "branch": "main",
  "commit_sha": "abc123...",
  "pipeline_id": "12345",
  "status": "failure",
  "started_at": "2024-01-01T00:00:00Z",
  "completed_at": "2024-01-01T00:05:00Z"
}
```

### GET /failures

Get all failure analyses.

**Query Parameters:**
- `skip` (int): Number of records to skip
- `limit` (int): Maximum records to return

**Response:**
```json
[
  {
    "id": 1,
    "pipeline_id": 1,
    "error_category": "dependency_conflict",
    "error_message": "Package version conflict...",
    "root_cause": "Incompatible versions of...",
    "confidence_score": 85,
    "analyzed_at": "2024-01-01T00:05:30Z"
  }
]
```

### GET /fixes

Get all applied fixes.

**Query Parameters:**
- `skip` (int): Number of records to skip
- `limit` (int): Maximum records to return

**Response:**
```json
[
  {
    "id": 1,
    "analysis_id": 1,
    "fix_type": "dependency_conflict_resolution",
    "description": "Updated package versions",
    "commit_sha": "def456...",
    "status": "verified",
    "success": true,
    "applied_at": "2024-01-01T00:06:00Z"
  }
]
```

### GET /stats

Get agent statistics.

**Response:**
```json
{
  "total_pipelines": 100,
  "total_failures": 25,
  "total_fixes": 20,
  "successful_fixes": 18,
  "success_rate": 90.0
}
```

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

## Error Responses

All endpoints may return error responses:

```json
{
  "detail": "Error message"
}
```

**Status Codes:**
- `200`: Success
- `404`: Resource not found
- `500`: Internal server error
