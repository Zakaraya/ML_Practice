with max_amount as(
    select
    sum(amount)::int as total_amount
    from new_payments
    where status='Confirmed' and mode in ('MasterCard', 'Visa', 'МИР')
    group by email_id
    order by total_amount desc
    limit 1
), amount_user as(
    select
        email_id as id, sum(amount) as total_amount
    from new_payments
    where status='Confirmed' and mode in ('MasterCard', 'Visa', 'МИР')
    group by email_id
    order by total_amount desc
)
select
  case
    when amount_user.total_amount between 0 and 20000 then '0-20000'
    when amount_user.total_amount between 20001 and 40000 then '20000-40000'
    when amount_user.total_amount between 40001 and 60000 then '40000-60000'
    when amount_user.total_amount between 60001 and 80000 then '60000-80000'
    when amount_user.total_amount between 80001 and 100000 then '80000-100000'
    when amount_user.total_amount > 100000 then concat('100000-', (select * from max_amount)::integer)
    END AS purchase_range,
    count(id) as num_of_users
    from
      amount_user
    GROUP BY purchase_range
    ORDER BY MIN(total_amount)