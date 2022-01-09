# Data Collection Platform Backend

## Setup environment

If you are setting up on Linux install the package `sudo apt install libpq-dev`
If you are setting up on Mac install the package using Homebrew instead

1. For Linux, Create environment using conda: `conda env create -f environment.yml`
    - For Windows: `conda env create -f environment_windows.yml`
    - *TODO create environment_windows.yml (for devs working on Windows)
    - For MacOS: `conda env create -f environment_macOS.yml`

## Running the application

Prerequisite: A development or production database is running and healthy.
```
$ flask run
```

## Connecting to OpenBCI GUI with synthetic data
1. Download the OpenBCI GUI
   - https://openbci.com/downloads

2. Open the app, click "Synthetic (algorithmic)" --> "8 chan" --> START SESSION --> Start Data Stream.
3. Select "Networking" on one of the dropdowns, choose LSL protocol, select a data type (TimeSeries) then click "Start LSL Stream"
4. Run the application as shown above
5. Open a web browser and go to URLSHOWNINCONSOLEFORFLASKAPP/


## Connecting to the database
TODO: Update this part

The database credentials can be found on the `software` channel on Slack.
One can use the `psql` CLI to connect to the database: `psql --host=neurotech-db.postgres.database.azure.com --port=5432 --username=neurotech@neurotech-db --dbname=postgres`

Alternatively, see https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/#a-minimal-application to interact with the database using python.

For example:
```
>>> from models.data import CollectedData
>>> CollectedData.query.all()
[<CollectedData>, ..., <CollectedData>]
```

## Development database
TODO: Update this part

In order to not corrupt the production database, we should use a development database when developing the application. There are two options to setup such database locally: 
1.  Using docker: ``docker run --name <my-db-name> -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword -d postgres``
    - Altertive: Install the PostgreSQL server [here](https://www.postgresql.org/download/)

Then update the `DB_USERNAME`, `DB_PASSWORD` and `DATABASE_URL` to the configurations of your local database. 
For example, if I used docker to start a postgres server on my local machine, then I would have in my `.env` file:
- DB_USERNAME=postgres
- DB_PASSWORD=mysecretpassword
- DATABASE_URL=postgresql://${DB_USERNAME}:${DB_PASSWORD}@localhost:5432/postgres
