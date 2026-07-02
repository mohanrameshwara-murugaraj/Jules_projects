WITH stg_shipments AS (
    SELECT * FROM {{ ref('stg_shipments') }}
),

deduplicated AS (
    SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY shipment_id ORDER BY _load_timestamp DESC) as row_num
    FROM stg_shipments
    WHERE shipment_id IS NOT NULL
)

SELECT
    shipment_id,
    order_id,
    UPPER(TRIM(carrier)) AS carrier,
    TRIM(tracking_number) AS tracking_number,
    TRY_CAST(shipment_date AS TIMESTAMP) AS shipment_timestamp,
    TRY_CAST(estimated_delivery_date AS TIMESTAMP) AS estimated_delivery_timestamp,
    TRY_CAST(actual_delivery_date AS TIMESTAMP) AS actual_delivery_timestamp,
    LOWER(TRIM(status)) AS status,
    _load_timestamp
FROM deduplicated
WHERE row_num = 1
