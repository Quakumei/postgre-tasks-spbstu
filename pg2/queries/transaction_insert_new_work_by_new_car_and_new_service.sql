BEGIN;
WITH new_car_id AS (
INSERT INTO cars (num, color, mark, is_foreign)
        VALUES ('у777яр964', 'Чёрный', 'Mercedes', TRUE)
    RETURNING
        id
), new_service_id AS (
INSERT INTO services (cost_foreign, cost_our, name)
        VALUES (2650, 1250, 'Полировка сидений')
    RETURNING
        id)
    INSERT INTO works (master_id, car_id, service_id, date_work)
    SELECT
        1, (
            SELECT
                id
            FROM new_car_id),
    (
        SELECT
            id
        FROM
            new_service_id),
    '2023-09-09';
COMMIT;

