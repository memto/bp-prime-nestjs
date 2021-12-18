## Installation (Development)

```bash
$ npm install
```

## Setup local docker postgres

```bash
$ docker run -d \
    --name app_postgres_dev \
    -p 9432:5432 \
    -e POSTGRES_PASSWORD=123456a@ \
    -e PGDATA=/var/lib/postgresql/data/pgdata \
    -v <custom-path>:/var/lib/postgresql/data \
    postgres:12
```

## Sync schema (this will create tables into database)

```bash
$ npm run schema:sync
```

## Running the app

```bash
# copy and update .env (ex: change postgres password)
cp .env.example .env

# development
$ npm run start

# watch mode
$ npm run start:dev

# production mode
$ npm run start:prod
```

## Import DB

```bash
$ sudo docker cp <path_to_generated_csv> app_postgres_dev:/tmp/output.csv
$ sudo docker exec app_postgres_dev psql -U postgres -d postgres -c "\copy translation FROM '/tmp/output.csv' DELIMITER E'\t'"
```

- Import to https://customer.elephantsql.com/instance
```bash
$ cd scripts
$ sudo apt install python3-venv
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
# config .env
$ python ./import_db.py <CSV_FILE> <TABLE_NAME>
```

## Heroku deploy

```bash
$ heroku config -a century-be-demo

=== century-be-demo Config Vars
NODE_ENV:              production
NPM_CONFIG_PRODUCTION: false
POSTGRES_DB:           <POSTGRES_DB>
POSTGRES_HOST:         <POSTGRES_HOST>
POSTGRES_PASSWORD:     <POSTGRES_PASSWORD>
POSTGRES_PORT:         <POSTGRES_PORT>
POSTGRES_SSL:          <POSTGRES_SSL>
POSTGRES_USER:         <POSTGRES_USER>
PRIVATE_KEY:           <PRIVATE_KEY>
PUBLIC_KEY:            <PUBLIC_KEY>
```

## Endpoints (API test)

1. Install the insomnia app (postman like) (https://insomnia.rest/download)
2. Import the `Insomnia_2021-12-17.json` file
3. Enjoy