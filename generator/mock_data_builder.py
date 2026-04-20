import json
import os

def save_mock_data(mock_folder, function_name, response_body):
    os.makedirs(mock_folder, exist_ok=True)

    file_path = os.path.join(mock_folder, f"{function_name}.json")

    if isinstance(response_body, str):
        try:
            parsed = json.loads(response_body) if response_body else {
                "message": "Mock response generated"
            }
        except Exception:
            parsed = {
                "message": "Mock response generated",
                "raw_response": response_body
            }
    else:
        parsed = response_body if response_body else {
            "message": "Mock response generated"
        }

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(parsed, f, indent=4)

    return file_path
