WITH source AS (
    SELECT * FROM {{ source('medallion_db', 'raw_marketing') }}
)

SELECT
    campaign_id,
    campaign_name,
    channel,
    start_date,
    end_date,
    budget,
    _load_timestamp,
    _source_file
FROM source
