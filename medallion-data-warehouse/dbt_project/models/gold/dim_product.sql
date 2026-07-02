WITH slv_products AS (
    SELECT * FROM {{ ref('slv_products') }}
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['product_id']) }} AS product_sk,
    product_id,
    product_name,
    category,
    brand,
    price,
    cost,
    (price - cost) AS expected_margin,
    currency_code,
    CURRENT_TIMESTAMP() AS _inserted_at
FROM slv_products
