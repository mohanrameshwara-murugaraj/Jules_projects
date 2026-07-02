WITH stg_products AS (
    SELECT * FROM {{ ref('stg_products') }}
),

deduplicated AS (
    SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY product_id ORDER BY _load_timestamp DESC) as row_num
    FROM stg_products
    WHERE product_id IS NOT NULL
      AND product_id NOT LIKE 'BAD-PROD-%'
)

SELECT
    product_id,
    TRIM(product_name) AS product_name,
    COALESCE(TRIM(category), 'Unknown') AS category,
    TRIM(brand) AS brand,
    ABS(CAST(price AS FLOAT)) AS price, -- Fix negative prices
    ABS(CAST(cost AS FLOAT)) AS cost,
    UPPER(TRIM(currency)) AS currency_code,
    _load_timestamp
FROM deduplicated
WHERE row_num = 1
