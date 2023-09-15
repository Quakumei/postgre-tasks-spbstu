CREATE OR REPLACE FUNCTION restrict_delete_car_if_exists_in_works ()
    RETURNS TRIGGER
    AS $$
BEGIN
    IF EXISTS (
        SELECT
            1
        FROM
            works
        WHERE
            works.car_id = OLD.id) THEN
    RAISE EXCEPTION 'There are works related to this car which remain in works table: %', OLD.id;
END IF;
    RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER car_delete_constraint_in_works BEFORE DELETE ON cars FOR EACH ROW EXECUTE FUNCTION restrict_delete_car_if_exists_in_works ();

-- test
DELETE FROM cars
WHERE id = 2;

