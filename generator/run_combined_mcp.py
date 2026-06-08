import os
import sys
import subprocess
import time
import asyncio
import importlib.machinery
import importlib.util
from mcp.server.fastmcp import FastMCP

generator_dir = os.path.dirname(os.path.abspath(__file__))
servers_dir = os.path.join(generator_dir, "servers")

def get_mcp_tools(mcp_instance):
    # Try mcp.server.fastmcp (official SDK)
    if hasattr(mcp_instance, "_tool_manager") and hasattr(mcp_instance._tool_manager, "_tools"):
        return list(mcp_instance._tool_manager._tools.values())
    # Try fastmcp (alternative package)
    if hasattr(mcp_instance, "local_provider") and hasattr(mcp_instance.local_provider, "_components"):
        return [c for c in mcp_instance.local_provider._components.values() if c.__class__.__name__ == "FunctionTool"]
    return []


def main():
    print("==================================================")
    print(" Combined Plug-and-Play MCP Server Runner")
    print("==================================================\n")

    # 1. Scan for generated mock servers
    if not os.path.exists(servers_dir):
        print(f"[ERROR] Servers directory '{servers_dir}' does not exist.")
        return

    server_names = []
    for entry in os.listdir(servers_dir):
        full_path = os.path.join(servers_dir, entry)
        if os.path.isdir(full_path):
            main_py = os.path.join(full_path, "main.py")
            mcp_py = os.path.join(full_path, "mcp_integration.py")
            if os.path.exists(main_py) and os.path.exists(mcp_py):
                server_names.append(entry)

    server_names.sort()
    if not server_names:
        print("[ERROR] No valid mock servers with main.py and mcp_integration.py found.")
        return

    print(f"[+] Found {len(server_names)} plug-and-play mock servers: {', '.join(server_names)}")

    # 2. Start FastAPI mock servers on sequential ports
    start_port = start_port_num = 8000
    subprocesses = []
    server_ports = {}

    print("\n[+] Launching FastAPI mock servers...")
    for idx, name in enumerate(server_names):
        port = start_port_num + idx
        server_ports[name] = port
        server_path = os.path.join(servers_dir, name)
        
        print(f"    -> Starting '{name}' FastAPI mock server on port {port}...")
        
        # Start uvicorn as a subprocess
        cmd = [sys.executable, "-m", "uvicorn", "main:app", "--port", str(port)]
        proc = subprocess.Popen(
            cmd,
            cwd=server_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        subprocesses.append(proc)

    # Stagger a bit for servers to bind ports
    print("[+] Waiting 3 seconds for mock servers to initialize...")
    time.sleep(3)

    # 3. Create the central unified FastMCP server
    combined_mcp = FastMCP("combined-mock-servers")
    registered_tool_names = set()

    print("\n[+] Dynamically loading MCP tool integrations...")
    for name in server_names:
        port = server_ports[name]
        server_path = os.path.join(servers_dir, name)
        mcp_py_path = os.path.join(server_path, "mcp_integration.py")
        
        # Load the module dynamically
        module_name = f"servers.{name}.mcp_integration"
        loader = importlib.machinery.SourceFileLoader(module_name, mcp_py_path)
        spec = importlib.util.spec_from_loader(loader.name, loader)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        loader.exec_module(module)
        
        # Override the target API base URL for this mock server
        module.API_BASE_URL = f"http://localhost:{port}"
        
        # Get its registered tools
        local_mcp = getattr(module, "mcp", None)
        if not local_mcp:
            print(f"    [!] Warning: '{name}' does not export a valid FastMCP object.")
            continue
            
        local_tools = get_mcp_tools(local_mcp)
        print(f"    -> Loading {len(local_tools)} tools from '{name}' (pointing to port {port})...")
        
        for tool in local_tools:
            # Handle naming conflicts by prefixing the server name
            tool_name = tool.name
            if tool_name in registered_tool_names:
                tool_name = f"{name}_{tool_name}"
                
            registered_tool_names.add(tool_name)
            
            # Register on the central combined server
            combined_mcp.tool(name=tool_name, description=tool.description)(tool.fn)

    print(f"\n[OK] Combined MCP server initialized with {len(registered_tool_names)} total tools.")
    
    # 4. Run the combined server and handle cleanup on exit
    try:
        print("\n[+] Starting Combined MCP Server (stdio mode)...")
        combined_mcp.run()
    finally:
        print("\n[-] Shutting down all mock server subprocesses...")
        for proc in subprocesses:
            proc.terminate()
            try:
                proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                proc.kill()
        print("[OK] Subprocesses terminated.")

if __name__ == "__main__":
    main()
