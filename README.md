# Data Pipeline Project

This project implements a data pipeline that reads CSV files from an S3 bucket, validates the data schema, performs data quality checks, transforms the data using pandas, and loads it into a PostgreSQL database.

## Features

- CSV file reading from AWS S3
- Data schema validation
- Data quality checks
- Data transformation using pandas
- Data loading into PostgreSQL
- Error handling and logging
- Retry logic for resilience
- Configuration management

## Setup

1. Clone the repository:
   
   git clone https://github.com/your-username/data-pipeline-project.git
   cd data-pipeline-project
   

2. Create a virtual environment and activate it:
   
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   

3. Install the required packages:
   
   pip install -r requirements.txt
   

4. Create a `.env` file in the project root and add your configuration:
   
   AWS_ACCESS_KEY_ID=your_access_key
   AWS_SECRET_ACCESS_KEY=your_secret_key
   AWS_REGION=your_region
   S3_BUCKET=your_bucket_name
   S3_KEY=your_file_key
   DB_HOST=your_db_host
   DB_NAME=your_db_name
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   

## Usage

Run the main script to execute the data pipeline:


python main.py


## Project Structure

- `main.py`: The main script that orchestrates the data pipeline.
- `config.py`: Configuration management using environment variables.
- `data_validator.py`: Handles data schema validation and quality checks.
- `data_transformer.py`: Performs data transformations.
- `data_loader.py`: Manages data loading into the PostgreSQL database.
- `requirements.txt`: Lists all Python dependencies.
- `README.md`: Project documentation (this file).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
