import pandas as pd
import logging

logger = logging.getLogger(__name__)

def validate_schema(df, expected_schema):
    if set(df.columns) != set(expected_schema):
        logger.error(f"Schema mismatch. Expected: {expected_schema}, Got: {df.columns}")
        return False
    return True

def perform_data_quality_checks(df, rules):
    for rule in rules:
        column = rule['column']
        check_type = rule['check']
        if check_type == 'not_null':
            if df[column].isnull().any():
                logger.error(f"Data quality check failed: {column} contains null values")
                return False
        elif check_type == 'unique':
            if not df[column].is_unique:
                logger.error(f"Data quality check failed: {column} contains duplicate values")
                return False
    return True