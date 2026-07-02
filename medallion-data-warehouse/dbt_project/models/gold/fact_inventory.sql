WITH slv_inventory AS (
    SELECT * FROM {{ ref('slv_inventory') }}
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['inventory_id']) }} AS inventory_sk,
    inventory_id,
    {{ dbt_utils.generate_surrogate_key(['product_id']) }} AS product_sk,
    warehouse_id,
    quantity_on_hand,
    CAST(last_updated_timestamp AS DATE) AS snapshot_date_key,
    CURRENT_TIMESTAMP() AS _inserted_at
FROM slv_inventory
