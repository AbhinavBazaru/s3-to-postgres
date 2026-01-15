import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # AWS Configuration
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_REGION = os.getenv('AWS_REGION')
    S3_BUCKET = os.getenv('S3_BUCKET')
    S3_KEY = os.getenv('S3_KEY')

    # Database Configuration
    DB_HOST = os.getenv('DB_HOST')
    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')

    # Data Validation Configuration
    SCHEMA = {
        'column1': 'int64',
        'column2': 'float64',
        'column3': 'object'
    }
    REQUIRED_COLUMNS = ['column1', 'column2', 'column3']

    # Data Quality Configuration
    MIN_ROWS = 10
    MAX_NULL_PERCENTAGE = 0.1

    # Retry Configuration
    MAX_RETRIES = 3
    RETRY_DELAY = 5  # seconds
