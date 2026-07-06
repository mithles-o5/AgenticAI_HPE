import sys
import os
import logging
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, r"c:\AgenticAI_HPE\resource_resolver")
from db import db_manager
from seed_endpoint_registry import _infer_device_type

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("migration")

def migrate():
    conn = db_manager.get_connection()
    try:
        with conn.cursor() as cur:
            logger.info("Fetching endpoints to re-map device_type...")
            # We must select all unique endpoint properties except device_type
            # so we can explode them accurately without duplicating id-level things, 
            # but wait, the id is a UUID, we can just let PostgreSQL generate new UUIDs if we omit it.
            # However, our table is defined as: id UUID PRIMARY KEY DEFAULT gen_random_uuid().
            # Let's just fetch all DISTINCT endpoint combinations and re-insert them without ID, letting DB generate IDs.
            cur.execute("SELECT DISTINCT management_source, action_key, http_method, api_path FROM endpoint_registry")
            rows = cur.fetchall()
            
            new_rows = []
            seen = set()
            for mgmt_src, action_key, http_method, api_path in rows:
                new_dts = _infer_device_type(api_path, mgmt_src)
                dt_string = ", ".join(sorted(new_dts))
                key = (mgmt_src, dt_string, action_key, api_path, http_method)
                if key not in seen:
                    seen.add(key)
                    new_rows.append(key)
            
            logger.info(f"Deleting existing rows and re-inserting {len(new_rows)} rows to eliminate constraint violations...")
            cur.execute("TRUNCATE endpoint_registry")
            
            from psycopg2 import extras
            extras.execute_values(
                cur,
                """
                INSERT INTO endpoint_registry 
                    (management_source, device_type, action_key, api_path, http_method)
                VALUES %s
                ON CONFLICT (management_source, device_type, action_key, api_path, http_method) DO NOTHING
                """,
                new_rows,
                page_size=500
            )
        conn.commit()
        logger.info("Migration completed successfully.")
    except Exception as e:
        conn.rollback()
        logger.exception("Migration failed:")
        raise
    finally:
        db_manager.return_connection(conn)

if __name__ == "__main__":
    migrate()
