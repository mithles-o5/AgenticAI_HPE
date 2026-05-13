# Combined MCP Server — HPE OneView SSO + Authorization

This is the single, unified MCP server that combines:
- **SSO Login** via Auth0 (browser-based)
- **Hardware Management** via authorization backend (list/power/reboot servers)

---

## Architecture

```
Claude / AI Agent
       │
       ▼
mcp_server/mcp_server.py   ← Single entry point (THIS FILE)
       │
       ├── Auth0 (login)   → https://dev-m8h0kmfpfmbtdhoq.us.auth0.com
       │
       └── Authorization Backend → http://127.0.0.1:8001
                │
                ├── authorization/main.py         (FastAPI backend)
                ├── authorization/policy_engine.py (RBAC + ABAC)
                ├── authorization/hardware_mock.py (Mock HPE servers)
                └── authorization/roles.json       (User role mapping)
```

---

## How to Run

### Step 1 — Start the Authorization Backend
Open a terminal and run:
```bash
cd authorization
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

### Step 2 — Register this MCP Server with Claude Desktop
Add the following to your Claude Desktop `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "hpe-combined": {
      "command": "python",
      "args": ["d:\\HPE CPP\\MCP_Integrated\\mcp_server\\mcp_server.py"]
    }
  }
}
```

### Step 3 — Use the Tools in Claude
1. `sso_login` — Opens browser → Log in via Auth0 → Token auto-saved
2. `check_access` — Verify your identity and token
3. `list_servers` — List all mock HPE servers
4. `power_on` — Power on a server (e.g. `server01`)
5. `reboot_server` — Reboot a server (e.g. `server01`)

---

## Connection Points

| What | Where |
|---|---|
| Auth0 Domain | `dev-m8h0kmfpfmbtdhoq.us.auth0.com` |
| Auth0 Client ID | `De3dgvX4Szp5rPY2qwwRUlXHe1kEK4cy` |
| Callback URL | `http://127.0.0.1:8080/callback` |
| Authorization Backend | `http://127.0.0.1:8001` |
| Token file | `.auth_token` (auto-created after login) |
| Roles config | `authorization/roles.json` |
