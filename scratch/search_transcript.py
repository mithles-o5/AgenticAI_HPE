import json
import os

log_path = r"C:\Users\ELCOT\.gemini\antigravity-ide\brain\cc7eb1ff-36c0-4595-b099-7ba854524d62\.system_generated\logs\transcript.jsonl"

def search():
    if not os.path.exists(log_path):
        print(f"Log path does not exist: {log_path}")
        return
        
    print("=== Searching Conversation Transcript ===")
    with open(log_path, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f):
            if "previously" in line.lower() or "power" in line.lower() and "on" in line.lower() and "off" in line.lower():
                try:
                    data = json.loads(line)
                    # Print part of the content
                    content = data.get("content", "")
                    if content:
                        print(f"Line {idx}: {content[:300]}...")
                except Exception as e:
                    print(f"Line {idx} parse error: {e}")

if __name__ == "__main__":
    search()
