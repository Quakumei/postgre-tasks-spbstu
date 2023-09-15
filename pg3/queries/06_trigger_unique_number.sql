-- This must rather be implemented via constraint rather than trigger...
-- However, it is an assignment.
CREATE OR REPLACE FUNCTION enforce_unique_cars_num ()
    RETURNS TRIGGER
    AS $$
BEGIN
    IF EXISTS (
        SELECT
            1
        FROM
            cars
        WHERE
            num = NEW.num) THEN
    RAISE EXCEPTION 'Duplicate value detected for num: %', NEW.num;
END IF;
    RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER unique_num_insert_trigger
    BEFORE INSERT ON cars
    FOR EACH ROW
    EXECUTE FUNCTION enforce_unique_cars_num ();

-- Test
INSERT INTO cars (num, color, mark, is_foreign)
    VALUES ('к999оп999', 'Оранжевый', 'Лада', FALSE);

INSERT INTO cars (num, color, mark, is_foreign)
    VALUES ('к999оп999', 'Оранжевый', 'Лада', FALSE);

