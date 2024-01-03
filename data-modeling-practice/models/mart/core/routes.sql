{{
    config(materialized='table')
}}

with 

airports as (
    SELECT * FROM {{ ref ('stg_airports') }}
),

result as (
    SELECT 
        distinct origin.STN_CODE || '' || destination.STN_CODE as Route,

        -- Distancia en KMs
        CASE
            WHEN SIN(RADIANS(origin.LATITUDE)) * SIN(RADIANS(destination.LATITUDE)) + COS(RADIANS(origin.LATITUDE)) * COS(RADIANS(destination.LATITUDE)) * COS(RADIANS(destination.LONGITUDE) - RADIANS(origin.LONGITUDE)) > 1 THEN 0 -- Valor fuera del rango, se establece a 0 o el valor que desees
            ELSE CAST(ACOS(SIN(RADIANS(origin.LATITUDE)) * SIN(RADIANS(destination.LATITUDE)) + COS(RADIANS(origin.LATITUDE)) * COS(RADIANS(destination.LATITUDE)) * COS(RADIANS(destination.LONGITUDE) - RADIANS(origin.LONGITUDE))) * 6371 as int)
        END AS DISTANCE,        -- Market_Segment_Code
        CASE
            WHEN {{ hierarchy_macro('origin.AREA_NAME') }} <= {{ hierarchy_macro('destination.AREA_NAME') }} THEN {{ continent_macro('origin.AREA_NAME') }}
            ELSE {{ continent_macro('destination.AREA_NAME') }}
        END AS MARKET_SEGMENT_CODE,

        -- Region_IAG
        CASE
            WHEN {{ hierarchy_macro('origin.AREA_NAME') }} <= {{ hierarchy_macro('destination.AREA_NAME') }} THEN {{ macro_iag('origin.AREA_NAME') }}
            ELSE {{ macro_iag('destination.AREA_NAME') }}
        END AS REGION_IAG,

        -- GR_AREA_NAME, AREA_NAME, SUBAREA_NAME, GR_AREA_CODE, AREA_CODE, SUBAREA_CODE
        -- GR_AREA_NAME
        CASE 
            WHEN {{ hierarchy_macro('origin.AREA_NAME') }} <= {{ hierarchy_macro('destination.AREA_NAME') }} THEN origin.GR_AREA_NAME
            ELSE destination.GR_AREA_NAME
        END AS GR_AREA_NAME,

        -- AREA_NAME
        CASE
            WHEN {{ hierarchy_macro('origin.AREA_NAME') }} <= {{ hierarchy_macro('destination.AREA_NAME') }} THEN origin.AREA_NAME
            ELSE destination.AREA_NAME
        END AS AREA_NAME,

        -- SUBAREA_NAME
        CASE
            WHEN {{ hierarchy_macro('origin.AREA_NAME') }} <= {{ hierarchy_macro('destination.AREA_NAME') }} THEN origin.SUBAREA_NAME
            ELSE destination.SUBAREA_NAME
        END AS SUBAREA_NAME,

        -- GR_AREA_CODE
        CASE
            WHEN {{ hierarchy_macro('origin.AREA_NAME') }} <= {{ hierarchy_macro('destination.AREA_NAME') }} THEN origin.GR_AREA_CODE
            ELSE destination.GR_AREA_CODE
        END AS GR_AREA_CODE,

        -- AREA_CODE
        CASE
            WHEN {{ hierarchy_macro('origin.AREA_NAME') }} <= {{ hierarchy_macro('destination.AREA_NAME') }} THEN origin.AREA_CODE
            ELSE destination.AREA_CODE
        END AS AREA_CODE,

        -- SUBAREA_CODE
        CASE
            WHEN {{ hierarchy_macro('origin.AREA_NAME') }} <= {{ hierarchy_macro('destination.AREA_NAME') }} THEN origin.SUBAREA_CODE
            ELSE destination.SUBAREA_CODE
        END AS SUBAREA_CODE,

        -- Cogemos la información para el origen o destino
        origin.STN_CODE AS STN_CODE_O,
        origin.CTRY_CODE  AS CTRY_CODE_O,
        origin.CTRY_NAME AS CTRY_NAME_O,
        origin.CITY_CODE AS CITY_NAME_O,
        {{ macro_iag('origin.AREA_NAME') }} AS REGION_IAG_O,
        origin.GR_AREA_CODE AS GR_AREA_CODE_O,
        origin.GR_AREA_NAME AS GR_AREA_NAME_O,
        origin.SUBAREA_CODE AS SUBAREA_CODE_O,
        origin.SUBAREA_NAME AS SUBAREA_NAME_O,
        origin.CONTINENT_CODE AS CONTINENT_CODE_O,
        origin.CONTINENT_NAME AS CONTINENT_NAME_O,
        origin.LATITUDE AS LATITUDE_O,
        origin.LONGITUDE AS LONGITUDE_O,

        destination.STN_CODE AS STN_CODE_D,
        destination.CTRY_CODE  AS CTRY_CODE_D,
        destination.CTRY_NAME AS CTRY_NAME_D,
        destination.CITY_CODE AS CITY_NAME_D,
        {{ macro_iag('destination.AREA_NAME') }} AS REGION_IAG_D,
        destination.GR_AREA_CODE AS GR_AREA_CODE_D,
        destination.GR_AREA_NAME AS GR_AREA_NAME_D,
        destination.SUBAREA_CODE AS SUBAREA_CODE_D,
        destination.SUBAREA_NAME AS SUBAREA_NAME_D,
        destination.CONTINENT_CODE AS CONTINENT_CODE_D,
        destination.CONTINENT_NAME AS CONTINENT_NAME_D,
        destination.LATITUDE AS LATITUDE_D,
        destination.LONGITUDE AS LONGITUDE_D

    FROM airports origin
        CROSS JOIN airports destination
)

SELECT * FROM result