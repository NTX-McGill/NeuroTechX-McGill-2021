# Overview

## Frontend
The frontend is a React App that creates the interfaces for the training and inference platforms. It uses requestAnimationFrame() to animate the key opacities according to a sinusoidal function.

## Backend
The backend is a Flask application with four routes:
- openbci_start: called to create the collection process, returns the process ID
- openbci_stop: called to terminate process with ID
- openbci_process_collect_start: called to start collection for a key
- openbci_process_collect_stop: called to stop collection for a key, returns prediction and autocomplete options

It uses a shared queue to store chunks of data and manages messaging between processes.

# How to run

## OpenBCI GUI

The backend requires a stream of data from OpenBCI GUI. 

Open OpenBCI GUI > Synthetic > 8 chan > Start session > Select "Networking" instead of "Time series" > Change protocol to "LSL" > Select "Timeseries" for "Stream 1" > Start LSL Stream > Start Data Stream 

## Install the anaconda environment

You can find the environment yml files in the backend folder

`conda env create -f environment.yml`
`conda activate environment`

## Environment file

Create a file backend/.env, example:

```
# flask
FLASK_APP=dcp
FLASK_ENV={development or production}
FLASK_RUN_HOST=0.0.0.0

# production settings
DB_USERNAME={DB_USERNAME}
DB_PASSWORD={DB_PASSWORD}

DATABASE_URL={DATABASE_URL}

# development settings
# docker-compose exposes hosts on internal network where the hostname of each service is the same as the name of the service, hence db
DB_HOSTNAME={DB_HOSTNAME}
DEV_DB_USERNAME={DEV_DB_USERNAME}
DEV_DB_PASSWORD={DEV_DB_PASSWORD}

# although container exposes PORT 9999 - composes uses an internal network
# change to 5432 if using docker-compose
DEV_DB_PORT={DEV_DB_PORT}
DEV_DATABASE_URL={DEV_DATABASE_URL}
```

## Run

To run both the frontend and backend:
`./start.sh`

To run the frontend:
`cd frontend`
`npm start`

To run the frontend with installation of dependencies:
`./frontend/start_frontend.sh`

To run the backend for development:
`./backend/start_backend.sh`

To run the backend for production:
`./backend/start_prod.sh`
