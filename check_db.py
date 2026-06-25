import psycopg2
conn = psycopg2.connect(dbname='hpe_agentic_ai', user='postgres', password='Mithles', host='localhost')
cur = conn.cursor()
cur.execute("SELECT source_device_id, management_source, device_type FROM devices WHERE serial_number='stg-array-10014'")
print(cur.fetchone())
