SELECT
    cars.is_foreign,
    SUM(
        CASE WHEN cars.is_foreign THEN
            services.cost_foreign
        ELSE
            services.cost_our
        END) AS service_cost
FROM
    works
    LEFT JOIN cars ON works.car_id = cars.id
    LEFT JOIN services ON works.service_id = services.id
GROUP BY
    cars.is_foreign
ORDER BY
    service_cost DESC;

