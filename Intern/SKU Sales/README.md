# Количество SKU, проданных в разные дни
### Вы работаете в одной крупной FMCG-компании. Ваш руководитель дал задание провести анализ продаж, а первым делом посчитать, сколько товаров компания продает в день.

# Описание задачи
### Вам дан доступ к таблице transactions_another_one, в которой хранится информация о транзакциях. Она содержит следующие поля:
+ calc_date — дата продажи
+ transaction_id — id транзакции
+ _productid_key — уникальный ключ товара
+ store_id — id магазина
+price_per_item — цена за единицу товара
+ dicount — скидка на товар
+ cnt — количество проданного товара

### Напишите запрос и постройте дашборд в Redash с демонстрацией количества SKU, проданных в различные дни.  Сохраните SQL-запрос в файл query.sql и загрузите его в форму ниже.


### Запрос для графика
```sql
SELECT 
    DATE_TRUNC('month', cal_date) days, 
    SUM(cnt) sku 
FROM transactions_another_one
WHERE cal_date > '2021-01-01'
GROUP BY cal_date
ORDER BY days
```

![Chart](/Chart.png)
[Chart link](http://redash.lab.karpov.courses/embed/query/25642/visualization/53045?api_key=cVvTlbpK3sv6WSewya3e3XkCGPEGL6NkctKfCMw2&)