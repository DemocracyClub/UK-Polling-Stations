[![Build Status](https://circleci.com/gh/DemocracyClub/UK-Polling-Stations.svg?style=svg)](https://circleci.com/gh/DemocracyClub/UK-Polling-Stations) [![Coverage Status](https://coveralls.io/repos/github/DemocracyClub/UK-Polling-Stations/badge.svg)](https://coveralls.io/github/DemocracyClub/UK-Polling-Stations) ![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)

# UK-Polling-Stations

This is a work in progress project that needs help in a number of ways:

1. Importing the data we have collected from councils ([See Below](https://github.com/DemocracyClub/UK-Polling-Stations#importing-the-data-we-have-from-councils))
2. If you are a developer (python, django, frontend, etc) or designer, we need help making the site itself.
3. If you are interested in helping us gather this data, or if you know a lot about the strange world of the UK geographic system.

If you are interested in helping out in any way at all, please contact sym@democracyclub.org.uk

## Getting Started

### Python
UK-Polling-Stations requires python 3.6

### Install system dependencies
UK-Polling-Stations requires Python 3.6, Postgres, PostGIS, libgeos, GDAL, Node JS and NPM.

On Mac OSX, run:
```
brew install postgresql
brew install postgis
brew install geos
brew install gdal
brew install node
```

From a clean install of Ubuntu 18.04 (Bionic):
```
sudo apt-get install postgresql-10 postgresql-server-dev-all python-psycopg2 python3-dev postgis postgresql-10-postgis-2.4 libxml2-dev libxslt1-dev nodejs npm

sudo npm install -g npm@latest-6
```

For other linux distributions, see [here](https://docs.djangoproject.com/en/2.2/ref/contrib/gis/install/geolibs/) for details on installing geospatial libraries for use with Django.

The API docs rely on [drafter](https://github.com/apiaryio/drafter/) for parsing API Blueprint. This does not need to be installed manually on linux.
**This currently cannot be done on OSX; Refer to [this issue](https://github.com/DemocracyClub/UK-Polling-Stations/issues/1400) for more details.**

### Install python dependencies
```
pip install -r requirements/base.txt
```

### Install front-end dependencies
```
npm install
```

### Install testing python dependencies
```
pip install -r requirements/testing.txt
```

### Install testing system dependencies
We have a suite of end-to-end integration tests. We use [Playwright](https://playwright.dev/python/)
with `pytest` to run these.

To set up playwright, after running `pip install -r requirements/testing.txt`,
run `playwright install`. This will download the browser biniaries required
for your system.

### Create local config
```
cp polling_stations/settings/local.example.py polling_stations/settings/local.py
```

### Create database
```
sudo -u postgres createdb polling_stations
sudo -u postgres createuser dc -P -s
sudo -u postgres psql polling_stations
psql (9.3.6)
Type "help" for help.

polling_stations=# CREATE EXTENSION postgis;
CREATE EXTENSION
polling_stations=#
```

### Update local.py
Be sure that your database user name matches
To check, run:
`psql postgres`
then:
`\l`
### Run migrations
```
python manage.py migrate
```

### Import initial data

#### Import ONSPD

For development purposes, you can use the ONSPD for geocoding. Grab the latest release from https://geoportal.statistics.gov.uk/search?collection=Dataset&sort=-modified&tags=PRD_ONSPD unzip the data and import it using:

```
python manage.py import_onspd /path/to/data
```

N.B. Path is to data _directory_ which contains the csv, not the csv itself.

#### Import Councils

```
python manage.py import_councils
```

#### Import some Polling District/Station data

For development purposes, you will need to seed your database with some data.
We depend on Ordnance Survey Addressbase Plus, which is not publicly available.
To allow open source contributions we have prepared the sample data Ordnance Survey
provide (https://www.ordnancesurvey.co.uk/business-government/products/addressbase-plus#sample-data)
ready for import, and some sample import scripts for testing.

To prepare your database run the following commands:

```
./manage.py import_cleaned_addresses test_data/addressbase/
./manage.py create_uprn_council_lookup
./manage.py import_uprn_council_lookup uprn-to-councils.csv
```

You can clean up the look up with:

```
rm uprn-to-councils.csv
```

And finally you can import some dummy data with:

```
./manage.py import_fake_teignbridge
./manage.py import_fake_exeter
```

## Importing the data we have from councils

Each council that has unimported data has a Github Issue with the [Data Import](https://github.com/DemocracyClub/UK-Polling-Stations/issues?q=is%3Aissue+is%3Aopen+label%3A%22Data+Import%22) label.

We make a Django `manage.py` command in the data_importers app for each council which imports the raw data.
If you are interested in helping the project by writing an import script, see the issues tagged [recommended for beginners](https://github.com/DemocracyClub/UK-Polling-Stations/issues?q=is%3Aissue+is%3Aopen+label%3A%22recommended+for+beginners%22) for more info.

## Welsh Language translations
`./manage.py compilemessages`

## Install git hooks

If you like you can use the commit hooks defined in `.pre-commit-config.yaml`. Run `pre-commit install && pre-commit install -t pre-push`.
