import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, r"c:\AgenticAI_HPE\resource_resolver")
from db import db_manager

conn = db_manager.get_connection()
cur = conn.cursor()
cur.execute("SELECT DISTINCT device_type FROM endpoint_registry WHERE management_source = 'ilo' ORDER BY device_type;")
for row in cur.fetchall():
    print(row[0])
