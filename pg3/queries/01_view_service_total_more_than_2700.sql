CREATE OR REPLACE VIEW service_total_more_than_2700 AS
WITH service_total_cost AS (
    SELECT
        service_id,
        SUM(
            CASE WHEN cars.is_foreign THEN
                cost_foreign
            ELSE
                cost_our
            END) AS total
    FROM
        works
        LEFT JOIN services ON services.id = works.service_id
        LEFT JOIN cars ON cars.id = works.car_id
    GROUP BY
        service_id
)
SELECT
    *
FROM
    service_total_cost
WHERE
    total > 2700;

-- Test query
SELECT
    *
FROM
    service_total_more_than_2700;

