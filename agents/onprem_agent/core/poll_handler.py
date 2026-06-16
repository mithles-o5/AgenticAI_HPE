import time
import logging
from models.task_request import TaskRequest
from models.task_response import TaskResponse
from core.task_handler import TaskHandler

logger = logging.getLogger("onprem_agent.poll_handler")

class PollHandler:
    def __init__(self, task_handler: TaskHandler = None):
        self.task_handler = task_handler or TaskHandler()

    async def trigger_sync(self, provider: str, credentials_ref: str = None) -> TaskResponse:
        """
        Executes a CMDB sync poll loop trigger for a given provider.
        Routes execution through the standard TaskHandler pipeline.
        """
        task_id = f"poll-sync-{provider}-{int(time.time())}"
        logger.info(f"Triggering background inventory sync via PollHandler for provider '{provider}'. Task ID: {task_id}")
        
        request = TaskRequest(
            task_id=task_id,
            task_type="poll_sync",
            agent_type="onprem",
            provider=provider,
            action="sync_cmdb",
            credentials_ref=credentials_ref,
            parameters={}
        )
        
        response = await self.task_handler.handle_task(request)
        logger.info(f"Poll sync task completed: ID={response.task_id}, status={response.status}")
        return response
