WITH sum_units as (
    SELECT user_id, item_id, SUM(units) qty
    FROM default.karpov_express_orders
    GROUP BY user_id, item_id
    )
SELECT user_id, item_id, qty, ROUND(price, 2) price
FROM (SELECT user_id, item_id, avg(price) price
    FROM default.karpov_express_orders
        WHERE timestamp >= %(start_date)s AND timestamp <= %(end_date)s
        GROUP BY user_id, item_id
        ) t1
JOIN sum_units USING(user_id, item_id)
ORDER BY user_id, item_id