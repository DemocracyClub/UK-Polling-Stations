# UK-Polling-Stations

This is a work in progress project that needs help in a number of ways:

1. Importing the data we have collected from councils
2. If you are a developer (python, django, frontend, etc) or designer, we need help making the site itself.
3. If you are interested in helping us gather this data, or if you know a lot about the strange world of the UK geographic system.

If you are interested in helping out in any way at all, please contact sym@democracyclub.org.uk

### Getting Started

Requirements

    pip install -r requirements/frist.txt      
    pip install -r requirements/base.txt      

Import initial data

    python manage.py import_councils
    python manage.py loaddata polling_stations/apps/pollingstations/fixtures/initial_data.json

### Importing the data we have from councils

Each council that has unimported data has a Github Issue with the `Data Import` label.

You can see the current status in [the Waffle Board](https://waffle.io/DemocracyClub/UK-Polling-Stations?label=Data%20Import).

Data lives in ./data/[council.id]-[council.name]/*

We make a Django manage.py command in the data_collection app for each council which converts
imports the raw data. There are some base importer command classes in the __init__.py of `data_collection.management.commands`.

We then serialize the imported data to `polling_stations/apps/pollingstations/fixtures/initial_data.json`


### Postgis install notes

Because who does that every week?

#### Creating a database

sudo -u postgres createdb pollingstations
sudo -u postgres createuser dc -P -s
sudo -u postgres psql pollingstations
psql (9.3.6)
Type "help" for help.

pollingstations=# CREATE EXTENSION postgis;
CREATE EXTENSION
pollingstations=#

