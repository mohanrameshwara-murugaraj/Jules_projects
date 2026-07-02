WITH source AS (
    SELECT * FROM {{ source('medallion_db', 'raw_inventory') }}
)

SELECT
    inventory_id,
    product_id,
    warehouse_id,
    quantity_on_hand,
    last_updated,
    _load_timestamp,
    _source_file
FROM source
