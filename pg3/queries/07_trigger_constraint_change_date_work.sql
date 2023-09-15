CREATE OR REPLACE FUNCTION enforce_update_constraint_work_date ()
    RETURNS TRIGGER
    AS $$
BEGIN
    IF ABS(DATE_PART('days', OLD.date_work::timestamp - NEW.date_work::timestamp)) > 1 THEN
        RAISE EXCEPTION 'date change is too big for works: %', NEW.date_work;
    END IF;
    RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER works_date_update_constraint_change BEFORE UPDATE ON works FOR EACH ROW EXECUTE FUNCTION enforce_update_constraint_work_date ();

-- Test
UPDATE
    works
SET
    date_work = '2023-09-07'
WHERE
    id = 8;

UPDATE
    works
SET
    date_work = '2023-09-11'
WHERE
    id = 8;

UPDATE
    works
SET
    date_work = '2023-09-10'
WHERE
    id = 8;

UPDATE
    works
SET
    date_work = '2023-09-09'
WHERE
    id = 8;

