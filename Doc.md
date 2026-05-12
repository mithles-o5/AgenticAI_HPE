# Resource Resolver Documentation

## 1. What This Project Does

This project is an HPE-only resource resolver for Claude MCP.

It takes a natural language command like:

```text
turn on rack-server-04
```

and converts it into a structured response containing:

- The matched HPE server
- The action to perform
- The selected HPE protocol
- The target API endpoint
- The credential reference
- Basic hardware and state information

Current scope:

```text
Resolve command -> Build execution context -> Return JSON to Claude
```

It does not directly power on, power off, or reboot real hardware yet.

## 2. Main Files

```text
mcp_tool.py       MCP server entry point for Claude
resolver.py       Main resolver pipeline
selector.py       Action classification and protocol selection
sample_data.py    Sample HPE server inventory
registry.py       Resource lookup by name, alias, UUID, serial, or fuzzy match
cache.py          In-memory TTL cache
records.py        Data models used across the project
enums.py          HPE enums like protocol, action, health, deployment type
errors.py         Custom resolver errors
requirements.txt  Python dependency list
.env.template     Example environment variables
resolver.log      Runtime log file created by the MCP server
```

## 3. Install Dependencies

From the project folder:

```powershell
pip install -r requirements.txt
```

Current required package:

```text
mcp
```

## 4. Configure Claude Desktop

Claude Desktop should run `mcp_tool.py` using your project Python environment.

Example MCP config:

```json
{
  "mcpServers": {
    "resource-resolver": {
      "command": "D:/resource_resolver/.venv/Scripts/python.exe",
      "args": [
        "D:/resource_resolver/mcp_tool.py"
      ]
    }
  }
}
```

Adjust the Python path if your virtual environment is somewhere else.

## 5. Start Claude and Test

After adding the MCP config:

1. Restart Claude Desktop.
2. Open a new chat.
3. Ask Claude to use the resource resolver.
4. Try one of these commands:

```text
turn on rack-server-04
```

```text
reboot blade-enclosure-01
```

```text
status synergy-compute-03
```

```text
power on cloud-compute-web-01
```

## 6. Available MCP Tools

### resolve_resource

Resolves a natural language command into an execution context.

Example request:

```json
{
  "query": "turn on rack-server-04"
}
```

Example important response fields:

```json
{
  "status": "resolved",
  "api_endpoint": "https://ilo-rack-04.mgmt.local/rest/v1/server-hardware/b2c3d4e5-0002-4f6a-9012-bcdef0123402",
  "protocol": "OneView",
  "resource": {
    "name": "rack-server-04",
    "vendor": "HPE"
  },
  "action": {
    "category": "Operational",
    "action": "On"
  }
}
```

### list_servers

Lists all HPE servers currently registered in `sample_data.py`.

## 7. Routing Logic

The resolver currently supports HPE only.

Routing is based on deployment type:

```text
On-Premises -> OneView
Cloud       -> COMS
```

Examples:

```text
rack-server-04        -> OneView
blade-enclosure-01    -> OneView
synergy-compute-01    -> OneView
cloud-compute-web-01  -> COMS
```

## 8. Action Mapping

Examples of supported action words:

```text
turn on / power on / start      -> On
turn off / power off / shutdown -> Off
reboot / restart / reset        -> Reset
cold boot                       -> ColdBoot
status / check / state          -> Status
create / provision              -> Create
allocate / deploy               -> Allocate
deallocate / release            -> Deallocate
delete / destroy / deprovision  -> Delete
```

If the resolver cannot understand the action, it defaults to:

```text
Status
```

## 9. Sample Resources

Current sample resources are defined in `sample_data.py`.

Common resource names:

```text
rack-server-04
blade-enclosure-01
synergy-compute-01
synergy-compute-02
synergy-compute-03
cloud-compute-web-01
```

Some aliases also work:

```text
server04
dl380-rack04
blade01
synergy01
synergy02
synergy03
web-server-01
cloud-web-01
```

Serial numbers can also be used.

## 10. Credentials

The resolver does not store real passwords.

It returns a credential reference like:

```text
secret/datacenter/rack-04/ilo
```

This means:

```text
The future execution layer should fetch the real secret from a vault.
```

For the current resolver, a real credential store is not required.

## 11. Logs

The file `resolver.log` stores runtime logs.

This is important because MCP uses stdout for JSON communication, so normal logs should not be printed to the terminal.

If something fails in Claude, check:

```text
resolver.log
```

You can delete this file anytime. It will be recreated when the MCP server runs.

## 12. Current Limitation

This project currently resolves commands only.

It does not yet call:

```text
HPE OneView API
HPE Compute Ops API
```

So this command:

```text
turn on rack-server-04
```

does not actually turn on the server yet.

It returns the endpoint and action needed for a future executor to perform the real operation.

## 13. Next Step

The next major feature would be an execution layer:

```text
Resolver output -> HPE API client -> Real power action -> Action result
```

That layer would need:

- Real HPE API authentication
- Vault or secret lookup
- OneView API calls
- Compute Ops API calls
- Error handling for failed hardware tasks
