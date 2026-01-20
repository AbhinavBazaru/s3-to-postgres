import logging
from config import load_config
from s3_utils import read_csv_from_s3
from data_validator import validate_schema, perform_data_quality_checks
from data_transformer import transform_data
from database import load_to_postgres
from utils import retry_with_backoff

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@retry_with_backoff(max_retries=3, backoff_in_seconds=5)
def process_file(file_name, config):
    try:
        logger.info(f"Processing file: {file_name}")
        
        # Read CSV from S3
        df = read_csv_from_s3(config['s3_bucket'], file_name)
        
        # Validate schema
        if not validate_schema(df, config['expected_schema']):
            logger.error(f"Schema validation failed for file: {file_name}")
            return
        
        # Perform data quality checks
        if not perform_data_quality_checks(df, config['data_quality_rules']):
            logger.error(f"Data quality checks failed for file: {file_name}")
            return
        
        # Transform data
        transformed_df = transform_data(df, config['transformations'])
        
        # Load to PostgreSQL
        load_to_postgres(transformed_df, config['postgres_table'], config['postgres_conn_id'])
        
        logger.info(f"Successfully processed file: {file_name}")
    except Exception as e:
        logger.error(f"Error processing file {file_name}: {str(e)}")
        raise

def main():
    config = load_config()
    
    for file_name in config['input_files']:
        process_file(file_name, config)

if __name__ == "__main__":
    main()