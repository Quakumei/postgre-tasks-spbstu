CREATE OR REPLACE PROCEDURE get_mean_price_per_car ()
LANGUAGE SQL
AS $$
    CREATE OR REPLACE TEMPORARY VIEW car_mean_service_price AS (
        SELECT
            cars.id AS car_id,
            COALESCE(AVG(
                    CASE WHEN cars.is_foreign THEN
                        services.cost_foreign
                    ELSE
                        services.cost_our
                    END), 0) AS mean_price
        FROM
            works
        LEFT JOIN services ON services.id = works.service_id
        FULL OUTER JOIN cars ON cars.id = works.car_id
    GROUP BY
        cars.id)
$$;

CALL get_mean_price_per_car ();

SELECT
    *
FROM
    car_mean_service_price;

