import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, r"c:\AgenticAI_HPE\resource_resolver")
from db import db_manager
conn = db_manager.get_connection()
cur = conn.cursor()
cur.execute("""
SELECT constraint_name, constraint_type
FROM information_schema.table_constraints
WHERE table_name = 'resource_type';
""")
for r in cur.fetchall():
    print(r)
