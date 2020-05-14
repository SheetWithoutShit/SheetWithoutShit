# Sheet Without Shit

>[![Travis CI](https://travis-ci.com/SheetWithoutShit/sws.svg?branch=develop)](https://travis-ci.com/SheetWithoutShit/sws)


### Installing [docker]
1. Create `.env` file in the root of the project with the variables provided in [.env](#environment-variables).
2. Run containers:
    ```shell script
    docker-compose up
    ```

### Commands
* Agnostic [[Reference]](https://agnostic.readthedocs.io/en/stable/cli.html#command-line)
    * Bootstrap the migrations table:
    ```shell script
    agnostic -t postgres -u <user> --password <password> -d <db name> -m ./postgres/migrations -h <host> -p <port> bootstrap
    ```
    * Run pending migrations:
    ```shell script
    agnostic -t postgres -u <user> --password <password> -d <db name> -m ./postgres/migrations -h <host> -p <port> migrate
    ```
    * List migrations:
    ```shell script
    agnostic -t postgres -u <user> --password <password> -d <db name> -m ./postgres/migrations -h <host> -p <port> list
    ```
    * Drop migrations table:
    ```shell script
    agnostic -t postgres -u <user> --password <password> -d <db name> -m ./postgres/migrations -h <host> -p <port> drop
    ```
    * Test pending migrations:
    ```shell script
    agnostic -t postgres -u <user> --password <password> -d <db name> -m ./postgres/migrations -h <host> -p <port> test
    ```
* Postgres
    * Run SQL script from the file:
    ```shell script
    psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} -a -f <file_name>
    ```
### Environment variables
```shell script
TELEGRAM_BOT_TOKEN=

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
