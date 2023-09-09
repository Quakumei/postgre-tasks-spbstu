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

