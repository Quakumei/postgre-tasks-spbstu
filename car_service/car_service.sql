-- Создание базы данных
CREATE DATABASE car_service;

-- Использование созданной базы данных
\c car_service;

-- Создание таблицы "cars" с автоинкрементом для id
CREATE TABLE cars (
    id SERIAL PRIMARY KEY,
    num VARCHAR(20) NOT NULL,
    color VARCHAR(20),
    mark VARCHAR(20),
    is_foreign BOOLEAN
);

-- Создание таблицы "masters" с автоинкрементом для id
CREATE TABLE masters (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);
CREATE TABLE services (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    cost_our NUMERIC(18, 2),
    cost_foreign NUMERIC(18, 2)
);
CREATE TABLE works (
    id SERIAL PRIMARY KEY,
    date_work DATE,
    master_id INT REFERENCES masters(id),
    car_id INT REFERENCES cars(id),
    service_id INT REFERENCES services(id)
);

-- Создание связи fk_works_cars между таблицами cars и works
ALTER TABLE works
ADD CONSTRAINT fk_works_cars
FOREIGN KEY (car_id)
REFERENCES cars(id);

-- Создание связи fk_works_masters между таблицами masters и works
ALTER TABLE works
ADD CONSTRAINT fk_works_masters
FOREIGN KEY (master_id)
REFERENCES masters(id);

-- Создание связи fk_works_services между таблицами services и works
ALTER TABLE works
ADD CONSTRAINT fk_works_services
FOREIGN KEY (service_id)
REFERENCES services(id);


--
-- Data for Name: cars; Type: TABLE DATA; Schema: public; Owner: tampio
--

COPY public.cars (id, num, color, mark, is_foreign) FROM stdin;
1	а905ав777	Красный	Honda	t
2	б123ка717	Белый	Лада	f
3	б128кф939	Чёрный	Лада	f
4	а888щл913	Фиолетовый	Mazda	t
5	г123ар834	Бирюзовый	УАЗ	f
\.


--
-- Data for Name: masters; Type: TABLE DATA; Schema: public; Owner: tampio
--

COPY public.masters (id, name) FROM stdin;
1	Василий
2	Сергей
3	Юлиана
4	Анатолий
5	Пётр
\.


--
-- Data for Name: services; Type: TABLE DATA; Schema: public; Owner: tampio
--

COPY public.services (id, name, cost_our, cost_foreign) FROM stdin;
1	Мытьё машины	575.00	1725.00
2	Замена карбюратора	5750.00	8625.00
3	Смена резины	2875.00	4600.00
\.


--
-- Data for Name: works; Type: TABLE DATA; Schema: public; Owner: tampio
--

COPY public.works (id, date_work, master_id, car_id, service_id) FROM stdin;
1	2023-01-25	1	1	1
2	2023-01-26	2	2	2
3	2023-01-27	3	3	3
4	2023-01-27	1	3	2
\.

--
-- Хранимая процедура
--

CREATE OR REPLACE FUNCTION service_cost_by_foreignness(date_one text, date_two text)
    RETURNS TABLE(is_foreign BOOLEAN, service_cost NUMERIC) AS $$
BEGIN
    RETURN QUERY
    SELECT
    cars.is_foreign,
    SUM(
        CASE WHEN cars.is_foreign THEN
            services.cost_foreign
        ELSE
            services.cost_our
        END) AS service_cost
FROM
    works
    LEFT JOIN cars ON works.car_id = cars.id
    LEFT JOIN services ON works.service_id = services.id
    WHERE date_work >= TO_DATE(date_one,'YYYY-MM-DD') 
    AND date_work <= TO_DATE(date_two, 'YYYY-MM-DD')
GROUP BY
    cars.is_foreign
ORDER BY
    service_cost DESC;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION top_five_masters(date_one text, date_two text)
    RETURNS TABLE(master_id INT, master_name VARCHAR(50), works_count BIGINT) AS $$
BEGIN
    RETURN QUERY
    SELECT 
    masters.id as master_id, 
    masters.name as master_name, 
    COUNT(1) as works_count 
FROM works 
    LEFT JOIN masters ON works.master_id = masters.id 
    WHERE works.date_work >= TO_DATE(date_one,'YYYY-MM-DD') 
    AND works.date_work <= TO_DATE(date_two, 'YYYY-MM-DD') 
GROUP BY masters.id 
ORDER BY 
    COUNT(1) DESC 
LIMIT 5;
END;
$$ LANGUAGE plpgsql;

