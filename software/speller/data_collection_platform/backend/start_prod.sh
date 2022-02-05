#!/bin/bash

# NOTE: make sure your virtual environment is activated
# starting for developer environ for developers
source .env

# verify that database is healthy before applying the migrations and running server
while ! nc -z $AWS_RDS_URL $AWS_RDS_PORT; 
do
    sleep 0.5
    echo "Waiting for database..."
done

echo "Database started"

# apply database migrations
echo "Applying database migrations"
flask db upgrade

flask run