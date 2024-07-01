from datetime import datetime
from airflow import DAG
import os
from airflow.operators.python_operator import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
# from airflow.providers.amazon.aws.operators.s3 import S3ListOperator
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator

# Create the table in Snowflake



TABLE_NAME = "WEB_LOGS"
DATABASE_NAME = "WAREHOUSE"
SCHEMA_NAME = "PUBLIC"
FILE_FORMAT_NAME = "nytaxi_csv_format"
SNOWFLAKE_CONN_ID = "snowflake_dec_conn"
BUCKET_NAME = "landing"
MINIO_CONN_ID = "minio_conn_id_v2"
local_file_path = '/tmp/data/web_logs.json'

# Define the DAG
dag = DAG(
    's3_to_snowflake_dag',
    start_date=datetime(2022, 1, 1),
    tags=['dec','dec-loading', 'week_3_data_warehouse'],
    schedule_interval='@once'
)


create_table_query = f"""
CREATE TABLE IF NOT EXISTS {DATABASE_NAME}.{SCHEMA_NAME}.{TABLE_NAME} (
    event_id INT,
    event_name STRING,
    timestamp TIMESTAMP
)
"""

stage_table_name = f"{DATABASE_NAME}.{SCHEMA_NAME}.{TABLE_NAME}"


create_table_task = SnowflakeOperator(
    task_id='create_table_task',
    sql=create_table_query,
    snowflake_conn_id=SNOWFLAKE_CONN_ID,
    dag=dag
)

# Using data from data/web_logs_producer.py

create_stage_table = SnowflakeOperator(
    task_id='create_stage_table',
    sql=f"""
    CREATE OR REPLACE STAGE {DATABASE_NAME}.{SCHEMA_NAME}.{TABLE_NAME}
    FILE_FORMAT = {FILE_FORMAT_NAME}
    """,
    snowflake_conn_id=SNOWFLAKE_CONN_ID,
    dag=dag
)

def staging_data_local():
    s3_hook = S3Hook(aws_conn_id=MINIO_CONN_ID)
    file_key = 'web_logs.json'
    os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
    s3_hook.get_key(
            key=file_key,
            bucket_name=BUCKET_NAME
        ).download_file(local_file_path)


copy_data_to_table_task = SnowflakeOperator(
    task_id='copy_data_to_table',
    sql=f"""
    COPY INTO {DATABASE_NAME}.{SCHEMA_NAME}.{TABLE_NAME}
    FROM (SELECT $1:event_id::integer, $1:event_name::string, $1:timestamp::timestamp FROM @{stage_table_name})
    FILE_FORMAT = (
        TYPE=JSON,
        STRIP_OUTER_ARRAY=FALSE,
        REPLACE_INVALID_CHARACTERS=TRUE,
        DATE_FORMAT=AUTO,
        TIME_FORMAT=AUTO,
        TIMESTAMP_FORMAT=AUTO
    )
    ON_ERROR=ABORT_STATEMENT
    """,
    snowflake_conn_id=SNOWFLAKE_CONN_ID,
    dag=dag
)
    
staging_data_local_task = PythonOperator(
    task_id='staging_data_local_task',
    python_callable=staging_data_local,
    dag=dag
)

put_data_to_stage_task = SnowflakeOperator(
    task_id='put_data_to_stage',
    snowflake_conn_id=SNOWFLAKE_CONN_ID,
    sql=f"""
    PUT file://{local_file_path} @{stage_table_name}
    """,
    dag=dag
)

check_table_count = SnowflakeOperator(
    task_id='check_table_count',
    sql=f"""
    SELECT COUNT(*) FROM {DATABASE_NAME}.{SCHEMA_NAME}.{TABLE_NAME}
    """,
    snowflake_conn_id=SNOWFLAKE_CONN_ID,
    dag=dag
)

sensor = S3KeySensor(
    task_id='check_s3_for_file_in_s3',
    bucket_key='web_logs_data.json',
    bucket_name='landing',
    aws_conn_id=MINIO_CONN_ID,
    timeout=18 * 60 * 60,
    poke_interval=600,
    dag=dag)


# Set task dependencies
sensor >> create_table_task >> create_stage_table >> staging_data_local_task >>put_data_to_stage_task >> copy_data_to_table_task >> check_table_count

