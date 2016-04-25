[![Stories in Ready](https://badge.waffle.io/democracyclub/uk-polling-stations.png?label=ready&title=Ready)](https://waffle.io/democracyclub/uk-polling-stations)

[![Build Status](https://travis-ci.org/DemocracyClub/UK-Polling-Stations.svg?branch=master)](https://travis-ci.org/DemocracyClub/UK-Polling-Stations)

# UK-Polling-Stations

This is a work in progress project that needs help in a number of ways:

1. Importing the data we have collected from councils ([See Below](https://github.com/DemocracyClub/UK-Polling-Stations#importing-the-data-we-have-from-councils))
2. If you are a developer (python, django, frontend, etc) or designer, we need help making the site itself.
3. If you are interested in helping us gather this data, or if you know a lot about the strange world of the UK geographic system.

If you are interested in helping out in any way at all, please contact sym@democracyclub.org.uk

## Getting Started

### Python
UK-Polling-Stations requires python 3.4

### Install system dependencies
UK-Polling-Stations requires Postgres, PostGIS, libgeos and GDAL.

On Mac OSX, run:
```
brew install postgresql
brew install postgis
brew install geos
brew install gdal
```
From a clean install of Ubuntu 14 (Trusty), the command:
```
sudo apt-get install postgresql-9.3 postgresql-server-dev-9.3 python-psycopg2 python3-dev postgis postgresql-9.3-postgis-2.1 libxml2-dev libxslt-dev
```
will install all of the necessary dependencies.

For other linux distributions, see [here](https://docs.djangoproject.com/en/1.8/ref/contrib/gis/install/geolibs/) for details on installing geospatial libraries for use with Django.

### Install project requirements
```
pip install -r requirements/base.txt
```

### Create database
```
sudo -u postgres createdb pollingstations
sudo -u postgres createuser dc -P -s
sudo -u postgres psql pollingstations
psql (9.3.6)
Type "help" for help.

pollingstations=# CREATE EXTENSION postgis;
CREATE EXTENSION
pollingstations=#
```

### Define database connection
UK-Polling-Stations uses [dj-database-url](https://github.com/kennethreitz/dj-database-url) to manage database connection. To set up a db connection, define an environment variable `DATABASE_URL` of the form `postgis://dc:password@127.0.0.1:5432/pollingstations`

### Run migrations
```
python manage.py migrate
```

### Import initial data

#### Import Councils

```
python manage.py import_councils
```

#### Import some Polling District/Station data

To populate your database, pass `manage.py import -e` a list of [Election IDs](https://democracyclub.org.uk/projects/election-ids/) to run all of the import scripts relating to a particular election or elections. For example:

```
python manage.py import -e parl.2015-05-07
```
will run all of the import scripts relating to the 2015 general election.

```
python manage.py import -e naw.c.2016-05-05 naw.r.2016-05-05
```
will run all of the import scripts relating to the 2016 Welsh Assembly elections.

```
python manage.py import -e ref.2016-06-23
```

will run all of the import scripts relating to the 2016 EU Referendum.


## Importing the data we have from councils

Each council that has unimported data has a Github Issue with the `Data Import` label.

You can see the current status in [the Waffle Board](https://waffle.io/DemocracyClub/UK-Polling-Stations?label=Data%20Import).

Data lives in ./data/[council.id]-[council.name]/*

We make a Django manage.py command in the data_collection app for each council which imports the raw data. There are some base importer command classes in the `__init__.py` of `data_collection.management.commands` and some template import scripts in `polling_stations/apps/data_collection/management/commands/templates/` to use as a starting point.
