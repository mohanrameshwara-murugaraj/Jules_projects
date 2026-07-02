WITH source AS (
    SELECT * FROM {{ source('medallion_db', 'raw_payments') }}
)

SELECT
    payment_id,
    order_id,
    payment_method,
    amount,
    status,
    payment_date,
    _load_timestamp,
    _source_file
FROM source
