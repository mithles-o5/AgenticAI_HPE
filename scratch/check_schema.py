import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, r"c:\AgenticAI_HPE\resource_resolver")
from db import db_manager
conn = db_manager.get_connection()
cur = conn.cursor()
cur.execute("""
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'endpoint_registry';
""")
print("--- ENDPOINT_REGISTRY ---")
for r in cur.fetchall():
    print(r)

cur.execute("""
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'resource_type';
""")
print("--- RESOURCE_TYPE ---")
for r in cur.fetchall():
    print(r)
