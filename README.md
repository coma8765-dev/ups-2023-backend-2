# UPS 2023 Backend 2
*Made by [Nikita Ananev](https://github.com/coma8765-dev)*

## Run with docker
```shell
docker compose -f templates/docker-compose.yaml up -d --build
```

## Run without Docker

### Install deps
```shell
pip install pipenv
pipenv install
```

### Prepare Postgres Database 
#### Default params
```yaml
POSTGRES_USER: 'postgres'
POSTGRES_PASSWORD: 'password'
POSTGRES_HOST: 'localhost'
POSTGRES_PORT: 5432
POSTGRES_DATABASE: 'postgres'
```
> For change, it [creates `.env` file with this vars](https://www.codementor.io/@parthibakumarmurugesan/what-is-env-how-to-set-up-and-run-a-env-file-in-node-1pnyxw9yxj)

### Run
```shell
pipenv run python -m app
```
