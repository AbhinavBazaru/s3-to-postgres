import pandas as pd
import psycopg2
import logging
from psycopg2 import sql
from config import Config

logger = logging.getLogger(__name__)

class DataLoader:
    def __init__(self, connection):
        self.connection = connection
        self.config = Config()

    def load_data(self, df):
        try:
            cursor = self.connection.cursor()
            table_name = 'your_table_name'  # Replace with your actual table name

            # Create table if not exists
            self._create_table_if_not_exists(cursor, table_name, df)

            # Insert data
            self._insert_data(cursor, table_name, df)

            self.connection.commit()
            logger.info(f"Successfully loaded {len(df)} rows into {table_name}")
        except Exception as e:
            self.connection.rollback()
            logger.error(f"Error loading data into database: {e}")
            raise
        finally:
            cursor.close()

    def _create_table_if_not_exists(self, cursor, table_name, df):
        columns = [f"{col} {self._get_postgres_type(df[col].dtype)}" for col in df.columns]
        create_table_query = sql.SQL("CREATE TABLE IF NOT EXISTS {} ({})").format(
            sql.Identifier(table_name),
            sql.SQL(', ').join(map(sql.SQL, columns))
        )
        cursor.execute(create_table_query)

    def _insert_data(self, cursor, table_name, df):
        columns = df.columns
        values = [tuple(row) for row in df.values]
        insert_query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
            sql.Identifier(table_name),
            sql.SQL(', ').join(map(sql.Identifier, columns)),
            sql.SQL(', ').join(sql.Placeholder() * len(columns))
        )
        cursor.executemany(insert_query, values)

    def _get_postgres_type(self, dtype):
        if dtype == 'int64':
            return 'INTEGER'
        elif dtype == 'float64':
            return 'FLOAT'
        elif dtype == 'bool':
            return 'BOOLEAN'
        elif dtype == 'datetime64[ns]':
            return 'TIMESTAMP'
        else:
            return 'TEXT'

    def close_connection(self):
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed")
