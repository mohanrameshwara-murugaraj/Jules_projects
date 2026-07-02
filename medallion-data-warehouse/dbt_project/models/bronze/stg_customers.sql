WITH source AS (
    SELECT * FROM {{ source('medallion_db', 'raw_customers') }}
)

SELECT
    customer_id,
    first_name,
    last_name,
    email,
    phone,
    address,
    city,
    state,
    zip_code,
    country,
    registration_date,
    is_active,
    _load_timestamp,
    _source_file
FROM source
