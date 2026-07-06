import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, r"c:\AgenticAI_HPE\resource_resolver")
from db import db_manager

conn = db_manager.get_connection()
cur = conn.cursor()
cur.execute("SELECT * FROM endpoint_registry e LEFT JOIN resource_type r ON e.resource_type_id = r.id WHERE e.vendor = 'mock_storage' AND r.name = 'volumes'")
print('Endpoints for volumes:', cur.fetchall())
