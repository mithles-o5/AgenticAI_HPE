import psycopg2

conn = psycopg2.connect(dbname='hpe_agentic_ai', user='postgres', password='Mithles', host='localhost')
cur = conn.cursor()
cur.execute("DELETE FROM devices WHERE serial_number='rack-mgr-alpha' AND management_source='mock_server';")
conn.commit()
print('Deleted.')
conn.close()
