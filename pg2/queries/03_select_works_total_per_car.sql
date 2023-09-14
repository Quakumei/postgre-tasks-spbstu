SELECT
    cars.id,
    COALESCE(SUM(
            CASE WHEN cars.is_foreign THEN
                services.cost_foreign
            ELSE
                services.cost_our
            END), 0) AS total_cost
FROM
    cars
    FULL OUTER JOIN works ON cars.id = works.car_id
    LEFT JOIN services ON services.id = works.service_id
GROUP BY
    cars.id
ORDER BY
    total_cost DESC;

