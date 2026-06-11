import json
import logging
import os
import sys
import time
import threading
import importlib.util
from typing import Dict, Any
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from server_agent import ServerAgent

# Configure logging to show timestamps and clean levels
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("server-agent-example")

# Global lock and query tracker for task state simulations
lock = threading.Lock()
task_calls: Dict[str, int] = {}

def get_task_call_count(task_id: str) -> int:
    """Thread-safe request counter helper for mock tasks."""
    with lock:
        count = task_calls.get(task_id, 0)
        task_calls[task_id] = count + 1
        return count


# ── Dynamically Load Generator Mock Servers ───────────────────────────────────

def load_fastapi_app(module_path: str, module_name: str) -> FastAPI:
    """
    Loads a FastAPI application from a file path dynamically, 
    isolating the sys.path to prevent namespace collisions (e.g. models.py conflicts).
    """
    dir_path = os.path.dirname(module_path)
    sys.path.insert(0, dir_path)
    try:
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Could not load spec for module at {module_path}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module.app
    finally:
        sys.path.remove(dir_path)


# Paths to the generator mock servers
ONEVIEW_SERVER_PATH = r"c:\Users\ELCOT\Desktop\sso_project\AgenticAI_HPE\generator\servers\oneview\main.py"
COMPUTE_OPS_SERVER_PATH = r"c:\Users\ELCOT\Desktop\sso_project\AgenticAI_HPE\generator\servers\compute_ops\main.py"

logger.info("Loading auto-generated FastAPI mock servers from generator...")
oneview_app = load_fastapi_app(ONEVIEW_SERVER_PATH, "generator_oneview")
compute_ops_app = load_fastapi_app(COMPUTE_OPS_SERVER_PATH, "generator_compute_ops")


# ── Dynamically Add Testing Routes to the Generator Mock Servers ──────────────

# 1. Extend OneView Mock Server
@oneview_app.put("/rest/server-hardware/{id}/powerState")
def oneview_put_power_state(id: str):
    with lock:
        task_calls["999"] = 0
    return {"taskUri": "/rest/tasks/999"}

@oneview_app.put("/rest/server-hardware/{id}/firmware")
def oneview_put_firmware(id: str):
    with lock:
        task_calls["777"] = 0
    return {"taskUri": "/rest/tasks/777"}

@oneview_app.get("/rest/tasks/{task_id}")
def oneview_get_task(task_id: str):
    count = get_task_call_count(task_id)
    if task_id == "999":
        if count == 0:
            return {"taskState": "Running", "percentComplete": 0}
        elif count == 1:
            return {"taskState": "Running", "percentComplete": 50}
        else:
            return {
                "taskState": "Completed",
                "percentComplete": 100,
                "statusText": "Server powered off successfully via HPE OneView"
            }
    elif task_id == "777":
        if count == 0:
            return {"taskState": "Running", "percentComplete": 0}
        else:
            return {
                "taskState": "Completed",
                "percentComplete": 100,
                "statusText": "Firmware updated successfully on system blade"
            }
    return JSONResponse(status_code=404, content={"message": "Task not found"})

@oneview_app.get("/rest/server-hardware/{id}/health")
def oneview_get_health(id: str):
    return {
        "statusText": "Normal",
        "powerState": "On",
        "healthState": "OK"
    }

@oneview_app.get("/rest/server-hardware/{id}/error-endpoint")
def oneview_get_error(id: str):
    return JSONResponse(
        status_code=500,
        content={
            "message": "Internal error occurred on management platform database.",
            "errorCode": "DB_CONN_TIMEOUT"
        }
    )


# 2. Extend Compute Ops Management (COM) Mock Server
@compute_ops_app.post("/api/v1/servers/{id}/power")
def com_post_power(id: str):
    with lock:
        task_calls["abc-123"] = 0
    return {"taskUri": "/api/v1/tasks/abc-123"}

@compute_ops_app.get("/api/v1/tasks/{task_id}")
def com_get_task(task_id: str):
    count = get_task_call_count(task_id)
    if task_id == "abc-123":
        if count == 0:
            return {"state": "running", "status": "running"}
        elif count == 1:
            return {"state": "running", "status": "running"}
        else:
            return {
                "state": "completed",
                "status": "success",
                "message": "Compute Ops Management action succeeded"
            }
    return JSONResponse(status_code=404, content={"message": "Task not found"})

@compute_ops_app.get("/api/v1/servers/{id}/health")
def com_get_health(id: str):
    return {
        "state": "OK",
        "health": "healthy"
    }


# ── Server Spin-up Helper using Uvicorn ───────────────────────────────────────

def run_uvicorn_server(app: FastAPI, port: int):
    config = uvicorn.Config(app, host="127.0.0.1", port=port, log_level="warning")
    server = uvicorn.Server(config)
    logger.info(f"Starting auto-generated mock server on port {port}...")
    server.run()


# ── Test Suite Execution ─────────────────────────────────────────────────────

