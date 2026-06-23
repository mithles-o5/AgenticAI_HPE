import json
log_path = r"C:\Users\ELCOT\.gemini\antigravity-ide\brain\cc7eb1ff-36c0-4595-b099-7ba854524d62\.system_generated\logs\transcript.jsonl"
with open(log_path, "r", encoding="utf-8") as f:
    for idx, line in enumerate(f):
        if idx == 420:
            data = json.loads(line)
            print(json.dumps(data, indent=2))
            break
