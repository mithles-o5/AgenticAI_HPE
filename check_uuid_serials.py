import psycopg2
import psycopg2.extras
conn = psycopg2.connect(dbname='hpe_agentic_ai', user='postgres', password='Mithles', host='localhost')
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
cur.execute("SELECT serial_number, source_device_id, management_source, device_type FROM devices WHERE LENGTH(serial_number) = 36")
rows = cur.fetchall()
print(f"Total uuid serials: {len(rows)}")
for r in rows[:10]:
    print(dict(r))
