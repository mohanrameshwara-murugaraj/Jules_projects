WITH source AS (
    SELECT * FROM {{ source('medallion_db', 'raw_orders') }}
)

SELECT
    order_id,
    customer_id,
    product_id,
    order_date,
    quantity,
    status,
    _load_timestamp,
    _source_file
FROM source
