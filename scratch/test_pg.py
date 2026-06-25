import psycopg2

conn = psycopg2.connect(dbname="hpe_agentic_ai", user="postgres", password="Mithles", host="localhost")
with conn.cursor() as cur:
    cur.execute("SELECT serial_number FROM devices WHERE serial_number IN ('gl-ns-008', 'stg-array-10014', 'net-gateway-013', 'wan-r08-7', 'alletra-array-015', 'ms-dsk-219')")
    print("Found in Postgres CMDB:")
    for row in cur.fetchall():
        print(row[0])
