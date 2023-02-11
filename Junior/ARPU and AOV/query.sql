SELECT
    date_trunc('month', date)::DATE AS time,
    sum(amount) / count(distinct email_id) AS ARPPU,
    sum(amount) / count(distinct id) AS AOV

FROM new_payments
WHERE status = 'Confirmed'
GROUP BY date_trunc('month', date)::DATE
ORDER BY time