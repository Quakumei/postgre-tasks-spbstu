CREATE VIEW last_year_masters_earnings AS (
    WITH master_total AS (
        SELECT
            masters.id,
            masters.name,
            COALESCE(SUM(
                    CASE WHEN cars.is_foreign THEN
                        services.cost_foreign
                    ELSE
                        services.cost_our
                    END), 0) AS total_earned
        FROM
            works
        LEFT JOIN cars ON cars.id = works.car_id
        LEFT JOIN services ON services.id = service_id
        LEFT JOIN masters ON masters.id = master_id
    WHERE
        works.date_work > now() - interval '1 year'
    GROUP BY
        masters.id
)
    SELECT
        masters.id,
        masters.name,
        COALESCE(total_earned, 0) AS total_earned
    FROM
        master_total
    FULL OUTER JOIN masters ON masters.id = master_total.id
ORDER BY
    total_earned DESC);

-- Testing
SELECT
    *
FROM
    masters;

SELECT
    *
FROM
    works;

SELECT
    *
FROM
    last_year_masters_earnings;

