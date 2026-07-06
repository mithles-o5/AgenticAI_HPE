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
            logger.info("Renaming vendor to management_source in endpoint_registry...")
            cur.execute("""
                DO $$
                BEGIN
                    IF EXISTS (
                        SELECT 1
                        FROM information_schema.columns
                        WHERE table_name='endpoint_registry' AND column_name='vendor'
                    ) THEN
                        ALTER TABLE endpoint_registry RENAME COLUMN vendor TO management_source;
                    END IF;
                END $$;
            """)
        conn.commit()
        logger.info("Column renamed successfully.")
    except Exception as e:
        conn.rollback()
        logger.exception("Migration failed:")
        raise
    finally:
        db_manager.return_connection(conn)

if __name__ == "__main__":
    migrate()
