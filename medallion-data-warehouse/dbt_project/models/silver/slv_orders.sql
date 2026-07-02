WITH stg_orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
),

deduplicated AS (
    SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY _load_timestamp DESC) as row_num
    FROM stg_orders
    WHERE order_id IS NOT NULL
)

SELECT
    order_id,
    customer_id,
    product_id,
    TRY_CAST(order_date AS TIMESTAMP) AS order_timestamp,
    TRY_CAST(order_date AS DATE) AS order_date,
    ABS(CAST(quantity AS INTEGER)) AS quantity, -- Fix negative quantities
    LOWER(TRIM(status)) AS status,
    _load_timestamp
FROM deduplicated
WHERE row_num = 1
