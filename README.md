# _Forex - Django Clean Architecture_

This repository contains the code for Forex API backend. The application aims to provide information for all currencies, latests and historical time series exchange rates for currency pairs, currency conversion and time weighted rates calculation.

## Documentation
This project has been developed using [Django][django] and [Django Rest Framework][djangorestframework], with [Celery][celery] as background tasks runner, [Postgres][postgres] as relational database and [Redis][redis] as cache service.

Code structure implementation follows a [Clean Architecture][cleanarchitecture] approach, emphasizing on code readability, responsibility decoupling and unit testing.

For API backend endpoints documentation refer to the [forex yaml][swagger] file in the docs directory.

## Setup

Download source code cloning this repository:
```
git clone https://github.com/sdediego/forex-django-clean-architecture.git
```

Get free API Key for the following exchange rate services:
1. https://fixer.io/
2. https://xchangeapi.com/
3. https://www.exchangerate-api.com/

Later update database with each value for the corresponding provider _api_key_ setting using the backend admin panel.

## Run the API backend:
Create docker images and execute the containers. From the project directory:
```
docker-compose -f ./docker/docker-compose.yaml -f ./docker/docker-compose.dev.yaml up
```

Shutdown the application and remove network and containers gracefully:
```
docker-compose -f ./docker/docker-compose.yaml -f ./docker/docker-compose.dev.yaml down
```

## Execute tests suite
1. Access running _forex_api_ docker container shell:
```
docker exec -it forex_api bash
```
2. Execute pytest command from project directory:
```
pytest
```

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job.)

[django]: <https://www.djangoproject.com>
[djangorestframework]: <https://www.django-rest-framework.org>
[celery]: <https://docs.celeryproject.org>
[postgres]: <https://www.postgresql.org>
[redis]: <https://redis.io>
[cleanarchitecture]: <https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html>
[swagger]: <https://github.com/sdediego/forex-django-clean-architecture/docs/forex.yaml>
