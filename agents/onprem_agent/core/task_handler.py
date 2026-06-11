import logging
from models.task_request import TaskRequest
from models.task_response import TaskResponse
from core.skill_executor import SkillExecutor

logger = logging.getLogger("onprem_agent.task_handler")

class TaskHandler:
    def __init__(self):
        self.executor = SkillExecutor()

    async def handle_task(self, request: TaskRequest) -> TaskResponse:
        """
        Receives Pydantic request model, delegates to the SkillExecutor,
        and serialises the outcome back into a Pydantic TaskResponse.
        """
        logger.info(f"Received task request: ID={request.task_id}, Action={request.action}, Provider={request.provider}")
        result_dict = await self.executor.execute_task(request)
        return TaskResponse(**result_dict)
