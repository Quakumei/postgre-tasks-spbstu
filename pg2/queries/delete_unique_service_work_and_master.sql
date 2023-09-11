BEGIN;
WITH unique_services AS (
    SELECT
        service_id
    FROM
        works
    GROUP BY
        service_id
    HAVING
        COUNT(DISTINCT master_id) = 1)
DELETE FROM works
WHERE works.service_id IN (
        SELECT
            service_id
        FROM
            unique_services)
    AND works.master_id = 1;
DELETE FROM works
WHERE master_id = 1;
DELETE FROM masters
WHERE id = 1;
ROLLBACK;

