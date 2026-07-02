WITH source AS (
    SELECT * FROM {{ source('medallion_db', 'raw_returns') }}
)

SELECT
    return_id,
    order_id,
    return_date,
    reason,
    refund_amount,
    _load_timestamp,
    _source_file
FROM source
