#! /bin/bash

docker run --name my-db-name -p 5432:5432 -e POSTGRES_USER=user -e POSTGRES_PASSWORD=mysecretpassword --restart=always -d postgres 