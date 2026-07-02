import psycopg2
conn = psycopg2.connect(dbname='hpe_agentic_ai', user='postgres', password='Mithles', host='localhost', port=5432)
cur = conn.cursor()
cur.execute("SELECT serial_number, management_source, source_host FROM devices WHERE serial_number = 'apollo-node-899'")
print(cur.fetchall())
