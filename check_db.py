import sqlite3
conn = sqlite3.connect(r'd:\HPE CPP\MCP_Integrated\mock_server(iLO)\ilo_db.sqlite')
cursor = conn.execute('SELECT PowerState, power_state FROM dynamic_redfish_v1_systems WHERE id = "8adce341-9e4a-4932-a943-dc33e5479222"')
print(cursor.fetchone())
conn.close()
