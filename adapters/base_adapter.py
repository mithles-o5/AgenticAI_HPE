import abc
import json
import logging
import time
import urllib.request
import urllib.error
from typing import Dict, Any, Tuple

class BaseAdapter(abc.ABC):
    """
    Abstract Base Adapter for Server Management Platforms.
    Handles HTTP communication, task polling, and common formatting.
    """
    
    def __init__(self, poll_interval: float = 1.0, poll_timeout: float = 30.0):
        self.poll_interval = poll_interval
        self.poll_timeout = poll_timeout
        self.logger = logging.getLogger(f"server-agent.adapters.{self.__class__.__name__}")

    def build_url(self, source_host: str, api_endpoint: str) -> str:
        """Helper to safely build the API request URL."""
        host = source_host.rstrip('/')
        path = api_endpoint.lstrip('/')
        return f"{host}/{path}"

    def send_request(self, method: str, url: str, headers: Dict[str, str], body_data: Dict[str, Any] = None) -> Tuple[int, Dict[str, Any]]:
        """
        Executes HTTP requests using Python's standard urllib.
        Returns status code and response payload.
        """
        data_bytes = None
        # Copy headers to avoid modifying caller's state
        req_headers = dict(headers)
        
        if body_data is not None and method in ["POST", "PUT", "PATCH"]:
            data_bytes = json.dumps(body_data).encode("utf-8")
            req_headers["Content-Type"] = "application/json"
            
        req = urllib.request.Request(url, data=data_bytes, headers=req_headers, method=method)
        
        try:
            self.logger.debug(f"Sending {method} request to {url}")
            with urllib.request.urlopen(req, timeout=15) as response:
                status_code = response.status
                response_body = response.read().decode("utf-8")
                
                try:
                    resp_json = json.loads(response_body) if response_body else {}
                except json.JSONDecodeError:
                    resp_json = {"raw_text": response_body}
                return status_code, resp_json
                
        except urllib.error.HTTPError as e:
            status_code = e.code
            try:
                response_body = e.read().decode("utf-8")
                resp_json = json.loads(response_body) if response_body else {}
            except Exception:
                resp_json = {"error_message": str(e)}
            self.logger.warning(f"HTTP error {status_code} from {url}: {resp_json}")
            return status_code, resp_json
            
        except urllib.error.URLError as e:
            self.logger.error(f"URL error connecting to {url}: {e.reason}")
            return 503, {"error_message": f"Connection failed: {e.reason}"}
            
        except Exception as e:
            self.logger.error(f"Unexpected error executing request to {url}: {str(e)}")
            return 500, {"error_message": f"Internal request error: {str(e)}"}

    def check_task_completion(self, task_data: Dict[str, Any]) -> Tuple[bool, bool]:
        """
        Parses task response data to see if it is finished and if it was successful.
        Returns (is_finished, is_success).
        Supports both OneView and COM task structures by default.
        """
        # OneView format (taskState)
        task_state = task_data.get("taskState")
        if task_state is not None:
            task_state_str = str(task_state).strip().lower()
            if task_state_str in ["completed", "success", "succeeded"]:
                return True, True
            elif task_state_str in ["error", "failed", "terminated", "aborted"]:
                return True, False
            else:
                return False, False
        
        # COM format (state or status)
        state = task_data.get("state") or task_data.get("status")
        if state is not None:
            state_str = str(state).strip().lower()
            if state_str in ["completed", "success", "succeeded", "finished"]:
                return True, True
            elif state_str in ["failed", "error", "terminated", "aborted"]:
                return True, False
            else:
                return False, False

        # Fallback if no task state indicators exist, assume finished successfully
        return True, True

    def poll_task(self, source_host: str, task_uri: str, headers: Dict[str, str]) -> Tuple[int, Dict[str, Any]]:
        """Polls the task Uri until completion, failure, or timeout."""
        poll_url = self.build_url(source_host, task_uri)
        start_time = time.time()
        
        self.logger.info(f"Asynchronous task detected. Polling URL: {poll_url}")
        
        while True:
            elapsed = time.time() - start_time
            if elapsed > self.poll_timeout:
                self.logger.error(f"Task polling timed out after {self.poll_timeout} seconds")
                return 408, {"error_message": f"Task polling timed out after {self.poll_timeout} seconds"}
            
            status_code, task_data = self.send_request("GET", poll_url, headers)
            if status_code not in [200, 201, 202]:
                self.logger.error(f"Error while polling task: status code {status_code}")
                return status_code, task_data
            
            is_finished, is_success = self.check_task_completion(task_data)
            if is_finished:
                if is_success:
                    self.logger.info("Task completed successfully.")
                    return 200, task_data
                else:
                    self.logger.error(f"Task execution failed. Response: {task_data}")
                    return 500, task_data
            
            self.logger.debug(f"Task state not finished. Sleeping {self.poll_interval}s...")
            time.sleep(self.poll_interval)

    @abc.abstractmethod
    def get_headers(self, payload: Dict[str, Any]) -> Dict[str, str]:
        """Build and return credentials and metadata headers for the vendor."""
        pass

    def normalize_success(self, payload: Dict[str, Any], raw_response: Dict[str, Any]) -> Dict[str, Any]:
        """Normalizes raw success response into standard format."""
        action = payload.get("action", "unknown")
        management_source = payload.get("management_source", "UNKNOWN")
        serial_number = payload.get("serial_number", "unknown")
        
        # Build standard success message
        message = f"Server action '{action}' completed successfully."
        if isinstance(raw_response, dict):
            if "message" in raw_response:
                message = raw_response["message"]
            elif "status" in raw_response and isinstance(raw_response["status"], str):
                message = f"Server action '{action}' is in state: {raw_response['status']}"

        return {
            "success": True,
            "action": action,
            "management_source": management_source,
            "serial_number": serial_number,
            "status": "completed",
            "message": message,
            "raw_response": raw_response
        }

    def normalize_error(self, payload: Dict[str, Any], message: str, raw_response: Dict[str, Any] = None) -> Dict[str, Any]:
        """Normalizes raw error response into standard format."""
        action = payload.get("action", "unknown")
        error_details = raw_response or {}
        
        if isinstance(raw_response, dict):
            if "error_message" in raw_response:
                message = f"{message}: {raw_response['error_message']}"
            elif "message" in raw_response:
                message = f"{message}: {raw_response['message']}"

        return {
            "success": False,
            "action": action,
            "status": "failed",
            "message": message,
            "error": error_details
        }

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Core adapter execution loop.
        Constructs request, attaches auth headers, executes call,
        handles async task polling, and normalizes final response.
        """
        try:
            url = self.build_url(payload["source_host"], payload["api_endpoint"])
            headers = self.get_headers(payload)
            method = payload["http_method"]
            
            # Executing initial API Request
            status_code, response_data = self.send_request(method, url, headers, body_data=payload)
            
            # Handle standard error status codes
            if status_code not in [200, 201, 202, 204]:
                return self.normalize_error(
                    payload, 
                    f"API request failed with status code {status_code}", 
                    response_data
                )
            
            # Check for Async Task URI
            task_uri = response_data.get("taskUri") if isinstance(response_data, dict) else None
            if task_uri:
                status_code, response_data = self.poll_task(payload["source_host"], task_uri, headers)
                if status_code not in [200, 201, 202]:
                    return self.normalize_error(
                        payload, 
                        f"Asynchronous task execution failed (status {status_code})", 
                        response_data
                    )
            
            return self.normalize_success(payload, response_data)
            
        except Exception as e:
            self.logger.error(f"Uncaught exception during adapter execution: {str(e)}", exc_info=True)
            return self.normalize_error(
                payload,
                f"Adapter execution exception: {str(e)}",
                {"exception": str(e)}
            )
