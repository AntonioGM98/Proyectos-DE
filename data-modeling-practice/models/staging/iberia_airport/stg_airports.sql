{{
    config(materialized='table')
}}

SELECT * FROM {{ ref('airports_database') }}