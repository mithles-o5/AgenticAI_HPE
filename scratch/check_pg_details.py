import psycopg2
conn = psycopg2.connect(dbname='hpe_agentic_ai', user='postgres', password='Mithles', host='localhost')
cur = conn.cursor()
cur.execute("SELECT id, source_device_id, device_type FROM devices WHERE serial_number='alletra-array-015'")
print(cur.fetchone())
