import psycopg2

try:
    conn = psycopg2.connect(dbname='hpe_agentic_ai', user='postgres', password='Mithles', host='127.0.0.1', port=5432)
    cur = conn.cursor()
    cur.execute("SELECT serial_number, device_type FROM devices WHERE serial_number IN ('wireless-ctrl-020', 'ap-floor-022');")
    rows = cur.fetchall()
    print('Found in DB:', rows)
    conn.close()
except Exception as e:
    print('Error:', e)
