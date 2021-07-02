#! /bin/bash

docker run --name db -p 9999:5432 -e POSTGRES_USER=user -e POSTGRES_PASSWORD=mysecretpassword --restart=always -d postgres 