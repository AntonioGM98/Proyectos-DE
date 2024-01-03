

{% macro continent_macro(area) -%}

    CASE {{ area }}
        WHEN 'ESPAÑA' THEN 'DO'       
        WHEN 'PAISES NO CEE' THEN 'MH'
        WHEN 'EUROPA CEE' THEN 'MH'
        WHEN 'AFRICA NORTE' THEN 'MH'
        WHEN 'ORIENTE MEDIO' THEN 'MH'
        WHEN 'AFRICA CENTRO' THEN 'LH'
        WHEN 'AFRICA SUR' THEN 'LH'
        WHEN 'PACIFICO SUDOCCIDENTAL' THEN 'LH'
        WHEN 'EXTREMO ORIENTE' THEN 'LH'
        WHEN 'AMERICA CENTRO' THEN 'LH'
        WHEN 'AMERICA SUR' THEN 'LH'
        WHEN 'AMERICA NORTE' THEN 'LH'
        else null
    END

{%- endmacro %}