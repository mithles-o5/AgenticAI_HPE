import psycopg2
import psycopg2.extras

conn = psycopg2.connect(dbname='hpe_agentic_ai', user='postgres', password='Mithles', host='localhost')
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
cur.execute("SELECT serial_number, management_source, device_type FROM devices WHERE serial_number LIKE '%rack-mgr%';")
print([dict(r) for r in cur.fetchall()])
conn.close()
