import sys
import os
import logging
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, r"c:\AgenticAI_HPE\resource_resolver")
from db import db_manager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("migration")

def migrate():
    conn = db_manager.get_connection()
    try:
        with conn.cursor() as cur:
            # 1. Fetch exact column device_type from endpoint registry
            logger.info("Fetching unique device_type values from endpoint_registry...")
            cur.execute("SELECT DISTINCT device_type FROM endpoint_registry WHERE device_type IS NOT NULL")
            device_types = [row[0] for row in cur.fetchall()]
            logger.info(f"Fetched {len(device_types)} unique values.")

            # 2. Create a single table named resource_type table keep the col name as res_type with an id
            logger.info("Creating resource_type table...")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS resource_type (
                    id SERIAL PRIMARY KEY,
                    res_type VARCHAR(64) UNIQUE NOT NULL
                )
            """)

            # 3. Fetched values should be pasted there
            logger.info("Inserting fetched values into resource_type...")
            from psycopg2 import extras
            extras.execute_values(
                cur,
                "INSERT INTO resource_type (res_type) VALUES %s ON CONFLICT (res_type) DO NOTHING",
                [(dt,) for dt in device_types]
            )

            # 4. Create a foreign key in end point registry and map the pk of resource_type table
            logger.info("Adding resource_type_id foreign key to endpoint_registry...")
            cur.execute("""
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1
                        FROM information_schema.columns
                        WHERE table_name='endpoint_registry' AND column_name='resource_type_id'
                    ) THEN
                        ALTER TABLE endpoint_registry ADD COLUMN resource_type_id INT REFERENCES resource_type(id);
                    END IF;
                END $$;
            """)

            logger.info("Mapping resource_type_id...")
            cur.execute("""
                UPDATE endpoint_registry e
                SET resource_type_id = r.id
                FROM resource_type r
                WHERE e.device_type = r.res_type
            """)

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
