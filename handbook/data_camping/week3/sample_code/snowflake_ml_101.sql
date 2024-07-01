-- This is your Cortex Project.
-----------------------------------------------------------
-- SETUP
-----------------------------------------------------------
use role ACCOUNTADMIN;
use warehouse COMPUTE_WH;
use database WAREHOUSE;
use schema ANALYSIS;

-- Inspect the first 10 rows of your training data. This is the data we'll
-- use to create your model.
select * from THIRTY_DAY_AVG_COST limit 10;

-- Inspect the first 10 rows of your prediction data. This is the data the model
-- will use to generate predictions.
select * from HOTEL_COUNT_BY_DAY limit 10;

-----------------------------------------------------------
-- CREATE PREDICTIONS
-----------------------------------------------------------
-- Create your model.
CREATE OR REPLACE SNOWFLAKE.ML.CLASSIFICATION classifying_ml_model(
    INPUT_DATA => SYSTEM$REFERENCE('VIEW', 'THIRTY_DAY_AVG_COST'),
    TARGET_COLNAME => 'DIFF_BTW_ACTUAL_AVG',
    CONFIG_OBJECT => { 'ON_ERROR': 'SKIP' }
);

-- Inspect your logs to ensure training completed successfully. 
CALL classifying_ml_model!SHOW_TRAINING_LOGS();

-- Generate predictions as new columns in to your prediction table.
CREATE TABLE My_classification_2024_06_17 AS SELECT
    *, 
    classifying_ml_model!PREDICT(
        OBJECT_CONSTRUCT(*),
        -- This option alows the prediction process to complete even if individual rows must be skipped.
        {'ON_ERROR': 'SKIP'}
    ) as predictions
from HOTEL_COUNT_BY_DAY;

-- View your predictions.
SELECT * FROM My_classification_2024_06_17;

-- Parse the prediction results into separate columns. 
-- Note: This is a just an example. Be sure to update this to reflect 
-- the classes in your dataset.
SELECT * EXCLUDE predictions,
        predictions:class AS class,
        round(predictions['probability'][class], 3) as probability
FROM My_classification_2024_06_17;

-----------------------------------------------------------
-- INSPECT RESULTS
-----------------------------------------------------------

-- Inspect your model's evaluation metrics.
CALL classifying_ml_model!SHOW_EVALUATION_METRICS();
CALL classifying_ml_model!SHOW_GLOBAL_EVALUATION_METRICS();
CALL classifying_ml_model!SHOW_CONFUSION_MATRIX();

-- Inspect the relative importance of your features, including auto-generated features.  
CALL classifying_ml_model!SHOW_FEATURE_IMPORTANCE();

-- DROP SNOWFLAKE.ml.classification classifying_ml_model;
