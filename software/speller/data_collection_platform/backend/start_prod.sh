#!/bin/bash

# NOTE: make sure your virtual environment is activated
# starting for developer environ for developers
source .env

# apply database migrations
echo "Applying database migrations"
flask db upgrade

flask run