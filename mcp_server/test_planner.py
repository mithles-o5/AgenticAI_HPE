import sys
sys.path.append('d:/HPE CPP/MCP_Integrated')
from task_planner.planner import TaskPlanner

query = "discover the topology of aruba-cx-017"
tasks = TaskPlanner.decompose_instruction(query)

for t in tasks:
    print(f"Action: {t.action}")
    print(f"Category: {t.category}")
    print(f"Identifier: {t.identifier}")
    print("---")
