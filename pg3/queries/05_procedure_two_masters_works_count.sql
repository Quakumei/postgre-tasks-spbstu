-- Dynamic SQL
CREATE OR REPLACE PROCEDURE two_masters_total (_master1 int, _master2 int)
LANGUAGE plpgsql
AS $$
DECLARE
    sql_st text;
BEGIN
    sql_st = format('CREATE OR REPLACE TEMPORARY VIEW two_masters_total_result AS ' || '(SELECT master_id, COUNT(id) as works_count FROM works ' || 'WHERE master_id IN (%s, %s) GROUP BY master_id)', _master1, _master2);
    EXECUTE sql_st;
END;
$$;

CALL two_masters_total (3, 4);

SELECT
    *
FROM
    two_masters_total_result;

