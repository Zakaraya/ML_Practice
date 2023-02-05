SELECT sku, dates, AVG(price) price, count(*) qty FROM transactions
GROUP BY sku, dates