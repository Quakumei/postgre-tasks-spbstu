SELECT
    'foreign' AS category,
    COUNT(*) FILTER (WHERE is_foreign) AS count,
    SUM(
        CASE WHEN is_foreign THEN
            cost_foreign
        ELSE
            0
        END) AS sum
FROM
    works
    LEFT JOIN services ON works.service_id = services.id
    LEFT JOIN cars ON works.car_id = cars.id
UNION ALL
SELECT
    'our' AS category,
    COUNT(*) FILTER (WHERE NOT is_foreign) AS count,
    SUM(
        CASE WHEN NOT is_foreign THEN
            cost_our
        ELSE
            0
        END) AS sum
FROM
    works
    LEFT JOIN services ON works.service_id = services.id
    LEFT JOIN cars ON works.car_id = cars.id;

