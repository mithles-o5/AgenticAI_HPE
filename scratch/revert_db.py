import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, r"c:\AgenticAI_HPE\resource_resolver")
from db import db_manager

conn = db_manager.get_connection()
cur = conn.cursor()

print("Reverting vendor changes...")
cur.execute("UPDATE endpoint_registry SET vendor = 'storage' WHERE vendor = 'mock_storage'")
cur.execute("UPDATE endpoint_registry SET vendor = 'network' WHERE vendor = 'mock_network'")
cur.execute("UPDATE endpoint_registry SET vendor = 'ilo' WHERE vendor = 'mock_server'")
cur.execute("UPDATE endpoint_registry SET vendor = 'cloud' WHERE vendor = 'mock_cloud'")

print("Dropping tables and columns...")
cur.execute("ALTER TABLE endpoint_registry DROP COLUMN IF EXISTS resource_type_id CASCADE")
cur.execute("DROP TABLE IF EXISTS cmdb_resource_mapping CASCADE")
cur.execute("DROP TABLE IF EXISTS resource_type CASCADE")

conn.commit()
print("DB Revert complete.")
