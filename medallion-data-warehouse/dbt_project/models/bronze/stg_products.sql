WITH source AS (
    SELECT * FROM {{ source('medallion_db', 'raw_products') }}
)

SELECT
    product_id,
    product_name,
    category,
    brand,
    price,
    cost,
    currency,
    _load_timestamp,
    _source_file
FROM source
