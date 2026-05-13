import os
import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("datacenter-mock")

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

@mcp.tool(description="Get server status by server ID")
def get_server_status(server_id: str):
    try:
        response = requests.get(f"{API_BASE_URL}/servers/{server_id}")
        if response.status_code == 404:
            return {"error": "Server not found"}
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}


@mcp.tool(description="Restart a server")
def restart_server(server_id: str):
    try:
        # Expected /servers/{server_id}/restart to handle restarting
        response = requests.post(f"{API_BASE_URL}/servers/{server_id}/restart")
        if response.status_code == 404:
            return {"error": "Server not found"}
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}


@mcp.tool(description="List all servers")
def list_servers():
    try:
        response = requests.get(f"{API_BASE_URL}/servers")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}


@mcp.tool(description="Retrieve list of users with filtering and pagination options")
def list_users(filter: str = "", limit: int = 300, offset: int = 0):
    try:
        params = {"filter": filter, "limit": limit, "offset": offset}
        response = requests.get(f"{API_BASE_URL}/identity/v1/users", params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Invite a user to a workspace")
def invite_user(email: str, send_welcome_email: bool = True):
    try:
        payload = {"email": email, "sendWelcomeEmail": send_welcome_email}
        response = requests.post(f"{API_BASE_URL}/identity/v1/users", json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Retrieve a single user based on user ID")
def get_user(user_id: str):
    try:
        response = requests.get(f"{API_BASE_URL}/identity/v1/users/{user_id}")
        if response.status_code == 404:
            return {"error": "User not found"}
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Update an existing user's preferences")
def update_user(user_id: str, language: str = "en", idle_timeout: int = 1800):
    try:
        payload = {"language": language, "idleTimeout": idle_timeout}
        response = requests.put(f"{API_BASE_URL}/identity/v1/users/{user_id}", json=payload)
        if response.status_code == 404:
            return {"error": "User not found"}
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}

@mcp.tool(description="Delete a user from a workspace")
def delete_user(user_id: str):
    try:
        response = requests.delete(f"{API_BASE_URL}/identity/v1/users/{user_id}")
        if response.status_code == 404:
            return {"error": "User not found"}
        response.raise_for_status()
        if response.status_code == 204:
            return {"message": "User successfully deleted"}
        return response.json()
    except Exception as e:
        return {"error": f"Failed to call API: {str(e)}"}


if __name__ == "__main__":
    mcp.run()