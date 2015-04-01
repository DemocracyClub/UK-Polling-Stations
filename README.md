# UK-Polling-Stations

This is a work in progress project that needs help in a number of ways:

1. If you are in a Council, or related to one in some way, can you get us either of the following types of data:
    1. Polling station addresses for 2015
    2. Polling district shapefiles per polling district
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

