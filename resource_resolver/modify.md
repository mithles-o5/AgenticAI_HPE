# Integration Note

During integration with the mock agent, change the generated API endpoints for both HPE OneView and HPE Compute Ops to match the mock agent's API routes.

Current resolver endpoint format:

```text
OneView:
https://{management_host}/rest/v1/server-hardware/{resource_uuid}

Compute Ops:
https://{compute_ops_host}/compute-ops/v1/servers/{resource_uuid}
```

For local mock-agent integration, `{management_host}` and `{compute_ops_host}` should point to the local mock agent host instead of a real HPE host.

Example:

```text
http://localhost:{mock_agent_port}/...
```

Integration requirement:

```text
Replace the above endpoint formats with the mock agent's expected API endpoint format.
```

The change should be made in this file and function:

```text
File: selector.py
Line: 155
Function: build_endpoint()
```

The resolver should still return the same resource, action, protocol, and credential information. Only the endpoint URL should be adjusted to match the mock agent API.
