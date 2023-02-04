WITH total_payment AS (
    SELECT date_trunc('month', date)::DATE AS time,
        COUNT(*) total, mode
    FROM new_payments
    WHERE mode <> 'Не определено'
    GROUP BY date_trunc('month', date)::DATE, mode
),
conf_total AS (
    SELECT date_trunc('month', date)::DATE AS time,
        COUNT(*) confirmed_count,
        mode
    FROM new_payments
    WHERE mode <> 'Не определено' AND status = 'Confirmed'
    GROUP BY date_trunc('month', date)::DATE, mode
)

SELECT total_payment.time,
    total_payment.mode,
    coalesce((conf_total.confirmed_count::FLOAT / total_payment.total * 100), 0) AS percents
FROM conf_total
RIGHT JOIN total_payment ON
    total_payment.time = conf_total.time AND total_payment.mode = conf_total.mode
ORDER BY total_payment.time,
    total_payment.mode