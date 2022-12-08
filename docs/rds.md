# RDS

## Working with RDS.

We use Postgres on RDS. Once RDS instance can have multiple postgres DBs in it.

There are different roles, we tend to end up doing everything with the `postgres` role.

#### Connect to RDS

Create a database
```shell
// Connects to 'postgres' db.
you@local-machine:$ `psql postgresql://postgres@wdiv-test.cl0ejuxihujo.eu-west-2.rds.amazonaws.com:5432`

// create a database
postgres=> create database polling_stations;

// ctrl-d or \q to exit psql
```

Install an extension
```shell
// Connects to 'polling_stations' db - note .../polling_stations on end of connection string
you@local-machine:$ psql postgresql://postgres@wdiv-test.cl0ejuxihujo.eu-west-2.rds.amazonaws.com:5432/polling_stations

// create an extension
polling_stations=> create extension postgis;
```

dump a db for loading
```shell
you@local-machine:$ pg_dump -U dc -Fc  polling_stations > polling_stations.dump

// use -s to just dump the schema
pg_dump -U dc -Fc -s  polling_stations > polling_stations.dump
```

```shell
pg_restore \
    -U postgres \
    -h wdiv-test.cl0ejuxihujo.eu-west-2.rds.amazonaws.com \
    -p 5432 \
    -c \
    -j 2 \
    --if-exists \
    --no-owner \
    --no-privileges \
    --role=postgres \
    -d polling_stations \
    polling_stations.dump
```
