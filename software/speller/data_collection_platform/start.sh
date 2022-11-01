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
    bash ./backend/start_prod.sh
    echo "Starting in production mode"
fi

#start frontend
#- conda activate dcp
#- install sklearn and scikit?
#- npm install
#- conda develop (signals folder)
#- npm start

#conda activate dcp
#conda develop ./backend/dcp/signals

#cd frontend
#npm install
#npm start