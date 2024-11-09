WITH CTE AS (
    SELECT state_id, state_name,
           ROW_NUMBER() OVER(PARTITION BY state_id, state_name ORDER BY state_id) AS row_num
    FROM state_table
)
DELETE FROM CTE WHERE row_num > 1;
