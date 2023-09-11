-- Alternative is to alter table scheme and use
-- ON DELETE CASCADE, so PostgreSQL handles
-- Deletion of car from other tables automatically
DELETE FROM works WHERE car_id = 1;
DELETE FROM cars WHERE id = 1;
