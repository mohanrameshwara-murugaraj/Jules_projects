WITH slv_customers AS (
    SELECT * FROM {{ ref('slv_customers') }}
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['customer_id']) }} AS customer_sk,
    customer_id,
    first_name,
    last_name,
    CONCAT(COALESCE(first_name, ''), ' ', COALESCE(last_name, '')) AS full_name,
    email,
    phone_cleaned AS phone,
    address,
    city,
    state,
    zip_code,
    country,
    registration_date,
    is_active,
    CURRENT_TIMESTAMP() AS _inserted_at
FROM slv_customers
