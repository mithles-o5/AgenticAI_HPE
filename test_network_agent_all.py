"""
Network Agent API Integration Test
Tests all 5 core actions against actual running services.
"""
import httpx
import json
import sys

NETWORK_AGENT = "http://127.0.0.1:8006"
MOCK_NETWORK  = "http://127.0.0.1:8002"

# Devices confirmed in CMDB + mock DB
SWITCH_SN   = "aruba-cx-017"   # from mock DB
ROUTER_SN   = "core-sw-018"    # from mock DB
GATEWAY_SN  = "wireless-ctrl-020"  # from mock DB
AP_SN       = "ap-floor-022"   # from mock DB
FIREWALL_SN = "edge-router-019"    # in CMDB

HEADERS = {"Content-Type": "application/json"}
PASS = "[PASS]"
FAIL = "[FAIL]"


def post(path, payload):
    try:
        r = httpx.post(f"{NETWORK_AGENT}{path}", json=payload, timeout=15.0)
        return r.status_code, r.json()
    except Exception as e:
        return 0, {"error": str(e)}


def get_mock(path):
    try:
        r = httpx.get(f"{MOCK_NETWORK}{path}", timeout=10.0)
        return r.status_code, r.json()
    except Exception as e:
        return 0, {"error": str(e)}


def check(label, sc, body):
    status = body.get("status", "")
    errors = body.get("errors", [])
    ok = sc in (200, 201) and status in ("success", "partial") and not errors
    icon = PASS if ok else FAIL
    print(f"  {icon}  {label}")
    if not ok:
        print(f"       status_code={sc}  status={status!r}  errors={errors}")
        metrics = body.get("metrics", {})
        if metrics:
            print(f"       metrics keys: {list(metrics.keys())}")
    return ok


print("=" * 65)
print("  NETWORK AGENT — FULL API INTEGRATION TEST")
print("=" * 65)
results = []


# ── 1. Health Check endpoint ──────────────────────────────────────────────────
print("\n[1] Agent Health & Protocol Registration")
sc, body = 0, {}
try:
    r = httpx.get(f"{NETWORK_AGENT}/network-agent/health", timeout=5.0)
    sc, body = r.status_code, r.json()
except Exception as e:
    body = {"error": str(e)}
ok = sc == 200 and body.get("status") == "ok"
print(f"  {PASS if ok else FAIL}  GET /network-agent/health -> {body}")
results.append(ok)

sc, body = 0, {}
try:
    r = httpx.get(f"{NETWORK_AGENT}/network-agent/protocols", timeout=5.0)
    sc, body = r.status_code, r.json()
except Exception as e:
    body = {"error": str(e)}
ok = sc == 200 and "protocols" in body
print(f"  {PASS if ok else FAIL}  GET /network-agent/protocols -> {body.get('protocols', body)}")
results.append(ok)


# ── 2. fetch_metrics — single switch ─────────────────────────────────────────
print(f"\n[2] fetch_metrics — single switch ({SWITCH_SN})")
sc, body = post("/network-agent/execute-task", {
    "task_id": "test-fetch-001",
    "task_type": "monitoring",
    "agent_type": "network",
    "resource_type": "switch",
    "resource_id": SWITCH_SN,
    "protocol": "mock_network",
    "action": "fetch_metrics",
    "parameters": {
        "api_path": f"/network/v1/devices/{SWITCH_SN}",
        "http_method": "GET"
    }
})
results.append(check("fetch_metrics single switch", sc, body))
if body.get("metrics"):
    print(f"       interfaces: {len(body['metrics'].get('interfaces', []))}")  


# ── 3. fetch_metrics — fleet (all switches) ───────────────────────────────────
print("\n[3] fetch_metrics — fleet (all switches via /monitoring/v1/switches)")
sc, body = post("/network-agent/execute-task", {
    "task_id": "test-fetch-002",
    "task_type": "monitoring",
    "agent_type": "network",
    "resource_type": "switch",
    "resource_id": "all",
    "protocol": "mock_network",
    "action": "fetch_metrics",
    "parameters": {
        "api_path": "/monitoring/v1/switches",
        "http_method": "GET"
    }
})
results.append(check("fetch_metrics fleet switches", sc, body))
if body.get("metrics"):
    print(f"       switch count: {len(body['metrics'].get('interfaces', []))}")


