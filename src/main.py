import logging
import pandas as pd
import boto3
import psycopg2
from botocore.exceptions import ClientError
from config import Config
from data_validator import DataValidator
from data_transformer import DataTransformer
from data_loader import DataLoader

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

config = Config()

def get_s3_client():
    return boto3.client('s3',
                        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
                        region_name=config.AWS_REGION)

def get_db_connection():
    return psycopg2.connect(
        host=config.DB_HOST,
        database=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD
    )

def read_csv_from_s3(bucket, key):
    s3 = get_s3_client()
    try:
        obj = s3.get_object(Bucket=bucket, Key=key)
        return pd.read_csv(obj['Body'])
    except ClientError as e:
        logger.error(f"Error reading CSV from S3: {e}")
        raise

def process_data(df):
    validator = DataValidator()
    transformer = DataTransformer()
    loader = DataLoader(get_db_connection())

    try:
        # Validate data
        if not validator.validate_schema(df):
            logger.error("Data schema validation failed")
            return

        if not validator.check_data_quality(df):
            logger.error("Data quality check failed")
            return

        # Transform data
        transformed_df = transformer.transform(df)

        # Load data
        loader.load_data(transformed_df)

        logger.info("Data processing completed successfully")
    except Exception as e:
        logger.error(f"Error processing data: {e}")
    finally:
        loader.close_connection()

def main():
    try:
        df = read_csv_from_s3(config.S3_BUCKET, config.S3_KEY)
        process_data(df)
    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}")

if __name__ == "__main__":
    main()
