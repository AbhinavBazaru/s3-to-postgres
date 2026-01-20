import psycopg2
from psycopg2.extras import execute_values
import logging
from utils import get_secret

logger = logging.getLogger(__name__)

def get_postgres_connection(conn_id):
    config = {
        'host': get_secret(f"{conn_id}_host"),
        'database': get_secret(f"{conn_id}_database"),
        'user': get_secret(f"{conn_id}_user"),
        'password': get_secret(f"{conn_id}_password"),
        'port': get_secret(f"{conn_id}_port")
    }
    return psycopg2.connect(**config)

def load_to_postgres(df, table_name, conn_id):
    conn = get_postgres_connection(conn_id)
    try:
        with conn.cursor() as cur:
            columns = df.columns.tolist()
            values = [tuple(row) for row in df.values]
            insert_query = f"INSERT INTO {table_name} ({','.join(columns)}) VALUES %s"
            execute_values(cur, insert_query, values)
        conn.commit()
        logger.info(f"Successfully loaded {len(df)} rows into {table_name}")
    except Exception as e:
        conn.rollback()
        logger.error(f"Error loading data into PostgreSQL: {str(e)}")
        raise
    finally:
        conn.close()