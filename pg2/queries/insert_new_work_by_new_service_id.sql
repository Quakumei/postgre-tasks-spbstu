WITH new_service_id AS (
    INSERT INTO services (cost_foreign, cost_our, name)
    VALUES (7400, 5000, 'Замена шины')
    RETURNING id
)
INSERT INTO works (car_id, date_work, master_id, service_id)
SELECT 1, '2023-07-08', 1, id FROM new_service_id;

