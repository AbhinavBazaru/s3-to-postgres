import pandas as pd
import logging

logger = logging.getLogger(__name__)

class DataTransformer:
    def transform(self, df):
        try:
            # Example transformations (modify as per your requirements)
            # 1. Convert column names to lowercase
            df.columns = df.columns.str.lower()

            # 2. Remove any leading/trailing whitespaces from string columns
            object_columns = df.select_dtypes(include=['object']).columns
            df[object_columns] = df[object_columns].apply(lambda x: x.str.strip())

            # 3. Convert date strings to datetime objects
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'], errors='coerce')

            # 4. Fill missing values (example: fill numeric columns with mean)
            numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns
            df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].mean())

            # 5. Create a new column (example: combining two columns)
            if 'first_name' in df.columns and 'last_name' in df.columns:
                df['full_name'] = df['first_name'] + ' ' + df['last_name']

            logger.info("Data transformation completed successfully")
            return df
        except Exception as e:
            logger.error(f"Error in data transformation: {e}")
            raise
