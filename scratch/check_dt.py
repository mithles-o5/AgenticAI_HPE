import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, r"c:\AgenticAI_HPE\resource_resolver")
from db import db_manager

conn = db_manager.get_connection()
cur = conn.cursor()
cur.execute("SELECT device_type, count(*) FROM endpoint_registry GROUP BY device_type ORDER BY count(*) DESC;")
for row in cur.fetchall():
    print(f'{row[0]}: {row[1]}')
