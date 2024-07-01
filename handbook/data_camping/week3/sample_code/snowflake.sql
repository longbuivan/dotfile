
USE warehouse COMPUTE_WH;
USE DATABASE WAREHOUSE;
USE SCHEMA PUBLIC;


-- Creating file format for CSV

CREATE OR REPLACE FILE FORMAT  public.nytaxi_csv_format
  TYPE = CSV
  FIELD_OPTIONALLY_ENCLOSED_BY = '"'
  SKIP_HEADER = 1
  NULL_IF = ('');

-- Creating file format for Parquet
CREATE OR REPLACE FILE FORMAT  public.nytaxi_parquet_format
  TYPE = PARQUET
  COMPRESSION = SNAPPY;

-- Creating file format for JSON
CREATE OR REPLACE FILE FORMAT  public.nytaxi_json_format
  TYPE = JSON;
-- Creating internal stage table
CREATE OR REPLACE STAGE public.NYTAXI_INTERNAL_YELLOW_TRIPDATA;

-- Loading CSV data from local to the internal stage table
-- PUT file:///path/to/local/csv/file.csv @nytaxi_internal_stage;

put file:///landing/data/yellow_tripdata_2024_01.parquet @nytaxi_internal_yellow_tripdata;

/*
+---------------------------------+---------------------------------+-------------+-------------+--------------------+--------------------+----------+---------+
| SOURCE                          | target                          | source_size | target_size | source_compression | target_compression | status   | message |
|---------------------------------+---------------------------------+-------------+-------------+--------------------+--------------------+----------+---------|
| yellow_tripdata_2024_01.parquet | yellow_tripdata_2024_01.parquet |    49961641 |    49961648 | PARQUET            | PARQUET            | UPLOADED |         |
+---------------------------------+---------------------------------+-------------+-------------+--------------------+--------------------+----------+---------+
*/

put file:///landing/data/yellow_tripdata_2024_01_cleansed.parquet @nytaxi_internal_yellow_tripdata;

/*
+------------------------------------------+------------------------------------------+-------------+-------------+--------------------+--------------------+----------+---------+
| SOURCE                                   | target                                   | source_size | target_size | source_compression | target_compression | status   | message |
|------------------------------------------+------------------------------------------+-------------+-------------+--------------------+--------------------+----------+---------|
| yellow_tripdata_2024_01_cleansed.parquet | yellow_tripdata_2024_01_cleansed.parquet |    63300629 |    63300640 | PARQUET            | PARQUET            | UPLOADED |         |
+------------------------------------------+------------------------------------------+-------------+-------------+--------------------+--------------------+----------+---------+
*/

/*
 == TABLE PROFILE ==
 1   tpep_pickup_datetime   datetime64[ns]
 2   tpep_dropoff_datetime  datetime64[ns]
 3   passenger_count        float64
 4   trip_distance          float64
 5   RatecodeID             float64
 6   store_and_fwd_flag     OBJECT
 7   PULocationID           int32
 8   DOLocationID           int32
 9   payment_type           int64
 10  fare_amount            float64
 11  extra                  float64
 12  mta_tax                float64
 13  tip_amount             float64
 14  tolls_amount           float64
 15  improvement_surcharge  float64
 16  total_amount           float64
 17  congestion_surcharge   float64
 18  Airport_fee            float64
*/

put file:///Users/longbuivan/Documents/Projects/de-handbook/docs/datacamping/week_1_basics_and_infrastructure/data/yellow_tripdata_2024_01_cleansed.parquet @nytaxi_internal_yellow_tripdata;


CREATE OR REPLACE TABLE nytaxi_internal_yellow_tripdata
(
  "VendorID" INT,
  "tpep_pickup_datetime" TIMESTAMP_NTZ,
  "tpep_dropoff_datetime" TIMESTAMP_NTZ,
  "passenger_count" INT,
  "trip_distance" FLOAT,
  "RatecodeID" INT,
  "store_and_fwd_flag" STRING,
  "PULocationID" INT,
  "DOLocationID" INT,
  "payment_type" INT,
  "fare_amount" FLOAT,
  "extra" FLOAT,
  "mta_tax" FLOAT,
  "tip_amount" FLOAT,
  "tolls_amount" FLOAT,
  "improvement_surcharge" FLOAT,
  "total_amount" FLOAT,
  "congestion_surcharge" FLOAT,
  "Airport_fee" FLOAT
)


