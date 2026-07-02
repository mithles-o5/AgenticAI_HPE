import structlog
import time
from models.task_request import TaskRequest, Action
from models.task_response import TaskResponse, ServerMetrics, StatusLevel
from core.execution_engine import ExecutionEngine
from core.normalization import normalize_metrics
from core.anomaly_detection import detect_anomalies

logger = structlog.get_logger()

class TaskHandler:
    def __init__(self) -> None:
        self.engine = ExecutionEngine()

    async def handle(self, request: TaskRequest) -> TaskResponse:
        start_time = time.perf_counter()
        task_id = request.task_id
        
        log = logger.bind(
            task_id=task_id,
            agent_type="server",
            action=request.action.value if hasattr(request.action, "value") else str(request.action),
            resource_type=request.resource_type.value if hasattr(request.resource_type, "value") else str(request.resource_type),
            resource_id=request.resource_id
        )
        
        log.info("Received incoming task request")

        try:
            raw_result = {}
            action_val = request.action.value if hasattr(request.action, "value") else str(request.action)
            actions_taken = [action_val]
            errors = []
            
            if action_val in (Action.FETCH_METRICS.value, "FETCH_METRICS", "STATUS"):
                if request.provider in ("mock", "mock_server", "default"):
                    request.parameters["api_path"] = f"/redfish/v1/systems/{request.resource_id}"
                    request.parameters["http_method"] = "GET"
                raw_result = self.engine.fetch_metrics(request)
            elif action_val in (Action.HEALTH_CHECK.value, "HEALTH_CHECK"):
                raw_result = self.engine.health_check(request)
            elif action_val in (Action.EXECUTE_ACTION.value, "EXECUTE_ACTION", "ON", "OFF", "RESET", "COLD_BOOT", "MOUNT_VIRTUAL_MEDIA", "CREATE", "ALLOCATE", "DELETE", "DEALLOCATE"):
                # Handle power operations
                if action_val in ("ON", "OFF", "RESET", "COLD_BOOT"):
                    request.parameters["action_type"] = "power_action"
                    request.parameters["action_verb"] = action_val.lower()
                    request.parameters["power_state"] = action_val.lower()
                    reset_type_map = {"ON": "On", "OFF": "ForceOff", "RESET": "GracefulRestart", "COLD_BOOT": "PowerCycle"}
                    request.parameters["payload"] = {"ResetType": reset_type_map.get(action_val, "GracefulRestart")}
                    if request.provider in ("mock", "mock_server", "default"):
                        request.parameters["api_path"] = f"/redfish/v1/systems/{request.resource_id}/actions/computersystem.reset"
                        request.parameters["http_method"] = "POST"
                # Handle virtual media mount
                elif action_val == "MOUNT_VIRTUAL_MEDIA":
                    query_str = request.parameters.get("query", "")
                    url_match = re.search(r'(https?://[^\s\'"]+)', query_str)
                    media_url = url_match.group(1) if url_match else ""
                    media_type = "CD" if re.search(r"\b(iso|cd|dvd|cdrom)\b", query_str, re.IGNORECASE) else "USBStick"
                    request.parameters["action_type"] = "virtual_media"
                    request.parameters["media_url"] = media_url
                    request.parameters["device_type"] = media_type
                    request.parameters["payload"] = {"Image": media_url, "TransferProtocolType": "HTTP", "Inserted": True, "WriteProtected": True}
                    if request.provider in ("mock", "mock_server", "default"):
                        request.parameters["api_path"] = f"/redfish/v1/managers/{request.resource_id}/virtualmedia/2/actions/virtualmedia.insertmedia"
                        request.parameters["http_method"] = "POST"
                # Handle create/allocate
                elif action_val in ("CREATE", "ALLOCATE"):
                    request.parameters["action_verb"] = action_val.lower()
                    request.parameters["action_type"] = "create"
                    if request.provider in ("mock", "mock_server", "default"):
                        request.parameters["api_path"] = f"/redfish/v1/systems"
                        request.parameters["http_method"] = "POST"
                # Handle delete/deallocate
                elif action_val in ("DELETE", "DEALLOCATE"):
                    request.parameters["action_verb"] = action_val.lower()
                    request.parameters["action_type"] = "delete"
                    if request.provider in ("mock", "mock_server", "default"):
                        request.parameters["api_path"] = f"/redfish/v1/systems/{request.resource_id}"
                        request.parameters["http_method"] = "DELETE"
                        
                raw_result = self.engine.execute_action(request)
                if request.parameters.get("action_type") == "power_action" or request.parameters.get("action_verb"):
                    action_verb = request.parameters.get("power_state") or request.parameters.get("action_verb")
                    actions_taken.append(f"power_{action_verb.lower()}")
            elif action_val in (Action.DISCOVER_INVENTORY.value, "DISCOVER_INVENTORY"):
                if request.provider in ("mock", "mock_server", "default"):
                    request.parameters["api_path"] = f"/redfish/v1/systems/{request.resource_id}"
                    request.parameters["http_method"] = "GET"
                raw_result = self.engine.discover_inventory(request)
            elif action_val in (Action.FETCH_EVENT_LOG.value, "FETCH_EVENT_LOG", "CLEAR_EVENT_LOG"):
                request.resource_type = ResourceType.EVENT_LOG
                query_str = request.parameters.get("query", "")
                request.parameters["clear"] = (action_val == "CLEAR_EVENT_LOG")
                sev_match = re.search(r"\b(critical|warning|info|fatal)\b", query_str, re.IGNORECASE)
                if sev_match:
                    request.parameters["severity"] = sev_match.group(1).lower()
                if request.provider in ("mock", "mock_server", "default"):
                    request.parameters["api_path"] = f"/redfish/v1/systems/{request.resource_id}/logservices/iml/entries"
                    request.parameters["http_method"] = "GET"
                raw_result = self.engine.fetch_event_log(request)
            elif action_val in (Action.SYNC_CMDB.value, "SYNC_CMDB"):
                if request.provider in ("mock", "mock_server", "default"):
                    request.parameters["api_path"] = f"/redfish/v1/systems/{request.resource_id}"
                    request.parameters["http_method"] = "GET"
                raw_result = await self.engine.sync_cmdb(request)
            elif action_val in ("LIST", "LIST_RESOURCES"):
                raw_result = self.engine.list_resources(request)
                if isinstance(raw_result, dict) and "devices" in raw_result:
                    inventory_data = raw_result.get("devices", [])
                    return TaskResponse(
                        task_id=task_id,
                        status="success",
                        resource_type=request.resource_type.value,
                        resource_id="list",
                        region=request.region,
                        status_level=StatusLevel.HEALTHY,
                        inventory=inventory_data,
                        insights=[f"Total matched: {raw_result.get('total', len(inventory_data))}"]
                    )
            else:
                errors.append(f"Unsupported action: {request.action}")

            # Check if execution engine reported failed status
            if isinstance(raw_result, dict) and raw_result.get("status") == "failed":
                errors.append(raw_result.get("error", "Execution engine failed"))
                return TaskResponse(
                    task_id=task_id,
                    status="failed",
                    resource_type=request.resource_type.value,
                    resource_id=request.resource_id,
                    region=request.region,
                    status_level=StatusLevel.CRITICAL,
                    errors=errors
                )

            # Normalize raw output to ServerMetrics model
            if action_val in (Action.HEALTH_CHECK.value, "HEALTH_CHECK"):
                # Merge health status and sensors
                health_data = raw_result.get("health", {})
                sensors = raw_result.get("sensors", [])
                
                # Overall health
                metrics = normalize_metrics(health_data)
                # Map sensors list to metrics
                from models.task_response import SensorReading
                from core.normalization import map_health_status
                metrics.sensors = [
                    SensorReading(
                        name=s.get("name"),
                        reading=float(s.get("reading", 0.0)),
                        units=s.get("units", ""),
                        status=map_health_status(s.get("status"))
                    )
                    for s in sensors
                ]
            elif action_val in (Action.DISCOVER_INVENTORY.value, "DISCOVER_INVENTORY"):
                metrics = ServerMetrics(inventory=raw_result.get("inventory"))
            elif action_val in (Action.FETCH_EVENT_LOG.value, "FETCH_EVENT_LOG", "CLEAR_EVENT_LOG"):
                events = raw_result.get("events", [])
                metrics = ServerMetrics(
                    event_count=len(events),
                    critical_event_count=sum(1 for e in events if str(e.get("severity")).lower() in ("critical", "fatal", "fail")),
                    recent_events=events
                )
            else:
                metrics = normalize_metrics(raw_result)

            # Run Anomaly Detection
            status_level, insights = detect_anomalies(metrics)
            
            duration_ms = int((time.perf_counter() - start_time) * 1000)
            log.info("Task completed successfully", duration_ms=duration_ms, status_level=status_level.value)

            return TaskResponse(
                task_id=task_id,
                status="success",
                resource_type=request.resource_type.value,
                resource_id=request.resource_id,
                region=request.region,
                metrics=metrics,
                actions_taken=actions_taken,
                status_level=status_level,
                insights=insights,
                errors=errors
            )

        except Exception as exc:
            duration_ms = int((time.perf_counter() - start_time) * 1000)
            log.error("Task failed with exception", duration_ms=duration_ms, error=str(exc))
            return TaskResponse(
                task_id=task_id,
                status="failed",
                resource_type=request.resource_type.value,
                resource_id=request.resource_id,
                region=request.region,
                status_level=StatusLevel.CRITICAL,
                errors=[str(exc)]
            )
