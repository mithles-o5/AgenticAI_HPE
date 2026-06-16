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
            action=request.action.value,
            resource_type=request.resource_type.value,
            resource_id=request.resource_id
        )
        
        log.info("Received incoming task request")

        try:
            raw_result = {}
            actions_taken = [request.action.value]
            errors = []
            
            if request.action == Action.FETCH_METRICS:
                raw_result = self.engine.fetch_metrics(request)
            elif request.action == Action.HEALTH_CHECK:
                raw_result = self.engine.health_check(request)
            elif request.action == Action.EXECUTE_ACTION:
                raw_result = self.engine.execute_action(request)
                if request.parameters.get("action_type") == "power_action" or request.parameters.get("action_verb"):
                    action_verb = request.parameters.get("power_state") or request.parameters.get("action_verb")
                    actions_taken.append(f"power_{action_verb.lower()}")
            elif request.action == Action.DISCOVER_INVENTORY:
                raw_result = self.engine.discover_inventory(request)
            elif request.action == Action.FETCH_EVENT_LOG:
                raw_result = self.engine.fetch_event_log(request)
            elif request.action == Action.SYNC_CMDB:
                raw_result = await self.engine.sync_cmdb(request)
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
            if request.action == Action.HEALTH_CHECK:
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
            elif request.action == Action.DISCOVER_INVENTORY:
                metrics = ServerMetrics(inventory=raw_result.get("inventory"))
            elif request.action == Action.FETCH_EVENT_LOG:
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
