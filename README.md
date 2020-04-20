Sheet Without Shit

> [![Build Status](https://travis-ci.com/SheetWithoutShit/SheetWithoutShit.svg?branch=develop)](https://travis-ci.com/SheetWithoutShit/SheetWithoutShit) 

### Overview
TODO

### Installing
1. Install redis:
    ```shell script
    sudo apt-get install redis-server

    # check redis connections
    redis-cli ping
    PONG
    ```
2. Install postgres:
    ```shell script
    sudo apt install postgresql postgresql-contrib
    ```
3. Create user and database:
    ```shell script
    sudo -u postgres psql
    postgres=# CREATE USER <db_user> PASSWORD '<db_password>';
    postgres=# CREATE DATABASE <db_name> OWNER <db_user>;
    ```
4. Initialize database:
    ```shell script
    cd ./postgres
    psql -U <db_user> -d <db_name> -a -f createdb.sql
    ```
5. Install project dependencies:
    ```shell script
    pip install -r ./requirements.txt
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
