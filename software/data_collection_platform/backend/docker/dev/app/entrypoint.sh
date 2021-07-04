#!/bin/bash

# verify that database is healthy before applying the migrations and running server
while ! nc -z $DB_HOSTNAME $DEV_DB_PORT; 
do
    sleep 0.5
    echo "Waiting for database..."
done

echo "Database started"

# apply database migrations
echo "Applying database migrations"
flask db upgrade

echo "Populating video table with videos from Data Team Google Sheet"
python db_utils.py

echo "Running command '$*'"
exec $*