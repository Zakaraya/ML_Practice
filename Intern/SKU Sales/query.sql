SELECT cal_date days, SUM(cnt) sku FROM transactions_another_one
GROUP BY cal_date
ORDER BY days