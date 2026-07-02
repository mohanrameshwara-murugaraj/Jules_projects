WITH slv_customers AS (
    SELECT DISTINCT
        city,
        state,
        zip_code,
        country
    FROM {{ ref('slv_customers') }}
    WHERE city IS NOT NULL AND state IS NOT NULL AND country IS NOT NULL
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['city', 'state', 'country', 'zip_code']) }} AS geography_sk,
    city,
    state,
    zip_code,
    country,
    CURRENT_TIMESTAMP() AS _inserted_at
FROM slv_customers
