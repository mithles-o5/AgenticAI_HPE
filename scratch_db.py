import psycopg2

conn = psycopg2.connect(dbname='hpe_agentic_ai', user='postgres', password='mithles', host='127.0.0.1', port='5432')
try:
    cur = conn.cursor()
    cur.execute("SELECT serial_number, device_type, management_source, source_device_id FROM devices WHERE serial_number LIKE '%apollo-node-999%'")
    rows = cur.fetchall()
    print('FOUND DEVICES:')
    for r in rows:
        print(r)
        
    print('\nDeleting orphaned entries...')
    cur.execute("DELETE FROM devices WHERE serial_number LIKE '%apollo-node-999%'")
    conn.commit()
    print('Deleted.')
except Exception as e:
    print(f"Error querying DB: {e}")
finally:
    conn.close()
