SELECT cars.id, COALESCE(SUM(CASE WHEN cars.is_foreign THEN services.cost_foreign ELSE services.cost_our END), 0) as total_cost  FROM cars FULL OUTER JOIN works on cars.id = works.car_id LEFT JOIN services on services.id = works.service_id GROUP BY cars.id ORDER BY total_cost DESC; 


