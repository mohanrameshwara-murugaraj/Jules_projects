-- ==========================================
-- Snowflake Environment Setup
-- ==========================================

-- 1. Create Roles
USE ROLE ACCOUNTADMIN;
CREATE ROLE IF NOT EXISTS data_engineer;
CREATE ROLE IF NOT EXISTS data_analyst;
GRANT ROLE data_engineer TO ROLE sysadmin;

-- 2. Create Warehouses
CREATE OR REPLACE WAREHOUSE elt_wh
WITH WAREHOUSE_SIZE = 'XSMALL'
AUTO_SUSPEND = 60
AUTO_RESUME = TRUE
INITIALLY_SUSPENDED = TRUE;

CREATE OR REPLACE WAREHOUSE bi_wh
WITH WAREHOUSE_SIZE = 'XSMALL'
AUTO_SUSPEND = 60
AUTO_RESUME = TRUE
INITIALLY_SUSPENDED = TRUE;

GRANT USAGE ON WAREHOUSE elt_wh TO ROLE data_engineer;
GRANT USAGE ON WAREHOUSE bi_wh TO ROLE data_analyst;

-- 3. Create Databases
CREATE DATABASE IF NOT EXISTS medallion_db;

-- 4. Create Schemas for Medallion Architecture
USE DATABASE medallion_db;
CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;

GRANT OWNERSHIP ON SCHEMA bronze TO ROLE data_engineer COPY CURRENT GRANTS;
GRANT OWNERSHIP ON SCHEMA silver TO ROLE data_engineer COPY CURRENT GRANTS;
GRANT OWNERSHIP ON SCHEMA gold TO ROLE data_engineer COPY CURRENT GRANTS;

GRANT USAGE ON DATABASE medallion_db TO ROLE data_engineer;
GRANT USAGE ON DATABASE medallion_db TO ROLE data_analyst;

-- Analyst needs to read from gold
GRANT USAGE ON SCHEMA gold TO ROLE data_analyst;
GRANT SELECT ON ALL TABLES IN SCHEMA gold TO ROLE data_analyst;
GRANT SELECT ON ALL VIEWS IN SCHEMA gold TO ROLE data_analyst;
GRANT SELECT ON FUTURE TABLES IN SCHEMA gold TO ROLE data_analyst;
GRANT SELECT ON FUTURE VIEWS IN SCHEMA gold TO ROLE data_analyst;

-- 5. Create File Formats
USE SCHEMA bronze;

CREATE OR REPLACE FILE FORMAT csv_format
    TYPE = 'CSV'
    COMPRESSION = 'AUTO'
    FIELD_DELIMITER = ','
    RECORD_DELIMITER = '\n'
    SKIP_HEADER = 1
    FIELD_OPTIONALLY_ENCLOSED_BY = '\042'
    TRIM_SPACE = FALSE
    ERROR_ON_COLUMN_COUNT_MISMATCH = FALSE
    ESCAPE = 'NONE'
    ESCAPE_UNENCLOSED_FIELD = '\134'
    DATE_FORMAT = 'AUTO'
    TIMESTAMP_FORMAT = 'AUTO'
    NULL_IF = ('\\N', '');

-- 6. Create Internal Stage for Data Loading
CREATE OR REPLACE STAGE raw_data_stage
    FILE_FORMAT = csv_format;

-- 7. Define Bronze Tables (Raw Data - no transformation)
-- Bronze schema preserves all raw issues
CREATE OR REPLACE TABLE bronze.raw_customers (
    customer_id STRING,
    first_name STRING,
    last_name STRING,
    email STRING,
    phone STRING,
    address STRING,
    city STRING,
    state STRING,
    zip_code STRING,
    country STRING,
    registration_date STRING,
    is_active STRING,
    _load_timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    _source_file STRING
);

CREATE OR REPLACE TABLE bronze.raw_products (
    product_id STRING,
    product_name STRING,
    category STRING,
    brand STRING,
    price FLOAT,
    cost FLOAT,
    currency STRING,
    _load_timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    _source_file STRING
);

CREATE OR REPLACE TABLE bronze.raw_orders (
    order_id STRING,
    customer_id STRING,
    product_id STRING,
    order_date STRING,
    quantity INTEGER,
    status STRING,
    _load_timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    _source_file STRING
);

CREATE OR REPLACE TABLE bronze.raw_payments (
    payment_id STRING,
    order_id STRING,
    payment_method STRING,
    amount FLOAT,
    status STRING,
    payment_date STRING,
    _load_timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    _source_file STRING
);

CREATE OR REPLACE TABLE bronze.raw_inventory (
    inventory_id STRING,
    product_id STRING,
    warehouse_id STRING,
    quantity_on_hand INTEGER,
    last_updated STRING,
    _load_timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    _source_file STRING
);

CREATE OR REPLACE TABLE bronze.raw_shipments (
    shipment_id STRING,
    order_id STRING,
    carrier STRING,
    tracking_number STRING,
    shipment_date STRING,
    estimated_delivery_date STRING,
    actual_delivery_date STRING,
    status STRING,
    _load_timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    _source_file STRING
);

CREATE OR REPLACE TABLE bronze.raw_returns (
    return_id STRING,
    order_id STRING,
    return_date STRING,
    reason STRING,
    refund_amount FLOAT,
    _load_timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    _source_file STRING
);

CREATE OR REPLACE TABLE bronze.raw_marketing (
    campaign_id STRING,
    campaign_name STRING,
    channel STRING,
    start_date STRING,
    end_date STRING,
    budget FLOAT,
    _load_timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    _source_file STRING
);

-- Note: The COPY INTO statements will be executed by the python ingestion script.