def execute_test_cases():
    # Instantiate ServerAgent with configurable polling parameters
    # Set interval to 0.1s for fast tests
    agent = ServerAgent(poll_interval=0.1, poll_timeout=5.0)

    # 1. HPE OneView Async Power Off
    logger.info("\n=== TEST CASE 1: HPE OneView Async Power Off ===")
    oneview_power_payload = {
        "management_source": "ONEVIEW",
        "source_host": "http://localhost:8000",
        "api_endpoint": "/rest/server-hardware/1234/powerState",
        "http_method": "PUT",
        "action": "power_off",
        "category": "server",
        "serial_number": "ABC123",
        "credential_ref": "oneview_session_token_xyz"
    }
    res1 = agent.execute(oneview_power_payload)
    print(json.dumps(res1, indent=2))
    assert res1["success"] is True
    assert res1["status"] == "completed"
    assert "HPE OneView" in res1["message"]

    # 2. HPE OneView AUTO-GENERATED Endpoint Check (Scraped from actual docs!)
    logger.info("\n=== TEST CASE 2: HPE OneView AUTO-GENERATED Endpoint (Scraped route) ===")
    oneview_inv_payload = {
        "management_source": "ONEVIEW",
        "source_host": "http://localhost:8000",
        "api_endpoint": "/rest/server-hardware",
        "http_method": "GET",
        "action": "get_inventory",
        "serial_number": "ABC123"
    }
    res2 = agent.execute(oneview_inv_payload)
    print(json.dumps(res2, indent=2))
    assert res2["success"] is True
    # The output is parsed from mock_data.json inside generator/servers/oneview
    assert "type" in res2["raw_response"]
    assert "members" in res2["raw_response"]

    # 3. HPE COM Async Power On
    logger.info("\n=== TEST CASE 3: HPE COM Async Power On ===")
    com_power_payload = {
        "management_source": "COM",
        "source_host": "http://localhost:8001",
        "api_endpoint": "/api/v1/servers/5678/power",
        "http_method": "POST",
        "action": "power_on",
        "credential_ref": "com_oauth_jwt_token_abc",
        "serial_number": "XYZ789"
    }
    res3 = agent.execute(com_power_payload)
    print(json.dumps(res3, indent=2))
    assert res3["success"] is True
    assert res3["status"] == "completed"
    assert "Compute Ops Management" in res3["message"]

    # 4. HPE COM AUTO-GENERATED Endpoint Check (Scraped route!)
    logger.info("\n=== TEST CASE 4: HPE COM AUTO-GENERATED Endpoint (Scraped route) ===")
    com_inv_payload = {
        "management_source": "COM",
        "source_host": "http://localhost:8001",
        "api_endpoint": "/compute-ops-mgmt/v1beta2/appliances",
        "http_method": "GET",
        "action": "get_inventory",
        "serial_number": "XYZ789"
    }
    res4 = agent.execute(com_inv_payload)
    print(json.dumps(res4, indent=2))
    assert res4["success"] is True
    # This route is defined in generator/servers/compute_ops/main.py and loaded from mock_data.json
    assert "items" in res4["raw_response"]

    # 5. Validation Error: Missing required fields
    logger.info("\n=== TEST CASE 5: Validation Error (Missing HTTP method & API endpoint) ===")
    bad_payload_missing = {
        "management_source": "ONEVIEW",
        "source_host": "http://localhost:8000",
        "action": "power_off"
    }
    res5 = agent.execute(bad_payload_missing)
    print(json.dumps(res5, indent=2))
    assert res5["success"] is False
    assert "missing_fields" in res5["error"]["validation_errors"]

    # 6. Validation Error: Unsupported Management Source
    logger.info("\n=== TEST CASE 6: Validation Error (Unsupported Source) ===")
    bad_payload_source = {
        "management_source": "VSPHERE",
        "source_host": "http://localhost:8000",
        "api_endpoint": "/rest/server-hardware/1234/powerState",
        "http_method": "PUT",
        "action": "power_off"
    }
    res6 = agent.execute(bad_payload_source)
    print(json.dumps(res6, indent=2))
    assert res6["success"] is False

    # 7. Network/Connection Failure
    logger.info("\n=== TEST CASE 7: Connection Failure (Dead Port) ===")
    dead_host_payload = {
        "management_source": "ONEVIEW",
        "source_host": "http://localhost:9999",  # Port not in use
        "api_endpoint": "/rest/server-hardware/1234/powerState",
        "http_method": "PUT",
        "action": "power_off"
    }
    res7 = agent.execute(dead_host_payload)
    print(json.dumps(res7, indent=2))
    assert res7["success"] is False

    # 8. Server-side Error (500 Internal Server Error)
    logger.info("\n=== TEST CASE 8: Server-side API Failure (HTTP 500) ===")
    error_payload = {
        "management_source": "ONEVIEW",
        "source_host": "http://localhost:8000",
        "api_endpoint": "/rest/server-hardware/1234/error-endpoint",
        "http_method": "GET",
        "action": "get_health"
    }
    res8 = agent.execute(error_payload)
    print(json.dumps(res8, indent=2))
    assert res8["success"] is False
    assert "500" in res8["message"]

    # 9. OneView Async Firmware Update
    logger.info("\n=== TEST CASE 9: HPE OneView Async Firmware Update ===")
    oneview_fw_payload = {
        "management_source": "ONEVIEW",
        "source_host": "http://localhost:8000",
        "api_endpoint": "/rest/server-hardware/1234/firmware",
        "http_method": "PUT",
        "action": "update_firmware",
        "credential_ref": "oneview_token_fw_update",
        "serial_number": "ABC123"
    }
    res9 = agent.execute(oneview_fw_payload)
    print(json.dumps(res9, indent=2))
    assert res9["success"] is True

    logger.info("\n=== ALL TEST CASES COMPLETED SUCCESSFULLY ===")


if __name__ == "__main__":
    # Start generator OneView mock server in a daemon thread on port 8000
    ov_thread = threading.Thread(
        target=run_uvicorn_server,
        args=(oneview_app, 8000),
        daemon=True
    )
    ov_thread.start()

    # Start generator COM mock server in a daemon thread on port 8001
    com_thread = threading.Thread(
        target=run_uvicorn_server,
        args=(compute_ops_app, 8001),
        daemon=True
    )
    com_thread.start()

    # Allow servers a moment to bind
    time.sleep(1.0)

    # Run the validation suite
    try:
        execute_test_cases()
    except Exception as e:
        logger.error(f"Test suite failed: {str(e)}", exc_info=True)
        sys.exit(1)
