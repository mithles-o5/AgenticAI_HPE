import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "resource_resolver"))
from query_agent import parse_query_hybrid

queries = [
    "List servers limit 5",
    "List servers skip 5 limit 5",
    "List servers page 2",
    "List switches limit 10",
]

for q in queries:
    res = parse_query_hybrid(q)
    print(f"Query: {q}")
    print(f"Parsed: {res}")
    print("-" * 20)
