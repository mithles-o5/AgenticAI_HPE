import psycopg2

conn = psycopg2.connect(dbname='hpe_agentic_ai', user='postgres', password='Mithles', host='localhost')
cur = conn.cursor()
cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
tables = [r[0] for r in cur.fetchall()]

for t in tables:
    cur.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{t}'")
    cols = [r[0] for r in cur.fetchall()]
    print(f"Table {t}: {cols}")
    
conn.close()
