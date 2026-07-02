WITH stg_inventory AS (
    SELECT * FROM {{ ref('stg_inventory') }}
),

deduplicated AS (
    SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY inventory_id ORDER BY _load_timestamp DESC) as row_num
    FROM stg_inventory
    WHERE inventory_id IS NOT NULL
)

SELECT
    inventory_id,
    product_id,
    UPPER(TRIM(warehouse_id)) AS warehouse_id,
    -- If quantity is negative, assume 0 for data cleaning purposes, or keep for audit? Let's fix.
    GREATEST(CAST(quantity_on_hand AS INTEGER), 0) AS quantity_on_hand,
    TRY_CAST(last_updated AS TIMESTAMP) AS last_updated_timestamp,
    _load_timestamp
FROM deduplicated
WHERE row_num = 1
