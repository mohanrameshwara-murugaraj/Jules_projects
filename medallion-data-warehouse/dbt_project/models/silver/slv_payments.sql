WITH stg_payments AS (
    SELECT * FROM {{ ref('stg_payments') }}
),

deduplicated AS (
    SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY payment_id ORDER BY _load_timestamp DESC) as row_num
    FROM stg_payments
    WHERE payment_id IS NOT NULL
)

SELECT
    payment_id,
    order_id,
    LOWER(REPLACE(TRIM(payment_method), ' ', '_')) AS payment_method,
    CAST(amount AS FLOAT) AS amount,
    LOWER(TRIM(status)) AS status,
    TRY_CAST(payment_date AS TIMESTAMP) AS payment_timestamp,
    _load_timestamp
FROM deduplicated
WHERE row_num = 1
