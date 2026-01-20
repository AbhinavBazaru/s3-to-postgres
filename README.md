# S3 to PostgreSQL Batch ETL Pipeline

This pipeline reads CSV files from an AWS S3 bucket, performs data validation, transformation, and loads the processed data into a PostgreSQL database.

## Architecture

mermaid
graph LR
    A[AWS S3] --> B[Data Validation]
    B --> C[Data Transformation]
    C --> D[PostgreSQL]


## Data Flow

1. Read CSV files from the specified S3 bucket.
2. Validate the schema of each file against the expected schema.
3. Perform data quality checks based on predefined rules.
4. Apply transformations to the data (renaming columns, dropping unnecessary columns, formatting dates).
5. Load the transformed data into the specified PostgreSQL table.

## Prerequisites

- Python 3.7+
- AWS account with access to S3 and Secrets Manager
- PostgreSQL database

## Setup

1. Clone the repository:
   
   git clone https://github.com/your-repo/s3-to-postgres-etl.git
   cd s3-to-postgres-etl
   

2. Install the required packages:
   
   pip install -r requirements.txt
   

3. Set up AWS credentials:
   - For local development, set up AWS CLI with `aws configure`
   - For production, ensure the EC2 instance or ECS task has the appropriate IAM role

4. Create secrets in AWS Secrets Manager:
   - Create secrets for PostgreSQL connection details (host, database, user, password, port)
   - Note the secret names, you'll need them for the configuration

5. Update the `config.yaml` file:
   - Set the correct S3 bucket name
   - Update the list of input files
   - Adjust the expected schema, data quality rules, and transformations as needed
   - Set the correct PostgreSQL table name and connection ID
   - Update the secret names for PostgreSQL connection details

## Usage

Run the pipeline with:


python main.py


## IAM Permissions Required

- S3:
  - s3:GetObject
  - s3:ListBucket

- Secrets Manager:
  - secretsmanager:GetSecretValue

## Local Development

For local development and testing:

1. Set up a local PostgreSQL database
2. Create environment variables for secrets:
   
   export my_postgres_conn_host=localhost
   export my_postgres_conn_database=your_db_name
   export my_postgres_conn_user=your_username
   export my_postgres_conn_password=your_password
   export my_postgres_conn_port=5432
   

3. Update the `config.yaml` file to use local file paths instead of S3 bucket if needed

## Logging

Logs are written to stdout. You can redirect them to a file if needed:


python main.py > pipeline.log 2>&1


## Error Handling

- The pipeline implements retry logic with exponential backoff for transient errors
- Errors are logged for debugging purposes
- The pipeline stops processing a file if it fails schema validation or data quality checks

## Security Considerations

- All sensitive information (database credentials, API keys) are stored in AWS Secrets Manager
- IAM roles are used for AWS service authentication
- For local development, secrets can be stored as environment variables
- Ensure that the S3 bucket and Secrets Manager are properly secured with appropriate IAM policies

## Monitoring and Maintenance

- Set up CloudWatch alarms for S3 events and Lambda function metrics
- Regularly review and update data quality rules and transformations as data evolves
- Monitor PostgreSQL database performance and scale resources as needed

