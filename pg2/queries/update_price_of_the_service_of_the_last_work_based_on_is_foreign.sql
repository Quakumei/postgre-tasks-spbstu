BEGIN;
WITH latest_service_id_is_foreign AS (
    SELECT
        service_id,
        cars.is_foreign
    FROM
        works
        LEFT JOIN cars ON works.car_id = cars.id
    ORDER BY
        date_work DESC,
        works.id DESC
    LIMIT 1)
UPDATE
    services
SET
    cost_foreign = (
        CASE WHEN (
            SELECT
                is_foreign
            FROM
                latest_service_id_is_foreign) THEN
            cost_foreign + 10
        ELSE
            cost_foreign
        END),
cost_our = (
    CASE WHEN NOT (
        SELECT
            is_foreign
        FROM
            latest_service_id_is_foreign) THEN
        cost_our + 10
    ELSE
        cost_our
    END)
WHERE
    services.id = (
        SELECT
            service_id
        FROM
            latest_service_id_is_foreign);
ROLLBACK;

