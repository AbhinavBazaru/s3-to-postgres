import pandas as pd
import logging
from config import Config

logger = logging.getLogger(__name__)

class DataValidator:
    def __init__(self):
        self.config = Config()

    def validate_schema(self, df):
        try:
            # Check if all required columns are present
            missing_columns = set(self.config.REQUIRED_COLUMNS) - set(df.columns)
            if missing_columns:
                logger.error(f"Missing columns: {missing_columns}")
                return False

            # Check data types
            for column, dtype in self.config.SCHEMA.items():
                if df[column].dtype != dtype:
                    logger.error(f"Column {column} has incorrect data type. Expected {dtype}, got {df[column].dtype}")
                    return False

            return True
        except Exception as e:
            logger.error(f"Error in schema validation: {e}")
            return False

    def check_data_quality(self, df):
        try:
            # Check minimum number of rows
            if len(df) < self.config.MIN_ROWS:
                logger.error(f"DataFrame has fewer than {self.config.MIN_ROWS} rows")
                return False

            # Check for null values
            null_percentages = df.isnull().mean()
            if (null_percentages > self.config.MAX_NULL_PERCENTAGE).any():
                logger.error(f"Some columns have more than {self.config.MAX_NULL_PERCENTAGE*100}% null values")
                return False

            return True
        except Exception as e:
            logger.error(f"Error in data quality check: {e}")
            return False