# ── 4. fetch_metrics — all devices ────────────────────────────────────────────
print("\n[4] fetch_metrics — all network devices")
sc, body = post("/network-agent/execute-task", {
    "task_id": "test-fetch-003",
    "task_type": "monitoring",
    "agent_type": "network",
    "resource_type": "network_device",
    "resource_id": "all",
    "protocol": "mock_network",
    "action": "fetch_metrics",
    "parameters": {
        "api_path": "/network/v1/devices",
        "http_method": "GET"
    }
})
results.append(check("fetch_metrics all devices", sc, body))
if body.get("metrics"):
    print(f"       device count: {len(body['metrics'].get('interfaces', []))}")


# ── 5. health_check — single gateway ─────────────────────────────────────────
print(f"\n[5] health_check — single gateway ({GATEWAY_SN})")
sc, body = post("/network-agent/execute-task", {
    "task_id": "test-health-001",
    "task_type": "monitoring",
    "agent_type": "network",
    "resource_type": "gateway",
    "resource_id": GATEWAY_SN,
    "protocol": "mock_network",
    "action": "health_check",
    "parameters": {
        "api_path": f"/network/v1/devices/{GATEWAY_SN}",
        "http_method": "GET"
    }
})
results.append(check("health_check single gateway", sc, body))
if body.get("metrics"):
    print(f"       healthy={body['metrics'].get('healthy')}  health_status={body['metrics'].get('health_status')}")


# ── 6. health_check — fleet switches ─────────────────────────────────────────
print("\n[6] health_check — fleet (all switches)")
sc, body = post("/network-agent/execute-task", {
    "task_id": "test-health-002",
    "task_type": "monitoring",
    "agent_type": "network",
    "resource_type": "switch",
    "resource_id": "all",
    "protocol": "mock_network",
    "action": "health_check",
    "parameters": {
        "api_path": "/monitoring/v1/switches",
        "http_method": "GET"
    }
})
results.append(check("health_check fleet switches", sc, body))


# ── 7. execute_action — Power ON ──────────────────────────────────────────────
print(f"\n[7] execute_action — Power ON for switch ({SWITCH_SN})")
sc, body = post("/network-agent/execute-task", {
    "task_id": "test-action-on-001",
    "task_type": "operational",
    "agent_type": "network",
    "resource_type": "switch",
    "resource_id": SWITCH_SN,
    "protocol": "mock_network",
    "action": "execute_action",
    "parameters": {
        "api_path": f"/network/v1/devices/{SWITCH_SN}/power",
        "http_method": "POST",
        "action_verb": "on",
        "payload": {"action": "ON"}
    }
})
results.append(check("execute_action Power ON switch", sc, body))
if body.get("metrics"):
    print(f"       power_state={body['metrics'].get('power_state')}")


# ── 8. execute_action — Power OFF ─────────────────────────────────────────────
print(f"\n[8] execute_action — Power OFF for router ({ROUTER_SN})")
sc, body = post("/network-agent/execute-task", {
    "task_id": "test-action-off-001",
    "task_type": "operational",
    "agent_type": "network",
    "resource_type": "router",
    "resource_id": ROUTER_SN,
    "protocol": "mock_network",
    "action": "execute_action",
    "parameters": {
        "api_path": f"/network/v1/devices/{ROUTER_SN}/power",
        "http_method": "POST",
        "action_verb": "off",
        "payload": {"action": "OFF"}
    }
})
results.append(check("execute_action Power OFF router", sc, body))
if body.get("metrics"):
    print(f"       power_state={body['metrics'].get('power_state')}")


# ── 9. execute_config_push — VLAN push ────────────────────────────────────────
print(f"\n[9] execute_config_push — VLAN push to switch ({SWITCH_SN})")
sc, body = post("/network-agent/execute-task", {
    "task_id": "test-config-001",
    "task_type": "config_push",
    "agent_type": "network",
    "resource_type": "switch",
    "resource_id": SWITCH_SN,
    "protocol": "mock_network",
    "action": "execute_config_push",
    "parameters": {
        "api_path": f"/network/v1/devices/{SWITCH_SN}/vlans",
        "http_method": "POST",
        "payload": {"vlan_id": 200, "name": "Production-VLAN"}
    }
})
results.append(check("execute_config_push VLAN push", sc, body))


# ── 10. execute_config_push — Port status ─────────────────────────────────────
print(f"\n[10] execute_config_push — Port status change ({SWITCH_SN})")
sc, body = post("/network-agent/execute-task", {
    "task_id": "test-config-002",
    "task_type": "config_push",
    "agent_type": "network",
    "resource_type": "switch",
    "resource_id": SWITCH_SN,
    "protocol": "mock_network",
    "action": "execute_config_push",
    "parameters": {
        "api_path": f"/network/v1/devices/{SWITCH_SN}/ports/eth2/status",
        "http_method": "POST",
        "payload": {"status": "UP"}
    }
})
results.append(check("execute_config_push port status", sc, body))


