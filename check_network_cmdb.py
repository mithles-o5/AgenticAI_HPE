import psycopg2
conn = psycopg2.connect(dbname='hpe_agentic_ai', user='postgres', password='Mithles', host='localhost')
cur = conn.cursor()
cur.execute("SELECT serial_number, device_type, management_source, source_device_id FROM devices WHERE management_source='mock_network' LIMIT 15")
rows = cur.fetchall()
print(f"Network devices in CMDB: {len(rows)}")
for r in rows:
    print(f"  sn={r[0]}, type={r[1]}, src={r[2]}, src_id={r[3]}")
conn.close()
