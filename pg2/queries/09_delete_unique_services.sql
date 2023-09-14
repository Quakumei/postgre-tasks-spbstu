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
ROLLBACK;

-- Select the master whos work to delet eby works.master_id = 1; --
