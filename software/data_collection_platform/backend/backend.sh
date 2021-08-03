#!/bin/bash

source .env

# NOTE: make sure your virtual environment is activated
# apply database migrations
echo "Applying database migrations"
flask db upgrade

echo "Populating video table with videos from Data Team Google Sheet"
python db_utils.py

# starting a celery worker
celery -A dcp.run_celery.celery worker --loglevel=info > logs/celery.log 2>&1 &
flask run