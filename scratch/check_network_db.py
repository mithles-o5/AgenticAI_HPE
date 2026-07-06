import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, r"c:\AgenticAI_HPE\resource_resolver")
from db import db_manager
conn = db_manager.get_connection()
cur = conn.cursor()
cur.execute("SELECT DISTINCT api_path, device_type FROM endpoint_registry WHERE management_source='network' AND api_path LIKE '%aps%' LIMIT 10;")
print("--- APS ---")
for row in cur.fetchall():
    print(f'{row[0]} -> {row[1]}')

cur.execute("SELECT DISTINCT api_path, device_type FROM endpoint_registry WHERE management_source='network' AND api_path LIKE '%devices%' LIMIT 10;")
print("--- DEVICES ---")
for row in cur.fetchall():
    print(f'{row[0]} -> {row[1]}')
