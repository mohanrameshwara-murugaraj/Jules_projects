{{ config(materialized='table') }}

WITH date_spine AS (
    {{ dbt_utils.date_spine(
        datepart="day",
        start_date="cast('2018-01-01' as date)",
        end_date="cast('2030-01-01' as date)"
    ) }}
)

SELECT
    CAST(date_day AS DATE) AS date_day,
    EXTRACT(YEAR FROM date_day) AS year,
    EXTRACT(MONTH FROM date_day) AS month,
    EXTRACT(DAY FROM date_day) AS day,
    EXTRACT(QUARTER FROM date_day) AS quarter,
    EXTRACT(DAYOFWEEK FROM date_day) AS day_of_week,
    CASE WHEN EXTRACT(DAYOFWEEK FROM date_day) IN (0, 6) THEN TRUE ELSE FALSE END AS is_weekend
FROM date_spine
