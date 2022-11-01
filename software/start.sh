#!/bin/bash

#start backend
#- open env
#- check prod or dev
#- startbackend or startprod

echo "$PWD"

source ./backend/.env

echo "$FLASK_ENV"

if [ "$FLASK_ENV" = "development" ];
then
    cd ./backend/
    bash start_backend.sh
    echo "Starting in development mode"

elif [ "$FLASK_ENV" = "production" ]
then
    ./backend/
    bash start_prod.sh
    echo "Starting in production mode"
fi

bash ../frontend/start_frontend.sh