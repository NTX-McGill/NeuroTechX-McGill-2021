#!/bin/bash

# NOTE: make sure your virtual environment is activated
# starting for developer environ for developers
source ./.env


if [ "`docker container inspect -f '{{.State.Status}}' db`" == "exited" ];
then
    echo "Starting container db."
    # start database
    docker start db
fi

if [ "`docker container inspect -f '{{.State.Running}}' db`" != "true" ];
then
    echo "Creating container db."
    # start database
    docker run --name db -p ${DEV_DB_PORT}:5432 -e POSTGRES_USER=${DEV_DB_USERNAME} -e POSTGRES_PASSWORD=${DEV_DB_PASSWORD} -d postgres 
fi



if [ "`docker container inspect -f '{{.State.Status}}' rabbitmq`" == "exited" ];
then
    echo "Starting container rabbitmq."
    # start message queue
    docker start rabbitmq 
fi

if [ "`docker container inspect -f '{{.State.Running}}' rabbitmq`" != "true" ];
then
    echo "Creating container rabbitmq."
    # start message queue
    docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 -e RABBITMQ_DEFAULT_USER=${DEV_RABBITMQ_DEFAULT_USER} -e RABBITMQ_DEFAULT_PASS=${DEV_RABBITMQ_DEFAULT_PASSWORD} rabbitmq:3-management
fi



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