import logging
from core.exceptions import AgentError, SkillError
from core.cred_vault_client import CredVaultClient
from core.adapter_manager import AdapterManager
from core.skill_registry import SKILLS, resolve_skill_name

logger = logging.getLogger("onprem_agent.skill_executor")

class SkillExecutor:
    def __init__(self):
        self.cred_vault = CredVaultClient()
        self.adapter_manager = AdapterManager()

    async def execute_task(self, request) -> dict:
        """
        Executes a task request by resolving the skill, fetching credentials,
        getting the correct adapter, and running the skill.
        Returns a dict matching the TaskResponse structure fields.
        """
        errors = []
        try:
            # 1. Fetch credentials if reference provided
            credentials = {}
            if request.credentials_ref:
                try:
                    credentials = self.cred_vault.get(request.credentials_ref)
                except Exception as e:
                    logger.error(f"Failed to fetch credentials for ref {request.credentials_ref}: {e}")
                    return {
                        "task_id": request.task_id,
                        "status": "failed",
                        "agent_type": "onprem",
                        "resource_type": request.resource_type,
                        "resource_id": request.resource_id,
                        "region": request.region,
                        "metrics": {},
                        "actions_taken": [],
                        "status_level": "critical",
                        "insights": [],
                        "errors": [f"Credential vault fetch failed: {str(e)}"]
                    }

            # 2. Get the appropriate adapter (raises ValueError if provider is 'default' or missing)
            adapter = self.adapter_manager.get_adapter(request.provider)

            # 3. Resolve the skill
            skill_name = resolve_skill_name(request.action, request.parameters)
            skill = SKILLS.get(skill_name)
            if not skill:
                raise SkillError(f"OASF skill '{skill_name}' is not registered or implemented")

            # 4. Execute the skill
            res = await skill.execute(adapter, request, credentials)
            
            # Form final result structure
            return {
                "task_id": request.task_id,
                "status": res.get("status", "success"),
                "agent_type": "onprem",
                "resource_type": request.resource_type,
                "resource_id": request.resource_id,
                "region": request.region,
                "metrics": res.get("metrics", {}),
                "actions_taken": res.get("actions_taken", []),
                "status_level": res.get("status_level", "healthy"),
                "insights": res.get("insights", []),
                "errors": res.get("errors", []) + errors
            }

        except ValueError as ve:
            # Captures 'provider == default' errors
            logger.error(f"Validation error running task {request.task_id}: {ve}")
            return {
                "task_id": request.task_id,
                "status": "failed",
                "agent_type": "onprem",
                "resource_type": request.resource_type,
                "resource_id": request.resource_id,
                "region": request.region,
                "metrics": {},
                "actions_taken": [],
                "status_level": "critical",
                "insights": [],
                "errors": [f"Validation failed: {str(ve)}"]
            }
        except AgentError as ae:
            logger.error(f"Agent domain error running task {request.task_id}: {ae}")
            return {
                "task_id": request.task_id,
                "status": "failed",
                "agent_type": "onprem",
                "resource_type": request.resource_type,
                "resource_id": request.resource_id,
                "region": request.region,
                "metrics": {},
                "actions_taken": [],
                "status_level": "critical",
                "insights": [],
                "errors": [f"Execution error: {str(ae)}"]
            }
        except Exception as e:
            logger.error(f"Unhandled system error running task {request.task_id}: {e}")
            return {
                "task_id": request.task_id,
                "status": "failed",
                "agent_type": "onprem",
                "resource_type": request.resource_type,
                "resource_id": request.resource_id,
                "region": request.region,
                "metrics": {},
                "actions_taken": [],
                "status_level": "critical",
                "insights": [],
                "errors": [f"System error: {str(e)}"]
            }
