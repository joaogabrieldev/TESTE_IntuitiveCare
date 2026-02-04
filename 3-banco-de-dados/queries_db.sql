-- 1. QUERY 1
SELECT
    RAZAO_SOCIAL,
    UF,
    TOTAL_DESPESAS
FROM despesas_agregadas
ORDER BY TOTAL_DESPESAS DESC
LIMIT 5;

-- QUERY 2
SELECT
    DESCRICAO,
    VL_SALDO_FINAL
FROM detalhe_despesas
ORDER BY VL_SALDO_FINAL DESC
LIMIT 5;

-- QUERY 3
WITH Despesas_Por_Operadora AS (
    SELECT
        REG_ANS,
        strftime('%m', DATA_EVENTO) as Mes,
        SUM(VL_SALDO_FINAL) as Total_Op
    FROM detalhe_despesas
    GROUP BY REG_ANS, Mes
),
Media_Mercado AS (
    SELECT
        Mes,
        AVG(Total_Op) as Media_Geral
    FROM Despesas_Por_Operadora
    GROUP BY Mes
)
SELECT
    op.REG_ANS,
    COUNT(*) as Meses_Acima_Media
FROM Despesas_Por_Operadora op
JOIN Media_Mercado m ON op.Mes = m.Mes
WHERE op.Total_Op > m.Media_Geral
GROUP BY op.REG_ANS
HAVING COUNT(*) >= 2
LIMIT 5;