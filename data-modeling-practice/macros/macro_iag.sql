

{% macro macro_iag(area) -%}

    CASE {{ area }}
        WHEN 'ESPAÑA' THEN 'Spain'
        WHEN 'PAISES NO CEE' THEN 'Europe'
        WHEN 'EUROPA CEE' THEN 'Europe'      
        WHEN 'AFRICA NORTE' THEN 'Africa and Middle East'
        WHEN 'AFRICA SUR' THEN 'Africa and Middle East'
        WHEN 'AFRICA CENTRO' THEN 'Africa and Middle East'
        WHEN 'ORIENTE MEDIO' THEN 'Africa and Middle East'
        WHEN 'AMERICA NORTE' THEN 'North America'
        WHEN 'AMERICA CENTRO' THEN 'LACAR'
        WHEN 'AMERICA SUR' THEN 'LACAR'
        WHEN 'PACIFICO SUDOCCIDENTAL' THEN 'Asia and Pacific'
        WHEN 'EXTREMO ORIENTE' THEN 'Asia and Pacific'
        else null
    END
    
{%- endmacro %}
