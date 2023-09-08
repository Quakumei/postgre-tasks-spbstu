# ====================
# PG Client configuration 
# ====================
PORT=5432
USER=tampio
DATABASE_NAME=car_service
HOST=localhost

# ====================
# Backup configuration
# ====================
BACKUP_DIR=./backups
DATE=$(shell date +"%Y%m%d%H%M")
OUTPUT_BACKUP := /tmp/backup.sql
BACKUP_FILENAME=${BACKUP_DIR}/backup_${DATABASE_NAME}_${DATE}.sql
NUM_BACKUPS := 10
${BACKUP_DIR}:
	mkdir $@

# ====================
# Database targets
# ====================
connection:
	psql -h ${HOST} -p ${PORT} -U ${USER} -d ${DATABASE_NAME}

backup_create: ${BACKUP_DIR}
	pg_dump -h ${HOST} -p ${PORT} -U ${USER} -d ${DATABASE_NAME} -f ${BACKUP_FILENAME} 
	gzip ${BACKUP_FILENAME}

backup_clean: ${BACKUP_DIR}
	rm -rf ${BACKUP_DIR}

backup_restore: ${BACKUP_DIR}
	@echo "Checking for available backups..."
	@BACKUPS=$$(ls -t $(BACKUP_DIR)/*.gz 2>/dev/null | head -n $(NUM_BACKUPS)); \
	if [ -z "$$BACKUPS" ]; then \
		echo "No backups available in $(BACKUP_DIR)"; \
	else \
		echo "Choose a backup to restore from:"; \
		echo "$$BACKUPS" | cat -n; \
		read -p "Enter the number of the backup to restore: " CHOICE; \
		CHOSEN_BACKUP=$$(echo "$$BACKUPS" | sed -n "$$CHOICE p"); \
		if [ -z "$$CHOSEN_BACKUP" ]; then \
			echo "Invalid choice"; \
		else \
			echo "Unpacking the chosen backup to $(OUTPUT_BACKUP)..."; \
			gunzip -c "$$CHOSEN_BACKUP" > $(OUTPUT_BACKUP); \
			echo "Restoring from backup: $(OUTPUT_BACKUP)"; \
			psql -h ${HOST} -U ${USER} -d ${DATABASE_NAME} -f $(OUTPUT_BACKUP); \
		fi; \
	fi
	# Don't forget that {DATABASE_NAME} should be created before restoration
