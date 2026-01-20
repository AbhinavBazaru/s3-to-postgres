import yaml
import os
from utils import get_secret

def load_config():
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    
    # Load secrets
    config['postgres_password'] = get_secret(config['postgres_password_secret_name'])
    
    return config