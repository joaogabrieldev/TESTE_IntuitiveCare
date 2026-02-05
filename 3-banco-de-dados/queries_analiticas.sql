--* Código MySQL

-- QUERY 1
WITH Despesas_Trimestrais AS (
    SELECT
        d.REG_ANS,
        c.RAZAO_SOCIAL
        CASE
            WHEN MONTH(d.DATA_EVENTO) BETWEEN 1 AND 3 THEN 1
            WHEN MONTH(d.DATA_EVENTO) BETWEEN 4 AND 6 THEN 2
            WHEN MONTH(d.DATA_EVENTO) BETWEEN 7 AND 9 THEN 3
            ELSE 4
        END AS Trimestre,
        SUM(d.VL_SALDO_FINAL) as Total_Tri

    FROM detalhe_despesas d
    JOIN operadoras_cadastral c on d.REG_ANS = c.REG_ANS
    GROUP BY d.REG_ANS, c.RAZAO_SOCIAL, Trimestre
),
Comparativo AS (
    SELECT
        RAZAO_SOCIAL,
        Valor_Inicial,
        Valor_Final,
        ROUND (((Valor_Final - Valor_Inicial) / Valor_Inicial) * 100, 2) AS Crescimento_Percentual
    FROM Comparativo
    WHERE Valor_Inicial > 0
    ORDER BY Crescimento_Percentual DESC
    LIMIT 5;
)

-- QUERY 2
SELECT
    c.UF,
    SUM(d.VL_SALDO_FINAL) AS Total_Despesas_UF,
    ROUND(AVG(sub.Total_Por_Op), 2) AS Media_Por_Operadora
FROM detalhe_despesas d
JOIN operadoras_cadastral c ON d.REG_ANS = c.REG_ANS
JOIN (
    SELECT REG_ANS, SUM(VL_SALDO_FINAL) as Total_Por_Op
    FROM detalhe_despesas
    GROUP BY REG_ANS
) sub ON d.REG_ANS = sub.REG_ANS
GROUP BY c.UF
ORDER BY Total_Despesas_UF DESC
LIMIT 5;

-- QUERY 3
WITH Despesas_Por_Operadora AS (
    SELECT
        d.REG_ANS,
        CASE
            WHEN MONTH(d.DATA_EVENTO) BETWEEN 1 AND 3 THEN 1
            WHEN MONTH(d.DATA_EVENTO) BETWEEN 4 AND 6 THEN 2
            WHEN MONTH(d.DATA_EVENTO) BETWEEN 7 AND 9 THEN 3
            ELSE 4
        END AS Trimestre,
        SUM(d.VL_SALDO_FINAL) as Total_Op
    FROM detalhe_despesas d
    GROUP BY d.REG_ANS, Trimestre
),
Media_Mercado_Por_Trimestre AS (
    SELECT
        Trimestre,
        AVG(Total_Op) as Media_Geral
    FROM Despesas_Por_Operadora
    GROUP BY Trimestre
)
SELECT
    COUNT(DISTINCT op.REG_ANS) as Qtd_Operadoras
FROM Despesas_Por_Operadora op
JOIN Media_Mercado_Por_Trimestre mercado ON op.Trimestre = mercado.Trimestre
WHERE op.Total_Op > mercado.Media_Geral
GROUP BY op.REG_ANS
HAVING COUNT(*) >= 2;