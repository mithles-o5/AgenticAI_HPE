"""
Full dry-run of mcp_server.py import chain.
Simulates exactly what mcp_server.py does at startup.
"""
import sys, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# mcp_server.py lives in mcp_server/ so parent is ROOT
ROOT_DIR = os.path.normpath(os.path.join(BASE_DIR, ".."))
MCP_DIR  = os.path.join(ROOT_DIR, "mcp_server")

for p in [ROOT_DIR,
          os.path.join(ROOT_DIR, "authentication"),
          os.path.join(ROOT_DIR, "authorization"),
          os.path.join(ROOT_DIR, "resource_resolver"),
          os.path.join(ROOT_DIR, "task_planner"),
          os.path.join(ROOT_DIR, "execution_engine")]:
    sys.path.insert(0, p)

os.chdir(MCP_DIR)  # mcp_server.py expects cwd = mcp_server/

print("=== MCP Server Startup Dry-Run ===\n")
all_ok = True

tests = [
    ("db_manager",        lambda: __import__("db").db_manager),
    ("db_loader",         lambda: __import__("db_loader").load_registry_from_db()),
    ("ResourceCache",     lambda: __import__("cache").ResourceCache()),
    ("ResourceResolver",  lambda: __import__("resolver").ResourceResolver(
                              registry=__import__("db_loader").load_registry_from_db(),
                              cache=__import__("cache").ResourceCache())),
    ("AgentDispatcher",   lambda: __import__("execution_engine").AgentDispatcher()),
    ("QueryAgent",        lambda: __import__("query_agent").QueryAgent),
    ("TaskPlanner",       lambda: __import__("planner").TaskPlanner),
    ("errors",            lambda: __import__("errors").ResolverError),
]

for name, fn in tests:
    try:
        result = fn()
        extra = ""
        if name == "db_manager":
            extra = f"  pg_available={result._pg_available}"
        elif name == "db_loader":
            extra = f"  type={type(result).__name__}"
        print(f"  PASS  {name}{extra}")
    except Exception as e:
        print(f"  FAIL  {name}: {e}")
        all_ok = False

print()
if all_ok:
    print("ALL CLEAR - MCP server will start cleanly!")
else:
    print("SOME FAILURES - MCP server will still crash on reconnect. Fix above.")
