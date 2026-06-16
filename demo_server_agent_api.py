"""
demo_server_agent_api.py
========================
Demonstrates calling HPE server-related APIs through the Server Agent proxy
(running at http://localhost:8009).

The Server Agent proxies:
  - OneView APIs  (/rest/...)            -> port 8000
  - Compute Ops   (/compute-ops-mgmt/?)  ? port 8001

It BLOCKS non-server resources (storage volumes, ethernet networks, etc.)
with HTTP 403.

Prerequisites (all started by start_services.py or manually):
  - OneView mock      : http://localhost:8000
  - Compute Ops mock  : http://localhost:8001
  - Server Agent      : http://localhost:8009

Usage:
  python demo_server_agent_api.py
"""

import json
import sys
import textwrap

try:
    import httpx
except ImportError:
    sys.exit("httpx is required: pip install httpx")

SERVER_AGENT = "http://localhost:8009"
SEPARATOR = "-" * 68


def _pretty(data):
    if isinstance(data, (dict, list)):
        text = json.dumps(data, indent=2)
    else:
        text = str(data)
    lines = text.splitlines()
    preview = lines[:30]
    if len(lines) > 30:
        preview.append(f"  ... ({len(lines) - 30} more lines truncated)")
    return "\n".join("  " + l for l in preview)


def call(label: str, method: str, url: str, body=None, expect_status=None):
    print(f"\n{'-'*68}")
    print(f"  {label}")
    print(f"  {method} {url}")
    try:
        with httpx.Client(timeout=10) as client:
            resp = client.request(method, url, json=body)
        status = resp.status_code
        try:
            data = resp.json()
        except Exception:
            data = resp.text

        badge = "[OK]" if (expect_status is None and status < 400) or status == expect_status else "[!!]"
        print(f"  {badge}  Status: {status}")
        print(_pretty(data))
    except Exception as exc:
        print(f"  [!!]  Connection error: {exc}")


# ------------------------------------------------------------------------------
# 1. HEALTH CHECK
# ------------------------------------------------------------------------------
print(f"\n{'='*68}")
print("  SERVER AGENT PROXY DEMO")
print(f"  Base URL: {SERVER_AGENT}")
print(f"{'='*68}")

call(
    label="[HEALTH] Server Agent health check",
    method="GET",
    url=f"{SERVER_AGENT}/server-agent/health",
)

# ------------------------------------------------------------------------------
# 2. ONEVIEW  ?  ALLOWED PATHS (proxied through Server Agent)
# ------------------------------------------------------------------------------
print(f"\n{'='*68}")
print("  ONEVIEW ? ALLOWED SERVER PATHS  (proxied ? :8000)")
print(f"{'='*68}")

call(
    label="[ALLOW] List all server hardware",
    method="GET",
    url=f"{SERVER_AGENT}/rest/server-hardware",
    expect_status=200,
)

call(
    label="[ALLOW] List custom servers",
    method="GET",
    url=f"{SERVER_AGENT}/rest/custom-servers",
    expect_status=200,
)

call(
    label="[ALLOW] List rack managers",
    method="GET",
    url=f"{SERVER_AGENT}/rest/rack-managers",
    expect_status=200,
)

call(
    label="[ALLOW] Login sessions (POST)",
    method="POST",
    url=f"{SERVER_AGENT}/rest/login-sessions",
    body={"userName": "admin", "password": "admin"},
    expect_status=200,
)

# ------------------------------------------------------------------------------
# 3. ONEVIEW  ?  BLOCKED PATHS (non-server resources ? 403)
# ------------------------------------------------------------------------------
print(f"\n{'='*68}")
print("  ONEVIEW ? BLOCKED NON-SERVER PATHS  (should get 403)")
print(f"{'='*68}")

call(
    label="[BLOCK] Ethernet networks (non-server resource)",
    method="GET",
    url=f"{SERVER_AGENT}/rest/ethernet-networks",
    expect_status=403,
)

call(
    label="[BLOCK] Storage volumes (non-server resource)",
    method="GET",
    url=f"{SERVER_AGENT}/rest/storage-volumes",
    expect_status=403,
)

call(
    label="[BLOCK] Storage systems (non-server resource)",
    method="GET",
    url=f"{SERVER_AGENT}/rest/storage-systems",
    expect_status=403,
)

call(
    label="[BLOCK] Interconnects (non-server resource)",
    method="GET",
    url=f"{SERVER_AGENT}/rest/interconnects",
    expect_status=403,
)

# ------------------------------------------------------------------------------
# 4. COMPUTE OPS  ?  ALLOWED PATHS (proxied ? :8001)
# ------------------------------------------------------------------------------
print(f"\n{'='*68}")
print("  COMPUTE OPS ? ALLOWED SERVER PATHS  (proxied ? :8001)")
print(f"{'='*68}")

call(
    label="[ALLOW] List servers",
    method="GET",
    url=f"{SERVER_AGENT}/compute-ops-mgmt/v1/servers",
    expect_status=200,
)

call(
    label="[ALLOW] List custom servers",
    method="GET",
    url=f"{SERVER_AGENT}/compute-ops-mgmt/v1/custom-servers",
    expect_status=200,
)

call(
    label="[ALLOW] List server groups",
    method="GET",
    url=f"{SERVER_AGENT}/compute-ops-mgmt/v1/groups",
    expect_status=200,
)

