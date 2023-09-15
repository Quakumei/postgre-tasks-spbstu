-- Result in a wrong way
-- WITH mastersalary AS (WITH masterbonus AS (WITH bonus_part_calc AS (WITH mastercar_earnings AS (SELECT master_id, car_id, SUM(CASE WHEN cars.is_foreign THEN cost_foreign ELSE cost_our END) AS total_earned, COUNT(works.id) as service_qty FROM works LEFT JOIN services ON services.id = service_id LEFT JOIN cars ON cars.id = car_id WHERE NOW()-date_work < '30 days' GROUP BY master_id, car_id) SELECT *, (CASE WHEN mastercar_earnings.service_qty >= 3 THEN 0.07 ELSE 0.05 END) AS bonus_part from mastercar_earnings) SELECT *, bonus_part_calc.total_earned * bonus_part as bonus_abs from bonus_part_calc) SELECT master_id, SUM(bonus_abs) AS total_bonus, 45000 as salary from masterbonus GROUP BY master_id) SELECT master_id, total_bonus + salary as payment FROM mastersalary;
CREATE OR REPLACE PROCEDURE calculate_salary_and_bonus (_master_id int, _salary int)
    AS $$
DECLARE
    total_bonus float := 0;
    service_qty int := 0;
    car_id int;
    is_foreign boolean;
    service_row RECORD;
    car_row RECORD;
    _payment float;
BEGIN
    -- Создаем курсор для работы с услугами мастера за текущий месяц
    FOR service_row IN
    SELECT
        w.car_id,
        c.is_foreign
    FROM
        works w
        JOIN services s ON w.service_id = s.id
        JOIN cars c ON w.car_id = c.id
    WHERE
        w.master_id = _master_id
        AND NOW() - w.date_work < interval '30 days' LOOP
            -- Подсчитываем количество услуг для данной машины
            service_qty := 0;
            FOR car_row IN
            SELECT
                w.car_id
            FROM
                works w
                JOIN services s ON w.service_id = s.id
            WHERE
                w.master_id = _master_id
                AND w.car_id = service_row.car_id
                AND NOW() - w.date_work < interval '30 days' LOOP
                    service_qty := service_qty + 1;
                END LOOP;
            -- Рассчитываем премию в зависимости от количества услуг
            IF service_qty >= 3 THEN
                total_bonus := total_bonus + (_salary * 0.07);
            ELSE
                total_bonus := total_bonus + (_salary * 0.05);
            END IF;
        END LOOP;
    -- Считаем общую выплату
    _payment := _salary + total_bonus;
    EXECUTE 'CREATE TEMPORARY VIEW temp_payment_view AS SELECT ' || _payment::text || ' AS payment';
END;
$$
LANGUAGE plpgsql;

-- Test
CALL calculate_salary_and_bonus (1, 45000);

SELECT
    *
FROM
    temp_payment_view;

