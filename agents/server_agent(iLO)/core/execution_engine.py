import subprocess
import httpx
import structlog
from typing import Dict, Any, List
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type, before_sleep_log
from models.task_request import TaskRequest
from core.adapter_manager import get_adapter
from config.settings import settings

logger = structlog.get_logger()

# Define which exceptions should trigger retries
def should_retry_exception(exception: Exception) -> bool:
    # Do NOT retry on 401 or 404 HTTP errors
    if isinstance(exception, httpx.HTTPStatusError):
        if exception.response.status_code in (401, 404):
            return False
    # Do NOT retry on unsupported device or adapter operations
    err_str = str(exception).lower()
    if "not supported" in err_str or "unsupported" in err_str:
        return False
    
    return isinstance(
        exception, 
        (httpx.HTTPError, ConnectionError, TimeoutError, subprocess.TimeoutExpired, RuntimeError)
    )

class ExecutionEngine:
    def __init__(self) -> None:
        self.max_attempts = settings.MAX_RETRIES
        self.backoff_mult = settings.RETRY_BACKOFF_MULTIPLIER

    def _get_retry_decorator(self, task_id: str):
        # We build a dynamic retry decorator using settings
        return retry(
            stop=stop_after_attempt(self.max_attempts),
            wait=wait_exponential(multiplier=self.backoff_mult, min=1, max=10),
            retry=retry_if_exception_type(Exception), # Checked dynamically inside wait/stop or via predicate
            retry_error_callback=lambda retry_state: retry_state.outcome.result(),
            before_sleep=before_sleep_log(logger, logging.INFO)
        )

    def fetch_metrics(self, request: TaskRequest) -> Dict[str, Any]:
        task_id = request.task_id
        log = logger.bind(task_id=task_id, agent_type="server")
        
        try:
            adapter = get_adapter(request.provider, request.credentials_ref)
            
            # We wrap the call in a retryable function
            @retry(
                stop=stop_after_attempt(self.max_attempts),
                wait=wait_exponential(multiplier=self.backoff_mult),
                retry=retry_if_exception_type(Exception),
                reraise=True
            )
            def _call_adapter():
                log.info("Executing fetch_metrics", resource_id=request.resource_id, resource_type=request.resource_type)
                is_mock = adapter.__class__.__name__ == "MockAdapter"
                if request.resource_type == "sensor":
                    return {"sensors": adapter.fetch_sensors(request.resource_id, request.parameters) if is_mock else adapter.fetch_sensors(request.resource_id)}
                else:
                    return adapter.fetch_system_metrics(request.resource_id, request.parameters) if is_mock else adapter.fetch_system_metrics(request.resource_id)

            return _call_adapter()
        except Exception as e:
            log.error("fetch_metrics execution failed", error=str(e))
            return {"status": "failed", "error": str(e)}

    def health_check(self, request: TaskRequest) -> Dict[str, Any]:
        task_id = request.task_id
        log = logger.bind(task_id=task_id, agent_type="server")
        
        try:
            adapter = get_adapter(request.provider, request.credentials_ref)
            
            @retry(
                stop=stop_after_attempt(self.max_attempts),
                wait=wait_exponential(multiplier=self.backoff_mult),
                retry=retry_if_exception_type(Exception),
                reraise=True
            )
            def _call_adapter():
                log.info("Executing health_check", resource_id=request.resource_id)
                is_mock = adapter.__class__.__name__ == "MockAdapter"
                health = adapter.health_check(request.resource_id, request.parameters) if is_mock else adapter.health_check(request.resource_id)
                sensors = adapter.fetch_sensors(request.resource_id, request.parameters) if is_mock else adapter.fetch_sensors(request.resource_id)
                return {"health": health, "sensors": sensors}

            return _call_adapter()
        except Exception as e:
            log.error("health_check execution failed", error=str(e))
            return {"status": "failed", "error": str(e)}

    def execute_action(self, request: TaskRequest) -> Dict[str, Any]:
        task_id = request.task_id
        log = logger.bind(task_id=task_id, agent_type="server")
        
        try:
            adapter = get_adapter(request.provider, request.credentials_ref)
            action_type = request.parameters.get("action_type")
            
            @retry(
                stop=stop_after_attempt(self.max_attempts),
                wait=wait_exponential(multiplier=self.backoff_mult),
                retry=retry_if_exception_type(Exception),
                reraise=True
            )
            def _call_adapter():
                log.info("Executing action", resource_id=request.resource_id, action_type=action_type)
                is_mock = adapter.__class__.__name__ == "MockAdapter"
                if action_type == "power_action" or request.parameters.get("action_verb") in ("on", "off", "reset", "cold_boot"):
                    power_state = request.parameters.get("power_state") or request.parameters.get("action_verb")
                    return adapter.execute_power_action(request.resource_id, power_state, request.parameters) if is_mock else adapter.execute_power_action(request.resource_id, power_state)
                elif action_type == "boot_config":
                    return adapter.set_boot_order(request.resource_id, request.parameters.get("boot_order", []), request.parameters) if is_mock else adapter.set_boot_order(request.resource_id, request.parameters.get("boot_order", []))
                elif action_type == "virtual_media":
                    return adapter.mount_virtual_media(
                        request.resource_id, 
                        request.parameters.get("media_url"), 
                        request.parameters.get("device_type"),
                        request.parameters
                    ) if is_mock else adapter.mount_virtual_media(
                        request.resource_id, 
                        request.parameters.get("media_url"), 
                        request.parameters.get("device_type")
                    )
                elif request.parameters.get("action_verb") in ("create", "delete", "allocate", "deallocate"):
                    if is_mock:
                        action_verb = request.parameters.get("action_verb")
                        if action_verb in ("create", "allocate"):
                            payload = request.parameters.get("payload") or {}
                            if adapter.__class__.__name__ == "MockAdapter":
                                return adapter._dynamic_call("POST", "/redfish/v1/systems", request.resource_id, payload, request.parameters.get("base_url", ""))
                            else:
                                resp = adapter._request("POST", "/systems", payload)
                                return resp.json() if resp.is_success else {"status": "failed", "error": resp.text}
                        else:  # delete, deallocate
                            if adapter.__class__.__name__ == "MockAdapter":
                                return adapter._dynamic_call("DELETE", f"/redfish/v1/systems/{request.resource_id}", request.resource_id, {}, request.parameters.get("base_url", ""))
                            else:
                                resp = adapter._request("DELETE", f"/systems/{request.resource_id}")
                                return resp.json() if resp.is_success else {"status": "failed", "error": resp.text}
                    else:
                        return {"status": "failed", "error": f"Action {request.parameters.get('action_verb')} not supported on physical BMC."}
                else:
                    raise ValueError(f"Unknown action_type: {action_type}")


            return _call_adapter()
        except Exception as e:
            log.error("execute_action execution failed", error=str(e))
            return {"status": "failed", "error": str(e)}

    def discover_inventory(self, request: TaskRequest) -> Dict[str, Any]:
        task_id = request.task_id
        log = logger.bind(task_id=task_id, agent_type="server")
        
        try:
            adapter = get_adapter(request.provider, request.credentials_ref)
            
            @retry(
                stop=stop_after_attempt(self.max_attempts),
                wait=wait_exponential(multiplier=self.backoff_mult),
                retry=retry_if_exception_type(Exception),
                reraise=True
            )
            def _call_adapter():
                log.info("Executing discover_inventory", filters=request.parameters)
                filters = dict(request.parameters)
                filters["resource_id"] = request.resource_id
                is_mock = adapter.__class__.__name__ == "MockAdapter"
                return {"inventory": adapter.discover_inventory(filters, request.parameters) if is_mock else adapter.discover_inventory(filters)}

            return _call_adapter()
        except Exception as e:
            log.error("discover_inventory execution failed", error=str(e))
            return {"status": "failed", "error": str(e)}

    def fetch_event_log(self, request: TaskRequest) -> Dict[str, Any]:
        task_id = request.task_id
        log = logger.bind(task_id=task_id, agent_type="server")
        
        try:
            adapter = get_adapter(request.provider, request.credentials_ref)
            
            @retry(
                stop=stop_after_attempt(self.max_attempts),
                wait=wait_exponential(multiplier=self.backoff_mult),
                retry=retry_if_exception_type(Exception),
                reraise=True
            )
            def _call_adapter():
                log.info("Executing fetch_event_log", resource_id=request.resource_id)
                severity = request.parameters.get("severity")
                is_mock = adapter.__class__.__name__ == "MockAdapter"
                events = adapter.fetch_event_log(request.resource_id, severity, request.parameters) if is_mock else adapter.fetch_event_log(request.resource_id, severity)
                
                if request.parameters.get("clear") is True:
                    log.info("Clearing event log after fetch", resource_id=request.resource_id)
                    adapter.clear_event_log(request.resource_id, request.parameters) if is_mock else adapter.clear_event_log(request.resource_id)
                    
                return {"events": events}

            return _call_adapter()
        except Exception as e:
            log.error("fetch_event_log execution failed", error=str(e))
            return {"status": "failed", "error": str(e)}

    async def sync_cmdb(self, request: TaskRequest) -> Dict[str, Any]:
        task_id = request.task_id
        log = logger.bind(task_id=task_id, agent_type="server")
        
        try:
            adapter = get_adapter(request.provider, request.credentials_ref)
            log.info("Executing sync_cmdb", resource_id=request.resource_id)
            is_mock = adapter.__class__.__name__ == "MockAdapter"
            inv = adapter.discover_inventory({"resource_id": request.resource_id}, request.parameters) if is_mock else adapter.discover_inventory({"resource_id": request.resource_id})
            metrics = adapter.fetch_system_metrics(request.resource_id, request.parameters) if is_mock else adapter.fetch_system_metrics(request.resource_id)
            
            payload = {
                "inventory": inv,
                "metrics": metrics
            }
            
            # Write to CMDB
            cmdb_url = settings.CMDB_URL
            async with httpx.AsyncClient() as client:
                resp = await client.put(
                    f"{cmdb_url}/resources/{request.resource_id}/metrics",
                    json={"metrics": payload, "status_level": "healthy", "agent": "server-agent"},
                    timeout=10.0
                )
                resp.raise_for_status()
                
            return {"status": "success", "synced": True}
        except Exception as e:
            log.error("sync_cmdb execution failed", error=str(e))
            return {"status": "failed", "error": str(e)}
