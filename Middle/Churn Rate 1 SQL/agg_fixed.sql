with all_dates as (select distinct toDate(timestamp) day
                   from default.churn_submits),
     all_users as (select distinct user_id
                   from default.churn_submits),
     agg_values as (SELECT user_id,
                           toDate(timestamp) day,
                           COUNT(submit)           n_submits,
                           COUNT(distinct task_id) n_tasks,
                           SUM(is_solved)          n_solved
                    FROM default.churn_submits
                    GROUP BY user_id, toDate(timestamp))

select all_users.user_id user_id,
       all_dates.day day,
       coalesce(agg_values.n_submits, 0) n_submits,
       coalesce(agg_values.n_tasks, 0)   n_tasks,
       coalesce(agg_values.n_solved, 0)  n_solved
from all_dates
         cross join all_users
         left join agg_values on all_dates.day = agg_values.day and all_users.user_id = agg_values.user_id
order by all_users.user_id, all_dates.day