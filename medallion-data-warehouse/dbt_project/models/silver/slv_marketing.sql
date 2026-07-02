WITH stg_marketing AS (
    SELECT * FROM {{ ref('stg_marketing') }}
),

deduplicated AS (
    SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY campaign_id ORDER BY _load_timestamp DESC) as row_num
    FROM stg_marketing
    WHERE campaign_id IS NOT NULL
)

SELECT
    campaign_id,
    TRIM(campaign_name) AS campaign_name,
    LOWER(TRIM(channel)) AS channel,
    TRY_CAST(start_date AS DATE) AS start_date,
    TRY_CAST(end_date AS DATE) AS end_date,
    CAST(budget AS FLOAT) AS budget,
    _load_timestamp
FROM deduplicated
WHERE row_num = 1
