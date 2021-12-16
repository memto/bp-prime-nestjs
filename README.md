## Quick Setup (Production)

```bash
bash ./setup.sh
```

## Installation (Development)

```bash
$ npm install
```

## Setup local docker postgres

```bash
$ docker run -d \
    --name app_postgres_dev \
    -p 9432:5432
    -e POSTGRES_PASSWORD=123456a@ \
    -e PGDATA=/var/lib/postgresql/data/pgdata \
    -v <custom-path>:/var/lib/postgresql/data \
    postgres:12
```

## Sync schema

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

## Endpoints (API test)

1. Install the insomnia app (postman like) (https://insomnia.rest/download)
2. Import the `endpoints.json` file
3. Enjoy
