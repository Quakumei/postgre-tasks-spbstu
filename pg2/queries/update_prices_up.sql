BEGIN;
SELECT
    *
FROM
    services;
UPDATE
    services
SET
    cost_our = cost_our * 1.15,
    cost_foreign = cost_foreign * 1.15;
SELECT
    *
FROM
    services;
ROLLBACK;

