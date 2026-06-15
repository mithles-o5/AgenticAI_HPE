# Server Agent

The **Server Agent** is an independently deployable microservice running on port **8009**. It is designed to manage physical bare-metal servers directly at the hardware BMC level via modern standards (Redfish), legacy protocols (IPMI), and HPE-specific RESTful API extensions (iLO).

---

## Broader Architecture Role

### Distinction from On-Prem Agent
- **On-Prem Agent** (Port 8008) manages high-level composable infrastructure abstractions (Logical Interconnects, Enclosures, Server Profiles) via **HPE OneView** or **Compute Ops Management (CoM)** APIs.
- **Server Agent** (Port 8009) targets physical/bare-metal servers directly, bypasses orchestrators like OneView, and talks directly to individual server BMCs (iLO, iDRAC, etc.) or uses standard `ipmitool` queries to fetch low-level sensor metrics, thermal details, event logs (SEL), and execute power control.

---

## Supported BMC Adapters

1. **Redfish Adapter**: The primary, preferred protocol adapter working across modern standards (DMTF Redfish REST API).
2. **IPMI Adapter**: Legacy protocol fallback using shell integration to `ipmitool`. Masks passwords in logs.
3. **iLO Adapter**: An extension of the Redfish Adapter utilizing HPE iLO OEM schemas for SmartStorage status and embedded media checks.
4. **Mock Adapter**: Fallback adapter returning realistic mocked server data for local development/testing.

---

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `PORT` | Microservice listening port | `8009` |
| `CAPABILITY_REGISTRY_URL` | OASF capability registry endpoint | `http://localhost:8020` |
| `CRED_VAULT_URL` | Secret repository base URL | `http://localhost:8200` |
| `SERVICE_TOKEN` | Authentication token for Cred Vault | `mock-service-token` |
| `CMDB_URL` | Postgres/Redis configuration repository URL | `http://localhost:8004` |
| `POLL_ENABLED` | Toggle background health checks | `true` |
| `POLL_INTERVAL_SECONDS` | Interval between polling cycles | `120` |
| `CPU_WARNING_THRESHOLD` | Percentage utilization for CPU warning | `80.0` |
| `MEMORY_WARNING_THRESHOLD` | Percentage utilization for memory warning | `85.0` |
| `TEMPERATURE_CRITICAL_THRESHOLD` | Celsius temperature threshold for critical level | `90.0` |

---

## How to Run Locally

### Start Server
```bash
uvicorn main:app --port 8009 --reload
```

### Run Tests
```bash
pytest tests/ -v
```

---

## How to Add a New Adapter Plugin

1. Create a new python file in `adapters/plugins/` (e.g., `idrac_adapter.py`).
2. Inherit from `ServerAdapter` in `adapters/base.py` and implement all abstract methods.
3. Register the new class inside `core/adapter_manager.py` within the `REGISTRY` dictionary.

---

## OASF Registration

On startup, the agent sends its OASF capability manifest (`oasf_record.json`) to the Capability Registry via:
`POST http://localhost:8020/agents`

---

## Example API Curl Commands

### 1. Health Endpoint
```bash
curl http://localhost:8009/server-agent/health
```

### 2. Task Execution - Fetch Metrics
```bash
curl -X POST http://localhost:8009/server-agent/execute-task \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "test-task-1",
    "task_type": "monitoring",
    "resource_type": "server",
    "resource_id": "OV1-RackServer-001",
    "action": "fetch_metrics",
    "provider": "default",
    "credentials_ref": "mock"
  }'
```

### 3. Task Execution - Power Action
```bash
curl -X POST http://localhost:8009/server-agent/execute-task \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "test-task-2",
    "task_type": "control",
    "resource_type": "server",
    "resource_id": "OV1-RackServer-001",
    "action": "execute_action",
    "provider": "default",
    "parameters": {
      "action_type": "power_action",
      "power_state": "Off"
    },
    "credentials_ref": "mock"
  }'
```

### 4. Fetch Event Log
```bash
curl -X POST http://localhost:8009/server-agent/execute-task \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "test-task-3",
    "task_type": "monitoring",
    "resource_type": "server",
    "resource_id": "OV1-RackServer-001",
    "action": "fetch_event_log",
    "provider": "default",
    "parameters": {
      "severity": "Warning,Critical"
    },
    "credentials_ref": "mock"
  }'
```

### 5. Hardware Inventory
```bash
curl "http://localhost:8009/server-agent/inventory/OV1-RackServer-001?provider=default&credentials_ref=mock"
```

### 6. Force Background Poll Sync
```bash
curl -X POST http://localhost:8009/server-agent/poll/trigger
```
