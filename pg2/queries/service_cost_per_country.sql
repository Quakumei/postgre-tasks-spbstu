SELECT cars.is_foreign, SUM(CASE WHEN cars.is_foreign then services.cost_foreign else services.cost_our END) as service_cost from works LEFT JOIN cars ON works.car_id = cars.id LEFT JOIN services on works.service_id = services.id GROUP BY cars.is_foreign ORDER BY service_cost DESC;


