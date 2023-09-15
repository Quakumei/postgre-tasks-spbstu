CREATE OR REPLACE PROCEDURE get_total_and_count_for_car_for_service (a int, b int)
LANGUAGE plpgsql
AS $$
DECLARE
    sql text;
BEGIN
    sql = format('CREATE OR REPLACE TEMPORARY VIEW total_and_count_for_car_for_service_result AS ( ' || 'SELECT SUM(CASE WHEN cars.is_foreign THEN services.cost_foreign ELSE services.cost_our END) AS total, ' || 'COUNT(works.id) FROM works LEFT JOIN cars ON cars.id = works.car_id ' || 'LEFT JOIN services ON services.id = works.service_id WHERE ' || 'works.service_id = %s AND works.car_id = %s GROUP BY works.car_id)', a, b);
    EXECUTE SQL;
END;
$$;

CALL get_total_and_count_for_car_for_service (2, 2);

SELECT
    *
FROM
    total_and_count_for_car_for_service_result;

