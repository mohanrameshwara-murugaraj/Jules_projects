WITH slv_shipments AS (
    SELECT DISTINCT
        carrier,
        status AS shipping_status
    FROM {{ ref('slv_shipments') }}
    WHERE carrier IS NOT NULL
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['carrier', 'shipping_status']) }} AS shipping_sk,
    carrier,
    shipping_status,
    CURRENT_TIMESTAMP() AS _inserted_at
FROM slv_shipments
