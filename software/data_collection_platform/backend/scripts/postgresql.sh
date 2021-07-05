#! /bin/bash

docker run --name db -p ${DEV_DB_PORT}:5432 -e POSTGRES_USER=${DEV_DB_USERNAME} -e POSTGRES_PASSWORD=${DEV_DB_PASSWORD} --restart=always -d postgres 