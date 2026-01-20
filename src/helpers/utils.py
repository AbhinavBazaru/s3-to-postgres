import boto3
import time
import os
import logging
from functools import wraps

logger = logging.getLogger(__name__)

def get_secret(secret_name):
    # First, check if the secret is available as an environment variable
    env_secret = os.getenv(secret_name)
    if env_secret:
        logger.info(f"Loaded secret {secret_name} from environment variable")
        return env_secret

    # If not, retrieve from AWS Secrets Manager
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager')
    
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except Exception as e:
        logger.error(f"Error retrieving secret {secret_name}: {str(e)}")
        raise
    else:
        if 'SecretString' in get_secret_value_response:
            return get_secret_value_response['SecretString']
        else:
            return get_secret_value_response['SecretBinary']

def retry_with_backoff(max_retries, backoff_in_seconds):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries == max_retries:
                        logger.error(f"Max retries reached. Last error: {str(e)}")
                        raise
                    wait_time = backoff_in_seconds * (2 ** (retries - 1))
                    logger.warning(f"Retry {retries}/{max_retries} in {wait_time} seconds")
                    time.sleep(wait_time)
        return wrapper
    return decorator