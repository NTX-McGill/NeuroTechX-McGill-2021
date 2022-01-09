#!/bin/bash

# NOTE: this script assumes that docker is installed and that the user is familiar with Docker.
# NOTE: make sure your virtual environment is activated
# starting for developer environ for developers
source .env

if [ "`docker container inspect -f '{{.State.Running}}' db`" != "true" ];
then
    echo "Creating container db."
    # start database
    docker run --name db -p ${DEV_DB_PORT}:5432 -e POSTGRES_USER=${DEV_DB_USERNAME} -e POSTGRES_PASSWORD=${DEV_DB_PASSWORD} --restart=always -d postgres 
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

flask run