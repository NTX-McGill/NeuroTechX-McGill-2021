#! /bin/bash

docker run --name my-db-name -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword -d postgres