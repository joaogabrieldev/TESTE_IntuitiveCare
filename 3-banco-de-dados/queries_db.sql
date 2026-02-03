-- QUERY 1

WITH Despesas_Trimestres AS (
    SELECT
        d.REG_ANS,
        c.RAZAO_SOCIAL,
        CASE
            WHEN MONTH(d.DATA_EVENTO) BETWEEN 1 AND 3 THEN 1
            WHEN MONTH(d.DATA_EVENTO) BETWEEN 4 AND 6 THEN 2
            WHEN MONTH(d.DATA_EVENTO) BETWEEN 7 AND 9 THEN 3
            ELSE 4
        END AS Trimestre,
        SUM(d.VALOR_COMERCIAL) as Total_Tri
    FROM detalhe_despesas d
    JOIN operadores_cadastral c ON d.REG_ANS = c.REGISTRO_ANS
    GROUP BY d.REG_ANS, c.RAZAO_SOCIAL, Trimestre
),
Comparativo AS (
    SELECT
        RAZAO_SOCIAL,
        MAX(CASE WHEN Trimestre = 1 THEN Total_Tri ELSE 0 END) as Valor_Inicial,
        MAX(CASE WHEN Trimestre = 4 THEN Total_Tri ELSE 0 END) as Valor_Final

    FROM Despesas_Trimestres
    GROUP BY RAZAO_SOCIAL
)
SELECT
    RAZAO_SOCIAL,
    Valor_Inicial,
    Valor_Final,
    ROUND(((Valor_Final - Valor_Inicial) / Valor_Inicial) * 100, 2) AS Crescimento_Percentual
FROM Comparativo
WHERE Valor_Inicial > 0
ORDER BY Crescimento_Percentual DESC
LIMIT 5;


-- QUERY 2
SELECT
    c.UF, SUM(d.VALOR_COMERCIAL) as Total_Despesas_UF
    COUNT(DISTINCT d.REG_ANS) AS Qtd_Operadoras,
    ROUND(AVG(sub.Total_Por_Op), 2) AS Media_Por_Operadora
FROM detalhe_despesas d
JOIN operadores_cadastral c ON d.REG_ANS = c.REGISTRO_ANS
JOIN (
    SELECT REG_ANS, SUM(VALOR_COMERCIAL) as Total_Por_Op
    FROM detalhe_despesas
    GROUP BY REG_ANS
)