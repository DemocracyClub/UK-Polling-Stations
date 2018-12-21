[![Stories in Ready](https://badge.waffle.io/democracyclub/uk-polling-stations.png?label=ready&title=Ready)](https://waffle.io/democracyclub/uk-polling-stations)

[![Build Status](https://travis-ci.org/DemocracyClub/UK-Polling-Stations.svg?branch=master)](https://travis-ci.org/DemocracyClub/UK-Polling-Stations) [![Coverage Status](https://coveralls.io/repos/github/DemocracyClub/UK-Polling-Stations/badge.svg)](https://coveralls.io/github/DemocracyClub/UK-Polling-Stations) ![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)

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

sudo npm install -g npm
```

For other linux distributions, see [here](https://docs.djangoproject.com/en/1.11/ref/contrib/gis/install/geolibs/) for details on installing geospatial libraries for use with Django.

The API docs rely on [drafter](https://github.com/apiaryio/drafter/) for parsing API Blueprint. On OSX this can be installed using
```
brew install --HEAD https://raw.github.com/apiaryio/drafter/master/tools/homebrew/drafter.rb
```

On Ubuntu, this needs to be installed/compiled manually:
```
wget https://github.com/apiaryio/drafter/releases/download/v3.2.7/drafter-v3.2.7.tar.gz
tar xvzf drafter-v3.2.7.tar.gz
cd drafter-v3.2.7
./configure --shared
make libdrafter
sudo cp build/out/Release/lib.target/libdrafter.so /usr/lib/libdrafter.so
sudo cp src/drafter.h /usr/include/drafter/drafter.h
```

### Install python dependencies
```
pip install -r requirements/base.txt
```

### Install front-end dependencies
```
npm install
```

### Install testing system dependencies
We have a suite of end-to-end integration tests. We use [ChromeDriver](http://chromedriver.chromium.org/) to drive headless Chrome or Chromuim. This step isn't required to get a dev install running but will be required to run the full test suite.

On ubuntu, run

```
sudo apt-get install chromium-browser chromium-chromedriver
```

to install the dependencies. The chromedriver executable needs to be in `PATH`, so either add `/usr/lib/chromium-browser/chromedriver` to `PATH` or create a symlink e.g:

```
sudo ln -s /usr/lib/chromium-browser/chromedriver /usr/local/bin/chromedriver
```

On Mac OSX, run:
```
brew tap homebrew/cask
brew cask install chromedriver
```

and if you don't already have Chrome installed:
```
brew cask install google-chrome
```

### Install testing python dependencies
```
pip install -r requirements/testing.txt
```

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

### Run migrations
```
python manage.py migrate
```

### Import initial data

#### Import ONSPD

For development purposes, you can use the ONSPD for geocoding. Grab the latest release from http://geoportal.statistics.gov.uk/datasets?q=ONS%20Postcode%20Directory%20(ONSPD)&sort=-updatedAt unzip the data and import it using:

```
python manage.py import_onspd /path/to/data
```

#### Import Councils

```
python manage.py import_councils
```

#### Import some Polling District/Station data

For development purposes, you will need to seed your database with some data.
Most of our import scripts reference data is hosted privately, but there are
a number of councils who publish their data at a public location.

For example:

* `python manage.py import_camden`
* `python manage.py import_doncaster`
* `python manage.py import_lambeth`
* `python manage.py import_salford`
* `python manage.py import_southampton`
* `python manage.py import_st_albans`
* `python manage.py import_tunbridge_wells`
* `python manage.py import_wolverhampton`

all reference data which is publicly available.

## Importing the data we have from councils

Each council that has unimported data has a Github Issue with the [Data Import](https://github.com/DemocracyClub/UK-Polling-Stations/issues?q=is%3Aissue+is%3Aopen+label%3A%22Data+Import%22) label.

You can see the current status in [the Waffle Board](https://waffle.io/DemocracyClub/UK-Polling-Stations?label=Data%20Import).

We make a Django `manage.py` command in the data_collection app for each council which imports the raw data.
If you are interested in helping the project by writing an import script, see the issues tagged [recommended for beginners](https://github.com/DemocracyClub/UK-Polling-Stations/issues?q=is%3Aissue+is%3Aopen+label%3A%22recommended+for+beginners%22) for more info.
