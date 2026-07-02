{% macro cents_to_dollars(column_name, scale=2) %}
    ROUND(CAST({{ column_name }} AS FLOAT) / 100, {{ scale }})
{% endmacro %}
