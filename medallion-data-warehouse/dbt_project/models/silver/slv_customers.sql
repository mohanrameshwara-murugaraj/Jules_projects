WITH stg_customers AS (
    SELECT * FROM {{ ref('stg_customers') }}
),

deduplicated AS (
    SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY _load_timestamp DESC) as row_num
    FROM stg_customers
    WHERE customer_id IS NOT NULL
      AND customer_id NOT LIKE 'INVALID-%'
)

SELECT
    customer_id,
    TRIM(first_name) AS first_name,
    TRIM(last_name) AS last_name,
    LOWER(TRIM(email)) AS email,
    REGEXP_REPLACE(phone, '[^0-9]', '') AS phone_cleaned,
    address,
    UPPER(TRIM(city)) AS city,
    UPPER(TRIM(state)) AS state,
    zip_code,
    CASE WHEN UPPER(TRIM(country)) IN ('US', 'USA', 'UNITED STATES') THEN 'US' ELSE UPPER(TRIM(country)) END AS country,
    TRY_CAST(registration_date AS DATE) AS registration_date,
    CASE
        WHEN LOWER(TRIM(is_active)) IN ('true', 'yes', '1') THEN TRUE
        WHEN LOWER(TRIM(is_active)) IN ('false', 'no', '0') THEN FALSE
        ELSE NULL
    END AS is_active,
    _load_timestamp
FROM deduplicated
WHERE row_num = 1
