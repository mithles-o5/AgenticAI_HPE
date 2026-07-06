import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, r"c:\AgenticAI_HPE\resource_resolver")
from db import db_manager

conn = db_manager.get_connection()
cur = conn.cursor()
cur.execute("UPDATE endpoint_registry SET vendor = 'mock_storage' WHERE vendor = 'storage'")
cur.execute("UPDATE endpoint_registry SET vendor = 'mock_network' WHERE vendor = 'network'")
cur.execute("UPDATE endpoint_registry SET vendor = 'mock_server' WHERE vendor = 'ilo'")
cur.execute("UPDATE endpoint_registry SET vendor = 'mock_cloud' WHERE vendor = 'cloud'")
conn.commit()
print("Vendor normalization complete")
