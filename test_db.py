import sqlite3
import json

conn = sqlite3.connect(r'd:\HPE CPP\MCP_Integrated\mock_server(oneview)\oneview_db.sqlite')
conn.row_factory = sqlite3.Row
res = conn.execute("SELECT value FROM static_store WHERE key = 'get_rest_server_hardware_id'").fetchone()
if res:
    print(res['value'])
else:
    print('Not found')
