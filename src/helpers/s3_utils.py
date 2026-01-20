import boto3
import pandas as pd
from io import StringIO
import logging

logger = logging.getLogger(__name__)

def read_csv_from_s3(bucket, file_name):
    s3 = boto3.client('s3')
    try:
        obj = s3.get_object(Bucket=bucket, Key=file_name)
        body = obj['Body'].read().decode('utf-8')
        return pd.read_csv(StringIO(body))
    except Exception as e:
        logger.error(f"Error reading file {file_name} from S3: {str(e)}")
        raise