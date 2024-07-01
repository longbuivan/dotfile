Coding Practices
================================================

## Introduction

This page contains the popular coding practices that I mostly used in daily basis as Data Engineer.

- [SQL](SampleCode.md#SQL)
- [Python](SampleCode.md#Python)
- [Docker and CLI](SampleCode.md#Docker&CLI)

## SQL

```sql

-- Create landingSales Table
CREATE TABLE landingSales (
    sales_id SERIAL PRIMARY KEY,
    product_name VARCHAR(255),
    quantity_sold INT,
    sales_date DATE,
    tracking_id INT
);

-- Insert sample records into landingSales
INSERT INTO landingSales (product_name, quantity_sold, sales_date, tracking_id)
VALUES
    ('Product A', 100, '2024-01-15',1),
    ('Product B', 150, '2024-01-16',2),
    ('Product C', 80, '2024-01-17',3),
    ('Product C', 100, '2024-01-20',3);

-- Create stagingSales Table
CREATE TABLE stagingSales (
    sales_id SERIAL PRIMARY KEY,
    product_name VARCHAR(255),
    quantity_sold INT,
    sales_date DATE,
    processed_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tracking_id INT
);

-- Create reportSales Table
CREATE TABLE reportSales (
    report_id SERIAL PRIMARY KEY,
    product_id INT,
    product_name VARCHAR(255),
    total_quantity_sold INT,
    report_date DATE,
    tracking_id INT

);

CREATE TABLE reportProducts (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(255)
);


-- Insert sample records into reportSales
INSERT INTO reportSales (product_id , product_name, total_quantity_sold, report_date, tracking_id)
VALUES
    (-2, 'Product A', 250, '2024-01-15',1),
    (2,'Product B', 300, '2024-01-16',2),
    (3, 'Product C', 180, '2024-01-17',3);

-- Insert sample records into stagingSales
INSERT INTO stagingSales (product_name, quantity_sold, sales_date, tracking_id)
VALUES
    ('Product X', 120, '2024-01-15',5),
    ('Product Y', 90, '2024-01-16',6),
    ('Product Z', 110, '2024-01-17',4),
    ('Product B', 150, '2024-01-16',2),
    ('Product C', 80, '2024-01-17',3);


INSERT INTO reportproducts (product_name)
VALUES ('Product A'), ('Product B');


-- Start Here:

SELECT * FROM landingsales;


WITH final_cte AS (
SELECT *, ROW_NUMBER() OVER(PARTITION BY product_name ORDER BY sales_date DESC)
FROM landingsales l
) SELECT * FROM final_cte
WHERE ROW_NUMBER = 1;


SELECT * FROM reportsales r ;
SELECT * FROM reportproducts r ;

-- Assume there is missing product_name
UPDATE reportsales  SET product_name  = NULL
WHERE report_id = 1


WITH base AS (
SELECT  * FROM
landingsales l
WHERE tracking_id IN (
    SELECT tracking_id
    FROM reportsales r
    WHERE product_id = '-2'
	)
),
missing_row AS (
SELECT base.tracking_id, r2.product_id  FROM base
JOIN reportproducts r2
ON base.product_name = r2.product_name
)

UPDATE reportsales rs
SET product_id =  mr.product_id
FROM missing_row mr
WHERE rs.tracking_id = mr.tracking_id

UPDATE reportsales rs
SET product_name  = rp.product_name
FROM reportproducts rp
WHERE rs.product_id  = rp.product_id


SELECT * FROM reportsales r ;

Tear down
DROP TABLE landingSales;
DROP TABLE reportProducts;
DROP TABLE reportSales;
DROP TABLE stagingSales;
```

## Python

### Hackerrank
* [countPairs.py](/codings/hackerrank/countPairs.py)
* [findNumberSequence.py](/codings/hackerrank/findNumberSequence.py)
* [pretiveMLModel.py](/codings/hackerrank/pretiveMLModel.py)
* [schoolCount.py](/codings/hackerrank/schoolCount.py)


### Facebook Ads

* [Insight](/codings/fbApis.py)
```python title="Getting Insight"
def get_facebook_ads_omni_purchases_data(access_token):
    url = "https://graph.facebook.com/v12.0/me/adaccounts"
    params = {
        "access_token": access_token,
        "fields": "name,insights{omni_purchase}"
    }

    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code == 200:
        # Retrieve all fields from insights
        insights_data = data['data']
        for account in insights_data:
            insights_url = f"https://graph.facebook.com/v12.0/{account['id']}/insights"
            insights_params = {
                "access_token": access_token
            }
            insights_response = requests.get(insights_url, params=insights_params)
            insights_data = insights_response.json()
            account['insights'] = insights_data['data']

        return data
    else:
        raise Exception(f"Failed to retrieve Facebook Ads data. Error: {data['error']['message']}")
```