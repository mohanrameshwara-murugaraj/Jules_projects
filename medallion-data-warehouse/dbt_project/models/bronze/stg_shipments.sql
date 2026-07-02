WITH source AS (
    SELECT * FROM {{ source('medallion_db', 'raw_shipments') }}
)

SELECT
    shipment_id,
    order_id,
    carrier,
    tracking_number,
    shipment_date,
    estimated_delivery_date,
    actual_delivery_date,
    status,
    _load_timestamp,
    _source_file
FROM source
