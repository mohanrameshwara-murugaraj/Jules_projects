WITH slv_orders AS (
    SELECT * FROM {{ ref('slv_orders') }}
),
slv_products AS (
    SELECT * FROM {{ ref('slv_products') }}
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['o.order_id', 'o.product_id']) }} AS sales_sk,
    o.order_id,
    {{ dbt_utils.generate_surrogate_key(['o.customer_id']) }} AS customer_sk,
    {{ dbt_utils.generate_surrogate_key(['o.product_id']) }} AS product_sk,
    o.order_date AS order_date_key, -- joins to dim_date
    o.quantity,
    p.price,
    p.cost,
    (o.quantity * p.price) AS total_revenue,
    (o.quantity * p.cost) AS total_cost,
    ((o.quantity * p.price) - (o.quantity * p.cost)) AS total_profit,
    o.status AS order_status,
    CURRENT_TIMESTAMP() AS _inserted_at
FROM slv_orders o
LEFT JOIN slv_products p ON o.product_id = p.product_id
