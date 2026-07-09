import re

def parse_update(query):
    query_lower = query.lower()
    
    # Matches: set firmware version of switch-01 to 1.2.3
    # Matches: change status of gl-ns-008 to offline
    # Matches: modify power_state of node-1 to on
    m = re.search(r'\b(?:set|change|update|modify|configure)\s+(.+?)\s+(?:of\s+[^\s]+\s+)?to\s+(.+)\b', query_lower)
    if m:
        attribute = m.group(1).strip().replace(" ", "_")
        value = m.group(2).strip()
        return {"attribute": attribute, "value": value}
    return None

queries = [
    "set firmware version of switch-01 to 1.2.3",
    "change status of gl-ns-008 to offline",
    "modify firmware of apollo-node-029 to 2.1.0",
    "update health status to OK"
]

for q in queries:
    print(f"{q} -> {parse_update(q)}")