-- Wrong data type for time
COPY INTO "WAREHOUSE"."PUBLIC"."NYTAXI_INTERNAL_YELLOW_TRIPDATA"
FROM '@"WAREHOUSE"."PUBLIC"."NYTAXI_INTERNAL_YELLOW_TRIPDATA"'
FILES = ('yellow_tripdata_2024_01.parquet')
FILE_FORMAT = (FORMAT_NAME="WAREHOUSE"."PUBLIC"."NYTAXI_PARQUET_FORMAT")
MATCH_BY_COLUMN_NAME=CASE_INSENSITIVE
ON_ERROR=CONTINUE

COPY INTO "WAREHOUSE"."PUBLIC"."NYTAXI_INTERNAL_YELLOW_TRIPDATA"
FROM '@WAREHOUSE.PUBLIC.NYTAXI_INTERNAL_YELLOW_TRIPDATA'
FILES = ('yellow_tripdata_2024_01_cleansed.parquet')
FILE_FORMAT = (FORMAT_NAME = 'WAREHOUSE.PUBLIC.NYTAXI_PARQUET_FORMAT')
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
ON_ERROR = CONTINUE;


COPY INTO "WAREHOUSE"."PUBLIC"."NYTAXI_INTERNAL_YELLOW_TRIPDATA"
FROM '@WAREHOUSE.PUBLIC.NYTAXI_INTERNAL_YELLOW_TRIPDATA'
FILES = ('yellow_tripdata_2024_01_cleansed.csv.gz')
FILE_FORMAT = (FORMAT_NAME = 'WAREHOUSE.PUBLIC.nytaxi_csv_format')
ON_ERROR = CONTINUE;

-- Check yellow trip data
SELECT * FROM NYTAXI_INTERNAL_YELLOW_TRIPDATA LIMIT 10;



SELECT
  TOP 100 "VendorID",
  "DOLocationID",
  "PULocationID",
  "total_amount",
  AVG("total_amount") OVER (PARTITION BY "PULocationID", "DOLocationID") AS avg_amount_location
FROM
  NYTAXI_INTERNAL_YELLOW_TRIPDATA;

-- Create a non-partitioned table from internal table
CREATE OR REPLACE TABLE yellow_tripdata_non_partitioned AS
SELECT * FROM NYTAXI_INTERNAL_YELLOW_TRIPDATA;

-- Create a partitioned table from internal table
CREATE OR REPLACE TABLE yellow_tripdata_partitioned
(
  VendorID INT,
  tpep_pickup_datetime TIMESTAMP_NTZ,
  tpep_dropoff_datetime TIMESTAMP_NTZ,
  passenger_count INT,
  trip_distance FLOAT,
  RatecodeID INT,
  store_and_fwd_flag STRING,
  PULocationID INT,
  DOLocationID INT,
  payment_type INT,
  fare_amount FLOAT,
  extra FLOAT,
  mta_tax FLOAT,
  tip_amount FLOAT,
  tolls_amount FLOAT,
  improvement_surcharge FLOAT,
  total_amount FLOAT,
  congestion_surcharge FLOAT,
  Airport_fee FLOAT
)
CLUSTER BY (DATE_TRUNC('DAY', tpep_pickup_datetime))
AS
SELECT * FROM nytaxi_internal_yellow_tripdata;

-- Impact of partition
-- Scanning ~50MBs of data, 2964624 rows,36ms , 2nd time: no scanning data
SELECT DISTINCT("VendorID")
FROM yellow_tripdata_non_partitioned
WHERE DATE_TRUNC('DAY', "tpep_pickup_datetime") BETWEEN '2024-01-01' AND '2024-01-30';

-- Scanning ~50MBs(17%) of data, 2964629 rows, 265ms
SELECT DISTINCT(VENDORID)
FROM yellow_tripdata_partitioned
WHERE DATE_TRUNC('DAY', tpep_pickup_datetime) BETWEEN '2024-01-01' AND '2024-01-30';

-- Let's look into the partitions: cannot see the partitions on Snowflake


-- Clustering Depth: 1.75
CALL SYSTEM$CLUSTERING_DEPTH('WAREHOUSE.PUBLIC.YELLOW_TRIPDATA_PARTITIONED');
