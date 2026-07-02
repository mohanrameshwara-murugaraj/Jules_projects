{{
    config(
        materialized='snapshot',
        unique_key='customer_id',
        strategy='timestamp',
        updated_at='_load_timestamp'
    )
}}

SELECT
    customer_id,
    first_name,
    last_name,
    email,
    phone_cleaned AS phone,
    address,
    city,
    state,
    zip_code,
    country,
    is_active,
    _load_timestamp
FROM {{ ref('slv_customers') }}
