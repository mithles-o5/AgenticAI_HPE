"""
Power Operation Executor
=========================
Handles power-on operations for both OneView and CoM managed servers.
Uses different MCP tools based on protocol type.
"""

from __future__ import annotations

import logging
from typing import Optional

from enums import Protocol, PowerAction
from records import ExecutionContext

logger = logging.getLogger(__name__)


class PowerOperationExecutor:
    """
    Orchestrates power operations using protocol-specific handlers.
    """

    def __init__(self):
        self.oneview_handler = OneViewPowerHandler()
        self.coms_handler = COMSPowerHandler()

    def execute_power_operation(
        self,
        ctx: ExecutionContext,
        action: PowerAction = PowerAction.ON,
    ) -> dict:
        """
        Execute power operation based on selected protocol.

        Parameters
        ----------
        ctx    : ExecutionContext from resolver
        action : PowerAction (ON, OFF, RESET, COLD, STATUS)

        Returns
        -------
        Operation result
        """
        protocol = ctx.selected_protocol

        logger.info(
            f"[PowerOps] Executing {action.value} on {ctx.resource_name} "
            f"via {protocol.value} protocol"
        )

        if protocol == Protocol.ONEVIEW:
            return self.oneview_handler.execute(ctx, action)
        elif protocol == Protocol.COMS:
            return self.coms_handler.execute(ctx, action)
        else:
            return {
                "status": "error",
                "error": f"Unsupported protocol: {protocol.value}",
                "resource_uuid": ctx.resource_uuid,
            }


class OneViewPowerHandler:
    """
    OneView-specific power operation handler.
    Uses HPE OneView API for on-premises servers.
    """

    def execute(self, ctx: ExecutionContext, action: PowerAction) -> dict:
        """
        Execute power operation via OneView API.

        Simulates:
        - Authentication to OneView appliance
        - Server lookup by UUID
        - Power state transition
        - Status verification
        """
        logger.info(
            f"[OneView] Power {action.value}: {ctx.resource_name} "
            f"at {ctx.endpoint}"
        )

        try:
            # Simulate OneView API call
            operation_id = self._simulate_oneview_api(ctx, action)

            result = {
                "status": "success",
                "protocol": "OneView",
                "resource_uuid": ctx.resource_uuid,
                "resource_name": ctx.resource_name,
                "action": action.value,
                "operation_id": operation_id,
                "endpoint": ctx.endpoint,
                "message": f"Power {action.value} initiated on {ctx.resource_name} via OneView",
                "deployment_type": "On-Premises",
            }

            logger.info(
                f"[OneView] ✓ Power {action.value} succeeded: {ctx.resource_name} "
                f"(Op ID: {operation_id})"
            )
            return result

        except Exception as e:
            logger.error(f"[OneView] ✗ Power operation failed: {e}")
            return {
                "status": "error",
                "protocol": "OneView",
                "resource_uuid": ctx.resource_uuid,
                "resource_name": ctx.resource_name,
                "error": str(e),
                "endpoint": ctx.endpoint,
            }

    def _simulate_oneview_api(self, ctx: ExecutionContext, action: PowerAction) -> str:
        """
        Simulate OneView API call.
        In production: Use OneView SDK or REST API
        """
        import uuid as _uuid

        # Map action to OneView API call
        action_map = {
            PowerAction.ON: "On",
            PowerAction.OFF: "Off",
            PowerAction.RESET: "Reset",
            PowerAction.COLD: "ColdBoot",
            PowerAction.STATUS: "NoOp",
        }

        api_action = action_map.get(action, "NoOp")
        operation_id = str(_uuid.uuid4())

        logger.debug(
            f"[OneView.API] POST /rest/server-profiles/{ctx.resource_uuid}/powerState "
            f"action={api_action}"
        )

        # Simulated API response time
        return operation_id


class COMSPowerHandler:
    """
    COMS (Compute Ops) Power handler.
    Uses HPE Compute Ops Management Service (cloud-based).
    """

    def execute(self, ctx: ExecutionContext, action: PowerAction) -> dict:
        """
        Execute power operation via COMS API.

        Simulates:
        - Authentication to COMS cloud service
        - Server lookup by resource ID
        - Power state transition
        - Async job tracking
        """
        logger.info(
            f"[COMS] Power {action.value}: {ctx.resource_name} "
            f"via cloud endpoint {ctx.endpoint}"
        )

        try:
            # Simulate COMS API call
            job_id = self._simulate_coms_api(ctx, action)

            result = {
                "status": "success",
                "protocol": "COMS",
                "resource_uuid": ctx.resource_uuid,
                "resource_name": ctx.resource_name,
                "action": action.value,
                "job_id": job_id,
                "endpoint": ctx.endpoint,
                "message": f"Power {action.value} job submitted for {ctx.resource_name} via COMS",
                "deployment_type": "Cloud",
                "async": True,
            }

            logger.info(
                f"[COMS] ✓ Power {action.value} job submitted: {ctx.resource_name} "
                f"(Job ID: {job_id})"
            )
            return result

        except Exception as e:
            logger.error(f"[COMS] ✗ Power operation failed: {e}")
            return {
                "status": "error",
                "protocol": "COMS",
                "resource_uuid": ctx.resource_uuid,
                "resource_name": ctx.resource_name,
                "error": str(e),
                "endpoint": ctx.endpoint,
            }

    def _simulate_coms_api(self, ctx: ExecutionContext, action: PowerAction) -> str:
        """
        Simulate COMS API call.
        In production: Use COMS REST API or SDK
        """
        import uuid as _uuid

        # Map action to COMS API call
        action_map = {
            PowerAction.ON: "powerOn",
            PowerAction.OFF: "powerOff",
            PowerAction.RESET: "powerReset",
            PowerAction.COLD: "hardReset",
            PowerAction.STATUS: "getStatus",
        }

        api_action = action_map.get(action, "getStatus")
        job_id = str(_uuid.uuid4())

        logger.debug(
            f"[COMS.API] POST /api/v1/jobs "
            f"resource={ctx.resource_uuid} action={api_action}"
        )

        return job_id


# Singleton instance
power_executor = PowerOperationExecutor()
