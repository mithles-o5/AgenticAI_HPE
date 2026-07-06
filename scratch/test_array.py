import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, r"c:\AgenticAI_HPE\resource_resolver")
from db import db_manager
conn = db_manager.get_connection()
cur = conn.cursor()
cur.execute("SELECT 'server' = ANY(string_to_array('server, storage, switch', ', '));")
print("Matches server:", cur.fetchone()[0])
cur.execute("SELECT 'rack_server' = ANY(string_to_array('server, storage, switch', ', '));")
print("Matches rack_server:", cur.fetchone()[0])
