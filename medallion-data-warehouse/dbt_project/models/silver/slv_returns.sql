WITH stg_returns AS (
    SELECT * FROM {{ ref('stg_returns') }}
),

deduplicated AS (
    SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY return_id ORDER BY _load_timestamp DESC) as row_num
    FROM stg_returns
    WHERE return_id IS NOT NULL
)

SELECT
    return_id,
    order_id,
    TRY_CAST(return_date AS TIMESTAMP) AS return_timestamp,
    LOWER(TRIM(reason)) AS return_reason,
    CAST(refund_amount AS FLOAT) AS refund_amount,
    _load_timestamp
FROM deduplicated
WHERE row_num = 1
