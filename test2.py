import os
import sys

# Ensure parent directory in python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from resource_resolver.query_agent import QueryAgent

query = '{"identifier": "gl-ns-008", "action": "STATUS", "category": "Operational"}'
print(QueryAgent.parse_query(query))
