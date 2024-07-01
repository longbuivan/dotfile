from datetime import datetime
from airflow import DAG
# from airflow.operators.python import PythonOperator
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator

from ddl.nytaxi_yellow_tripdata import __create_yellow_trip

TABLE_NAME = "WEB_EVENTS"
DATABASE_NAME = "ANALYTICS"
SCHEMA_NAME = "PUBLIC"
FILE_FORMAT_NAME = "nytaxi_parquet_format"
SNOWFLAKE_CONN_ID = "snowflake_dec_conn"
FILE_PATH = "/opt/airflow/dags/data/yellow_tripdata_2024_01.parquet"

# SQL commands

SQL_INSERT_STATEMENT = f"INSERT INTO {TABLE_NAME} VALUES ('name', %(id)s)"
SQL_CREATE_TABLE = __create_yellow_trip(TABLE_NAME, SCHEMA_NAME, DATABASE_NAME)
SQL_LIST = [SQL_INSERT_STATEMENT % {"id": n} for n in range(10)]
SQL_MULTIPLE_STMTS = "; ".join(SQL_LIST)

# USE DATABASE {DATABASE_NAME}; USE SCHEMA {SCHEMA_NAME}; USE WAREHOUSE {WAREHOUSE_NAME};

# airflow task to create table on snowflake
def create_table_if_not_exists(snowflake_conn_id):
    with SnowflakeOperator(snowflake_conn_id=snowflake_conn_id, sql=SQL_CREATE_TABLE) as create_table:
        create_table.execute()
        

# Define the DAG
default_args = {
    'snowflake_conn_id': SNOWFLAKE_CONN_ID,
    'start_date': datetime(2022, 1, 1),
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'schedule_interval':'@once'
    }

dag = DAG(
    'filesystem_to_snowflake_dag',
    tags=['dec','dec-loading', 'week_3_data_warehouse'],
    default_args=default_args,
    description='DAG to load parquet file to snowflake',)

get_audit_date = SnowflakeOperator(
    task_id='get_audit_date',
    sql='SELECT CURRENT_DATE;',
    snowflake_conn_id=SNOWFLAKE_CONN_ID,
    dag=dag,
)

# Define the tasks
create_table = SnowflakeOperator(
    task_id='create_table',
    snowflake_conn_id=SNOWFLAKE_CONN_ID,
    sql=SQL_CREATE_TABLE,
    dag=dag
)

create_stage_table = SnowflakeOperator(
    task_id='create_stage_table',
    snowflake_conn_id=SNOWFLAKE_CONN_ID,
    sql=f"CREATE OR REPLACE STAGE {SCHEMA_NAME}.{TABLE_NAME};",
    dag=dag
)

put_data_to_stage = SnowflakeOperator(
    task_id='put_data_to_stage',
    snowflake_conn_id=SNOWFLAKE_CONN_ID,
    sql=f"PUT file://{FILE_PATH} @{SCHEMA_NAME}.{TABLE_NAME};",
    dag=dag
)

load_data = SnowflakeOperator (
    task_id = 'load_data',
    snowflake_conn_id = SNOWFLAKE_CONN_ID,
    sql = f"COPY INTO {SCHEMA_NAME}.{TABLE_NAME} FROM @{SCHEMA_NAME}.{TABLE_NAME} FILE_FORMAT=(FORMAT_NAME = {SCHEMA_NAME}.{FILE_FORMAT_NAME}) MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;",
    dag = dag
)


# Define the task dependencies
get_audit_date >> create_stage_table >> put_data_to_stage >> create_table >> load_data
