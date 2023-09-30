PORT=5432
USER=tampio
DATABASE_NAME=car_service
HOST=localhost

DB_FILE=./car_service_initdb.sql


connection:
	psql -h ${HOST} -p ${PORT} -U ${USER} -d ${DATABASE_NAME}

recreate_db:
	psql -h ${HOST} -p ${PORT} -U ${USER} -d ${DATABASE_NAME} -f ${DB_FILE}
	
