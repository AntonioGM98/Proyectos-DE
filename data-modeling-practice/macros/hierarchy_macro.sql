

{% macro hierarchy_macro(area) -%}

    CASE {{ area }}
        WHEN 'PACIFICO SUDOCCIDENTAL' THEN 1
        WHEN 'EXTREMO ORIENTE' THEN 2
        WHEN 'AMERICA SUR' THEN 3
        WHEN 'AMERICA CENTRO' THEN 4
        WHEN 'AMERICA NORTE' THEN 5
        WHEN 'AFRICA SUR' THEN 6
        WHEN 'AFRICA CENTRO' THEN 7
        WHEN 'ORIENTE MEDIO' THEN 8
        WHEN 'PAISES NO CEE' THEN 9
        WHEN 'AFRICA NORTE' THEN 10
        WHEN 'EUROPA CEE' THEN 11
        WHEN 'ESPAÑA' THEN 12
        else null
    END

{%- endmacro %}