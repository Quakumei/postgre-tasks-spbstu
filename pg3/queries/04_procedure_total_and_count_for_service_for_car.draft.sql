CREATE OR REPLACE PROCEDURE get_total_and_count_for_car_for_service (a int, b int)
LANGUAGE SQL
AS $$
    CREATE OR REPLACE TEMPORARY VIEW total_and_count_for_car_for_service_result AS (
        SELECT
            SUM(
                CASE WHEN cars.is_foreign THEN
                    services.cost_foreign
                ELSE
                    services.cost_our
                END) AS total,
            COUNT(works.id)
        FROM
            works
        LEFT JOIN cars ON cars.id = works.car_id
        LEFT JOIN services ON services.id = works.service_id
    WHERE
        works.service_id = a
        AND works.car_id = b
    GROUP BY
        works.car_id)
$$;
CALL get_total_and_count_for_car_for_service (2, 2);
SELECT * FROM total_and_count_for_car_for_service_result;
-- ??? https://stackoverflow.com/questions/77111674/postgresql-sql-how-to-pass-an-argument-to-create-view-in-stored-procedure

