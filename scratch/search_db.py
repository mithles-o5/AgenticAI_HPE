import sys
import os

sys.path.append(os.path.abspath('c:\\Users\\ELCOT\\OneDrive\\Desktop\\integrated\\AgenticAI_HPE\\resource_resolver'))
from db import db_manager

query = "SELECT serial_number, fqdn, device_type FROM devices WHERE serial_number LIKE %s OR fqdn LIKE %s"
params = ('%10019%', '%10019%')
res = db_manager.execute_query(query, params)
print("SEARCH RESULTS:")
for r in res:
    print(r)
