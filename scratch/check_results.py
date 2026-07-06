import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, r"c:\AgenticAI_HPE\resource_resolver")
from db import db_manager
conn = db_manager.get_connection()
cur = conn.cursor()
cur.execute("SELECT device_type, action_key FROM endpoint_registry WHERE api_path = '/redoc' LIMIT 2")
print('redoc device_type:', cur.fetchall())
cur.execute("SELECT device_type, action_key FROM endpoint_registry WHERE api_path = '/rest/certificates/client/rabbitmq' LIMIT 2")
print('rabbitmq device_type:', cur.fetchall())
