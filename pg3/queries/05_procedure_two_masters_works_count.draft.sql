SELECT master_id, COUNT(id) as works_count FROM works WHERE master_id = 1 OR master_id = 2 GROUP BY master_id;

