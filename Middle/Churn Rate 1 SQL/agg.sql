SELECT
    user_id,
    toDate(timestamp) day,
    COUNT(submit) n_submits,
    COUNT(distinct task_id) n_tasks,
    SUM(is_solved) n_solved
FROM default.churn_submits
GROUP BY user_id, toDate(timestamp)
ORDER BY user_id, day