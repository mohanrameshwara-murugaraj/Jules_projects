WITH slv_marketing AS (
    SELECT * FROM {{ ref('slv_marketing') }}
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['campaign_id']) }} AS campaign_sk,
    campaign_id,
    campaign_name,
    channel,
    start_date,
    end_date,
    budget,
    CURRENT_TIMESTAMP() AS _inserted_at
FROM slv_marketing
