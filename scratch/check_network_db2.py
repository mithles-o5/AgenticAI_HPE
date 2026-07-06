import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, r"c:\AgenticAI_HPE\resource_resolver")
from db import db_manager
conn = db_manager.get_connection()
cur = conn.cursor()
cur.execute("SELECT device_type FROM endpoint_registry WHERE api_path = '/network/v1/devices/{id}';")
print("Total rows for devices/id:", cur.rowcount)
for r in cur.fetchall():
    print(r[0])
