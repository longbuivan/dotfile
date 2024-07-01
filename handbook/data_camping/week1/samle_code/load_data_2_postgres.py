#!/usr/bin/env python
# coding: utf-8

import os
import argparse

from time import time
import pandas as pd
from sqlalchemy import create_engine

def load_data_to_postgres(params):
    # Connect to PostgreSQL database
    local = params.local
    user = params.user
    password = params.password
    host = params.host 
    port = params.port 
    db = params.db
    table_name = params.table_name
    csv_name = params.csv_file

    if local == 'True':
        os.system(f"wget {csv_name} -O {csv_name}")


    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # Load data from Parquet file in chunks
    
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000, index_col=False)

    # Process each chunk
    for df in df_iter:

        t_start = time()
        # Convert columns to datetime
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

        # Load chunk into PostgreSQL database
        df.to_sql(name=table_name, con=engine, if_exists='append', index=False)  # Exclude the "index" column

        t_end = time()

        print('inserted another chunk, took %.3f second' % (t_end - t_start))

 
    engine.dispose()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--local', required=False, help='Check if running locally', default='False')
    parser.add_argument('--user', required=True, help='user name for postgres')
    parser.add_argument('--password', required=True, help='password for postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres')
    parser.add_argument('--db', required=True, help='database name for postgres')
    parser.add_argument('--table_name', required=True, help='name of the table where we will write the results to')
    parser.add_argument('--csv_file', required=True, help='csv_file of the csv file')

    args = parser.parse_args()

    load_data_to_postgres(args)
