#!/bin/bash

# NOTE: make sure your virtual environment is activated
# starting for developer environ for developers
source ./.env

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

# starting a celery worker
celery -A dcp.run_celery.celery worker --loglevel=info > logs/celery.log 2>&1 &
flask run