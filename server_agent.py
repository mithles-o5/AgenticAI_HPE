import logging
from typing import Dict, Any
from models import validate_payload, ValidationError
from adapter_factory import AdapterFactory

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)-8s %(name)s - %(message)s")
logger = logging.getLogger("server-agent")

class ServerAgent:
    """
    Standalone Server Agent for Datacenter Management.
    Receives fully resolved context, validates the input payload,
    delegates the execution to the appropriate platform adapter,
    and returns a standardized normalized response.
    """

    def __init__(self, poll_interval: float = 1.0, poll_timeout: float = 30.0):
        """
        Initialize the server agent.
        :param poll_interval: Sleep interval (seconds) when polling asynchronous tasks.
        :param poll_timeout: Maximum time (seconds) to wait for an asynchronous task.
        """
        self.poll_interval = poll_interval
        self.poll_timeout = poll_timeout
        logger.info(f"ServerAgent initialized (poll_interval={poll_interval}s, poll_timeout={poll_timeout}s)")

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validates the payload, obtains the adapter, and runs execution.
        Guarantees that a normalized JSON-serializable response structure is returned.
        """
        logger.info("ServerAgent received execution request.")
        
        # 1. Validate the execution payload fields
        try:
            validated_payload = validate_payload(payload)
            logger.debug(f"Payload validation succeeded for action: {validated_payload['action']}")
        except ValidationError as val_err:
            logger.error(f"Payload validation failed: {val_err.message}")
            return val_err.to_dict()
        except Exception as exc:
            # Handle non-dict payload or other parsing errors
            action = payload.get("action", "unknown") if isinstance(payload, dict) else "unknown"
            logger.error(f"Unexpected pre-validation failure: {str(exc)}")
            return {
                "success": False,
                "action": action,
                "status": "failed",
                "message": f"Pre-validation failure: {str(exc)}",
                "error": {"exception_type": type(exc).__name__, "details": str(exc)}
            }

        # 2. Select the correct adapter and delegate execution
        try:
            management_source = validated_payload["management_source"]
            logger.info(f"Selecting adapter for source: {management_source}")
            
            adapter = AdapterFactory.get(
                management_source,
                poll_interval=self.poll_interval,
                poll_timeout=self.poll_timeout
            )
            
            logger.info(f"Executing operation '{validated_payload['action']}' on endpoint '{validated_payload['api_endpoint']}'")
            result = adapter.execute(validated_payload)
            
            logger.info(f"Execution finished. Success status: {result.get('success')}")
            return result

        except Exception as e:
            logger.error(f"Failed to execute adapter operation: {str(e)}", exc_info=True)
            return {
                "success": False,
                "action": validated_payload["action"],
                "status": "failed",
                "message": f"Server Agent runtime execution error: {str(e)}",
                "error": {"exception": str(e)}
            }
