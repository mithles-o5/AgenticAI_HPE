
import urllib.request
import urllib.error
import json

def check_tags():
    try:
        req = urllib.request.Request("http://localhost:11434/api/tags")
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))
            print("Successfully connected to Ollama!")
            print("Available models:")
            for m in data.get("models", []):
                print(" -", m.get("name"))
    except urllib.error.URLError as e:
        print("Connection failed:", e.reason)

def check_generate():
    try:
        payload = json.dumps({
            "model": "qwen2.5:1.5b",
            "prompt": "Hello",
            "stream": False
        }).encode("utf-8")
        req = urllib.request.Request("http://localhost:11434/api/generate", data=payload)
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            print("Successfully generated response!")
            print("Response:", data.get("response"))
    except urllib.error.URLError as e:
        print("Generation failed:", e.reason)

if __name__ == "__main__":
    check_tags()
    check_generate()

