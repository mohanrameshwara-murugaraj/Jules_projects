WITH slv_payments AS (
    SELECT * FROM {{ ref('slv_payments') }}
),
slv_orders AS (
    SELECT * FROM {{ ref('slv_orders') }}
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['p.payment_id']) }} AS payment_sk,
    p.payment_id,
    o.order_id,
    {{ dbt_utils.generate_surrogate_key(['o.customer_id']) }} AS customer_sk,
    CAST(p.payment_timestamp AS DATE) AS payment_date_key,
    p.payment_method,
    p.amount,
    p.status AS payment_status,
    CURRENT_TIMESTAMP() AS _inserted_at
FROM slv_payments p
LEFT JOIN slv_orders o ON p.order_id = o.order_id