# ── 11. discover_topology — single device ─────────────────────────────────────
print(f"\n[11] discover_topology — single switch ({SWITCH_SN})")
sc, body = post("/network-agent/execute-task", {
    "task_id": "test-topo-001",
    "task_type": "discovery",
    "agent_type": "network",
    "resource_type": "switch",
    "resource_id": SWITCH_SN,
    "protocol": "mock_network",
    "action": "discover_topology",
    "parameters": {
        "api_path": f"/network/v1/devices/{SWITCH_SN}",
        "http_method": "GET"
    }
})
results.append(check("discover_topology single", sc, body))
if body.get("topology"):
    print(f"       topology nodes: {len(body['topology'])}")


# ── 12. discover_topology — full fleet ────────────────────────────────────────
print("\n[12] discover_topology — full fleet (/network/v1/devices)")
sc, body = post("/network-agent/execute-task", {
    "task_id": "test-topo-002",
    "task_type": "discovery",
    "agent_type": "network",
    "resource_type": "network_device",
    "resource_id": "all",
    "protocol": "mock_network",
    "action": "discover_topology",
    "parameters": {
        "api_path": "/network/v1/devices",
        "http_method": "GET"
    }
})
results.append(check("discover_topology full fleet", sc, body))
if body.get("metrics"):
    nodes = body["metrics"].get("nodes", {})
    print(f"       nodes discovered: {len(nodes)}")


# ── 13. detect_fault — single device ─────────────────────────────────────────
print(f"\n[13] detect_fault — single AP ({AP_SN})")
sc, body = post("/network-agent/execute-task", {
    "task_id": "test-fault-001",
    "task_type": "fault_detection",
    "agent_type": "network",
    "resource_type": "access_point",
    "resource_id": AP_SN,
    "protocol": "mock_network",
    "action": "detect_fault",
    "parameters": {
        "api_path": f"/network/v1/devices/{AP_SN}",
        "http_method": "GET"
    }
})
results.append(check("detect_fault single AP", sc, body))
if body.get("status_level"):
    print(f"       status_level={body['status_level']}  insights={body.get('insights', [])}")


# ── 14. detect_fault — fleet scan ─────────────────────────────────────────────
print("\n[14] detect_fault — fleet scan (all devices)")
sc, body = post("/network-agent/execute-task", {
    "task_id": "test-fault-002",
    "task_type": "fault_detection",
    "agent_type": "network",
    "resource_type": "network_device",
    "resource_id": "all",
    "protocol": "mock_network",
    "action": "detect_fault",
    "parameters": {
        "api_path": "/network/v1/devices",
        "http_method": "GET"
    }
})
results.append(check("detect_fault fleet scan", sc, body))
if body.get("insights"):
    print(f"       issues found: {len(body['insights'])}")


# ── 15. Access Points via Aruba endpoint ──────────────────────────────────────
print("\n[15] fetch_metrics — Aruba APs (/network-monitoring/v1/aps)")
sc, body = post("/network-agent/execute-task", {
    "task_id": "test-aps-001",
    "task_type": "monitoring",
    "agent_type": "network",
    "resource_type": "access_point",
    "resource_id": "all",
    "protocol": "mock_network",
    "action": "fetch_metrics",
    "parameters": {
        "api_path": "/network-monitoring/v1/aps",
        "http_method": "GET"
    }
})
results.append(check("fetch_metrics Aruba APs", sc, body))


# ── 16. Power ON using mock alias protocol ────────────────────────────────────
print(f"\n[16] execute_action — Power ON using 'mock' protocol alias ({FIREWALL_SN})")
sc, body = post("/network-agent/execute-task", {
    "task_id": "test-alias-001",
    "task_type": "operational",
    "agent_type": "network",
    "resource_type": "firewall",
    "resource_id": FIREWALL_SN,
    "protocol": "mock",
    "action": "execute_action",
    "parameters": {
        "api_path": f"/network/v1/devices/{FIREWALL_SN}/power",
        "http_method": "POST",
        "action_verb": "on",
        "payload": {"action": "ON"}
    }
})
results.append(check("execute_action 'mock' alias protocol", sc, body))


# ── Summary ───────────────────────────────────────────────────────────────────
total = len(results)
passed = sum(results)
failed = total - passed
print()
print("=" * 65)
print(f"  RESULTS: {passed}/{total} passed  |  {failed} failed")
print("=" * 65)
sys.exit(0 if failed == 0 else 1)
