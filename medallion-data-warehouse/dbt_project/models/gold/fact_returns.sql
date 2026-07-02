WITH slv_returns AS (
    SELECT * FROM {{ ref('slv_returns') }}
),
slv_orders AS (
    SELECT * FROM {{ ref('slv_orders') }}
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['r.return_id']) }} AS return_sk,
    r.return_id,
    {{ dbt_utils.generate_surrogate_key(['o.order_id', 'o.product_id']) }} AS sales_sk,
    o.order_id,
    {{ dbt_utils.generate_surrogate_key(['o.customer_id']) }} AS customer_sk,
    {{ dbt_utils.generate_surrogate_key(['o.product_id']) }} AS product_sk,
    CAST(r.return_timestamp AS DATE) AS return_date_key,
    r.return_reason,
    r.refund_amount,
    CURRENT_TIMESTAMP() AS _inserted_at
FROM slv_returns r
LEFT JOIN slv_orders o ON r.order_id = o.order_id