call(
    label="[ALLOW] List server settings",
    method="GET",
    url=f"{SERVER_AGENT}/compute-ops-mgmt/v1/settings",
    expect_status=200,
)

call(
    label="[ALLOW] List firmware bundles",
    method="GET",
    url=f"{SERVER_AGENT}/compute-ops-mgmt/v1/firmware-bundles",
    expect_status=200,
)

# ------------------------------------------------------------------------------
# 5. COMPUTE OPS  ?  BLOCKED PATHS (non-server resources ? 403)
# ------------------------------------------------------------------------------
print(f"\n{'='*68}")
print("  COMPUTE OPS ? BLOCKED NON-SERVER PATHS  (should get 403)")
print(f"{'='*68}")

call(
    label="[BLOCK] Storage (non-server resource)",
    method="GET",
    url=f"{SERVER_AGENT}/compute-ops-mgmt/v1/storage",
    expect_status=403,
)

call(
    label="[BLOCK] Switches (non-server resource)",
    method="GET",
    url=f"{SERVER_AGENT}/compute-ops-mgmt/v1/switches",
    expect_status=403,
)

call(
    label="[BLOCK] Networks (non-server resource)",
    method="GET",
    url=f"{SERVER_AGENT}/compute-ops-mgmt/v1/networks",
    expect_status=403,
)

# ------------------------------------------------------------------------------
# 6. LEGACY /compute-ops/ PREFIX ROUTES
# ------------------------------------------------------------------------------
print(f"\n{'='*68}")
print("  COMPUTE OPS ? LEGACY /compute-ops/ PREFIX ROUTES")
print(f"{'='*68}")

call(
    label="[ALLOW] Legacy prefix: /compute-ops/v1/servers",
    method="GET",
    url=f"{SERVER_AGENT}/compute-ops/v1/servers",
    expect_status=200,
)

call(
    label="[BLOCK] Legacy prefix: /compute-ops/v1/networks  (should 403)",
    method="GET",
    url=f"{SERVER_AGENT}/compute-ops/v1/networks",
    expect_status=403,
)

# ------------------------------------------------------------------------------
# 7. /server-agent/ PREFIX VARIANTS
# ------------------------------------------------------------------------------
print(f"\n{'='*68}")
print("  SERVER AGENT PREFIX VARIANTS  (/server-agent/rest/?)")
print(f"{'='*68}")

call(
    label="[ALLOW] /server-agent/rest/server-hardware",
    method="GET",
    url=f"{SERVER_AGENT}/server-agent/rest/server-hardware",
    expect_status=200,
)

call(
    label="[ALLOW] /server-agent/compute-ops-mgmt/v1/servers",
    method="GET",
    url=f"{SERVER_AGENT}/server-agent/compute-ops-mgmt/v1/servers",
    expect_status=200,
)

call(
    label="[BLOCK] /server-agent/rest/storage-volumes  (should 403)",
    method="GET",
    url=f"{SERVER_AGENT}/server-agent/rest/storage-volumes",
    expect_status=403,
)

# ------------------------------------------------------------------------------
# 8. CRUD demo: Create -> Read -> Update -> Delete a custom server (OneView)
#    The mock assigns its own UUID on POST, so we capture it dynamically.
# ------------------------------------------------------------------------------
print(f"\n{'='*68}")
print("  CRUD DEMO - Custom Server via Server Agent -> OneView")
print(f"{'='*68}")

new_server = {
    "name": "Demo-Server-001",
    "model": "HPE ProLiant DL380 Gen10",
    "status": "OK",
    "powerState": "On",
}

print(f"\n{'-'*68}")
print("  [CREATE] POST /rest/custom-servers")
print(f"  POST {SERVER_AGENT}/rest/custom-servers")
server_id = None
try:
    with httpx.Client(timeout=10) as client:
        resp = client.post(f"{SERVER_AGENT}/rest/custom-servers", json=new_server)
    created = resp.json()
    server_id = created.get("id")
    badge = "[OK]" if resp.status_code in (200, 201) else "[!!]"
    print(f"  {badge}  Status: {resp.status_code}  (assigned id: {server_id})")
    print(_pretty(created))
except Exception as exc:
    print(f"  [!!]  Error: {exc}")

if server_id:
    call(
        label=f"[READ]   GET  /rest/custom-servers/{server_id}",
        method="GET",
        url=f"{SERVER_AGENT}/rest/custom-servers/{server_id}",
        expect_status=200,
    )

    call(
        label=f"[UPDATE] PUT  /rest/custom-servers/{server_id}",
        method="PUT",
        url=f"{SERVER_AGENT}/rest/custom-servers/{server_id}",
        body={**new_server, "powerState": "Off", "status": "Warning"},
        expect_status=200,
    )

    call(
        label=f"[DELETE] DELETE /rest/custom-servers/{server_id}",
        method="DELETE",
        url=f"{SERVER_AGENT}/rest/custom-servers/{server_id}",
        expect_status=200,
    )

    call(
        label=f"[VERIFY] GET  /rest/custom-servers/{server_id}  (should 404 after delete)",
        method="GET",
        url=f"{SERVER_AGENT}/rest/custom-servers/{server_id}",
        expect_status=404,
    )
else:
    print("  [SKIP] Could not get server ID from POST - skipping read/update/delete")

print(f"\n{'='*68}")
print("  Demo complete!")
print(f"{'='*68}\n")

