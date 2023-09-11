WITH unique_services AS (SELECT service_id FROM works GROUP BY service_id HAVING COUNT(DISTINCT master_id) = 1) SELECT service_id FROM unique_services;
-- TODO: get masters by services by special joining, remove such works
