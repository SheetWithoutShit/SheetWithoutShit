# Sheet Without Shit

>[![Travis CI](https://travis-ci.com/SheetWithoutShit/sws.svg?branch=develop)](https://travis-ci.com/SheetWithoutShit/sws)


### Installing [docker]
1. Create `.env` file in the root of the project with the variables provided in [.env](#environment-variables).
2. Run containers:
    ```shell script
    docker-compose up
    ```

### Commands
* Postgres
    * Run SQL script from the file:
    ```shell script
    psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} -a -f <file_name>
    ```
### Environment variables
```shell script
TELEGRAM_BOT_TOKEN=

SECRET_KEY=

SPREADSHEET_REDIRECT_URI=
SPREADSHEET_CLIENT_ID=
SPREADSHEET_CLIENT_SECRET=

POSTGRES_HOST=
POSTGRES_PORT=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
POSTGRES_CONNECTION_MIN_SIZE=
POSTGRES_CONNECTION_MAX_SIZE=

REDIS_HOST=
REDIS_PORT=
REDIS_PASSWORD=
REDIS_TIMEOUT=
REDIS_CONNECTION_MIN_SIZE=
REDIS_CONNECTION_MAX_SIZE=

COLLECTOR_HOST=
COLLECTOR_PORT=

SERVER_HOST=
SERVER_PORT=

LOG_DIR=
```
