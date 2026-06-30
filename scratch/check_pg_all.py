import psycopg2
conn = psycopg2.connect(dbname='hpe_agentic_ai', user='postgres', password='mithles', host='localhost')
cur = conn.cursor()
# Show columns
cur.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name='devices' ORDER BY ordinal_position")
print('Columns:')
for row in cur.fetchall():
    print(f'  {row[0]}: {row[1]}')
# Count
cur.execute('SELECT COUNT(*) FROM devices')
print('Total devices:', cur.fetchone()[0])
# Sample with uuid
cur.execute('SELECT uuid, serial_number, device_type FROM devices LIMIT 5')
print('Sample rows (uuid, serial, type):')
for row in cur.fetchall():
    print(f'  {row}')
conn.close()
