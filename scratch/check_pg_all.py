import psycopg2
conn = psycopg2.connect(dbname='hpe_agentic_ai', user='postgres', password='Mithles', host='localhost')
cur = conn.cursor()
cur.execute("SELECT serial_number, device_type FROM devices")
for row in cur.fetchall():
    print(row)
