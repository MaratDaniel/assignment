#!/bin/bash
# Script to export PostgreSQL database to SQL file

# Database configuration
DB_NAME="caregivers_db"
DB_USER="postgres"
DB_HOST="localhost"
OUTPUT_FILE="caregivers_db_export.sql"

# Export database
echo "Exporting database $DB_NAME to $OUTPUT_FILE..."
pg_dump -h $DB_HOST -U $DB_USER -d $DB_NAME > $OUTPUT_FILE

if [ $? -eq 0 ]; then
    echo "Database exported successfully to $OUTPUT_FILE"
else
    echo "Error exporting database. Please check your database connection settings."
    exit 1
fi

