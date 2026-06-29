import sys
sys.path.append("d:/HPE CPP/MCP_Integrated/resource_resolver")
from polling_engine import PollingEngine
from cache import ResourceCache

print("Running poll cycle...")
cache = ResourceCache()
pe = PollingEngine(cache)
results = pe.run_poll_cycle()
for r in results:
    print(f"{r['source_type']}: {r['status']}")

print("Checking UUID serials now...")
import psycopg2
import psycopg2.extras
conn = psycopg2.connect(dbname='hpe_agentic_ai', user='postgres', password='Mithles', host='localhost')
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM devices WHERE LENGTH(serial_number) = 36")
count = cur.fetchone()[0]
print(f"Total uuid serials left: {count}")
