import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, r"c:\AgenticAI_HPE\resource_resolver")
from db import db_manager

conn = db_manager.get_connection()
cur = conn.cursor()
cur.execute("SELECT DISTINCT management_source FROM endpoint_registry ORDER BY management_source;")
print("Endpoint Registry Sources:")
for row in cur.fetchall():
    print(f"  {row[0]}")
