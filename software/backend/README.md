# Data Collection Platform Backend

## Setup environment

If you are setting up on Linux install the package `sudo apt install libpq-dev`

If you are setting up on Mac install the package use Homebrew to install this package.

1. For Linux, Create environment using conda: `conda env create -f environment.yml`
    - For Windows: `conda env create -f environment_windows.yml`
    - *TODO create environment_windows.yml (for devs working on Windows)
    - For MacOS: `conda env create -f environment_macOS.yml`
2. Create a `.env` file in the current directory (`software/speller/data_collection_platform/.env`). Its content can be found in the **#software** channel.
## Database migrations

We are using the [`Flask-Migrate`](https://flask-migrate.readthedocs.io/en/latest/) package to manage database migrations.

At the beginning, we need to create a migration repository with the following command:

```
$ flask db init
```

This will add a migrations folder to your application. The contents of this folder need to be added to version control along with your other source files.

Every time some modifies the database table, please generate a migration:

```
$ flask db migrate -m "Detail message about what has changed."
```

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

The database credentials can be found on the `software` channel on Slack - put them inside of a file called `.env` at the `software/speller/data_collection_platform/backend` directory. Then using the `psql` CLI to connect to the database:
```
source .env
psql ${DATABASE_URL}
```

Alternatively, see https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/#a-minimal-application to interact with the database using python.

For example:
```
>>> from models.data import CollectedData
>>> CollectedData.query.all()
[<CollectedData>, ..., <CollectedData>]
```

## Development database

In order to not corrupt the production database, we should use a development database when developing the application. The database credentials can be found on the `software` channel on Slack - put them inside of a file called `.env` at the `software/speller/data_collection_platform/backend` directory. There are two options to setup such database locally: 
1.  Using docker: 
```
cd software/speller/data_collection_platform/backend
source .env
docker run --name db -p ${DEV_DB_PORT}:5432 -e POSTGRES_USER=${DEV_DB_USERNAME} -e POSTGRES_PASSWORD=${DEV_DB_PASSWORD} --restart=always -d postgres 
```
2. Running PostgreSQL locally: Install the PostgreSQL server [here](https://www.postgresql.org/download/) and run the database server locally
