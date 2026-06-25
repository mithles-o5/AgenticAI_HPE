import psycopg2
conn = psycopg2.connect(dbname='hpe_agentic_ai', user='postgres', password='Mithles', host='localhost')
cur = conn.cursor()
cur.execute("SELECT * FROM endpoint_registry WHERE vendor='mock_storage' AND action_key='STATUS'")
for row in cur.fetchall():
    print(row)
