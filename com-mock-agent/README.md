# COM / HPE OneView Mock Agent — Beast Edition

A production-grade API mock agent that generates a fully functional, stateful,
protocol-faithful HPE OneView / Compute Ops Management mock server from API documentation.

---

## What makes this the Beast Edition

| Dimension | Mentor's Version | Beast Edition |
|---|---|---|
| **Doc Parsing** | Hardcoded 60-section list | 3-subagent recursive multi-page fetcher |
| **Resource Model** | Isolated flat collections | Semantic graph with typed relationships |
| **Protocol Fidelity** | Generic REST responses | Full HPE OneView: ETag, async tasks, version negotiation, HPE error format |
| **Data Quality** | Template clones `{id, name, status}` | Schema-driven typed synthesis with 15 realistic field types |
| **State Persistence** | In-memory dict (lost on restart) | Async SQLite with transactions + full audit log |
| **Agent Architecture** | Linear 3-node pipeline | Parallel multi-agent with validation–retry loop |

---

## Architecture

```
START
  │
[DocFetcherAgent]          ← recursive multi-page crawl (concurrently fetches 8 pages)
  │
  ├── HPE OneView URL?
  │     └── [FastPathNode] ← uses pre-seeded schemas, skips LLM extraction
  │
  └── Unknown API?
        └── [SchemaExtractorAgent × N batches] ← parallel LLM extraction
  │
[RelationshipMapperAgent]  ← builds cross-resource foreign-key graph
  │
[DataSynthesisAgent]  ◄────────────────────┐
  │                                          │ retry (up to 3x)
[ValidatorAgent]       ──── errors? ────────┘
  │ (clean)
[DbSeederAgent]        ← writes to SQLite (persistent)
  │
END
```

---

## Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set your LLM provider key
```bash
cp .env.example .env
# Edit .env and add GROQ_API_KEY (free at https://console.groq.com)
```

### 3. Run HPE OneView mock (fast path — no URL crawl needed)
```bash
python run_mock_agent.py --hpe-oneview
```

This generates 5 instances of every HPE OneView resource type, seeds them into
SQLite, and starts the mock server on port 8080.

### 4. Browse the API
- Swagger UI: http://localhost:8080/docs
- API overview: http://localhost:8080/
- Version info: http://localhost:8080/rest/version
- Server hardware: http://localhost:8080/rest/server-hardware

### 5. Other options
```bash
# More sample data
python run_mock_agent.py --hpe-oneview --instances 20

# Crawl unknown API docs
python run_mock_agent.py --url https://your-api-docs.example.com

# Reset and re-seed
python run_mock_agent.py --hpe-oneview --reset

# Serve existing DB without re-crawling
python run_mock_agent.py --serve-only

# Enable auth (after teammate integrates JWT)
python run_mock_agent.py --hpe-oneview --enable-auth
```

---

## HPE OneView Protocol Features

### ETag Concurrency
Every resource includes an `eTag` field. PUT requests must include `If-Match`:
```
GET  /rest/server-hardware/abc123
     → Response header: ETag: "d41d8cd9..."

PUT  /rest/server-hardware/abc123
     → Request header:  If-Match: "d41d8cd9..."
     → 200 OK (if match) or 412 Precondition Failed (if stale)
```

### Async Task System
POST/PUT/DELETE on complex resources return **202** with a task URI:
```json
{
  "taskUri": "/rest/tasks/7F3A2B1C-...",
  "taskState": "Running",
  "percentComplete": 0
}
```
Poll `GET /rest/tasks/{id}` to watch progress → `Running` → `Completed`.

### API Version Negotiation
```
GET /rest/version
→ {"currentVersion": 4600, "minimumVersion": 2800}

All requests should include:
X-API-Version: 4600
```

### Referential Integrity
- Deleting `ServerHardware` → nullifies `serverProfileUri` on linked `ServerProfile`
- Deleting `StoragePool` → cascade-deletes all `Volumes` in that pool
- Deleting `ServerHardwareType` → **blocked** (restrict) if server profiles reference it

### HPE Error Format
All errors use the standard envelope:
```json
{
  "errorCode": "RESOURCE_NOT_FOUND",
  "message": "The requested resource was not found.",
  "details": "/rest/server-hardware/abc123",
  "recommendedActions": ["Verify the resource URI and try again."],
  "nestedErrors": []
}
```

---

## Auth Integration (for your teammate)

Your teammate's JWT auth slots into `com_mock/oneview_protocol.py`:

```python
# 1. Replace the stub:
async def validate_token(token: str) -> Optional[dict]:
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    return {"username": payload["sub"], "role": payload["role"]}

# 2. Enable auth enforcement:
AUTH_ENABLED = True
```

Or at runtime:
```bash
python run_mock_agent.py --hpe-oneview --enable-auth
```

Role rules (already wired):
- `role == "admin"` → full CRUD access
- `role != "admin"` → GET allowed, POST/PUT/DELETE → 403

---

## Resource Types Covered

| Category | Resources |
|---|---|
| SERVERS | server-hardware, server-hardware-types, server-profiles, server-profile-templates |
| NETWORKING | ethernet-networks, fc-networks, network-sets |
| STORAGE | storage-systems, storage-pools, volumes |
| FACILITIES | enclosures, enclosure-groups, racks |
| ACTIVITY | tasks, alerts, events |
| FIRMWARE | firmware-drivers |
| SETTINGS | scopes |

---

## Database

Data lives in `output/mock.db` (SQLite). Tables:
- `resources` — all resource instances as JSON blobs
- `tasks` — async task records with state machine
- `resource_events` — immutable audit log of every mutation

```bash
# Inspect with any SQLite client:
sqlite3 output/mock.db "SELECT resource_type, COUNT(*) FROM resources GROUP BY resource_type;"
```
