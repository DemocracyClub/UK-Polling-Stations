#!/usr/bin/env bash

function main(){

  # packages
  apt-get update -y
  apt-get install -y python-pip git libpq-dev build-essential python-dev binutils python-psycopg2
  apt-get install -y build-essential postgresql-9.3 postgresql-server-dev-9.3 libgeos-c1 libgdal-dev libproj-dev libjson0-dev libxml2-dev libxml2-utils xsltproc docbook-xsl docbook-mathml subversion autoconf

  # build Postgis from source 
  svn co http://svn.osgeo.org/postgis/trunk postgis
  cd postgis
  ./autogen.sh
  ./configure
  make
  sudo make install
  sudo ldconfig
  sudo make comments-install
  cd ..
  
  # Enable various commandline tools
  sudo ln -sf /usr/share/postgresql-common/pg_wrapper /usr/local/bin/shp2pgsql
  sudo ln -sf /usr/share/postgresql-common/pg_wrapper /usr/local/bin/pgsql2shp
  sudo ln -sf /usr/share/postgresql-common/pg_wrapper /usr/local/bin/raster2pgsql

  # Postgres setup
  sudo -u postgres createdb pollingstations 
  sudo -u postgres createuser dc -P -s 
  sudo -u postgres psql -c "CREATE USER dev WITH PASSWORD 'dev';"
  sudo -u postgres psql pollingstations -c "CREATE EXTENSION postgis;"
  echo "export DATABASE_URL=postgresql://dev:dev@localhost/pollingstations" >> /home/vagrant/.bashrc
}

main
