#!/usr/bin/env bash
set -xeE

pg_dump -d every_election -t organisations_divisiongeography > /dev/null &
pg_dump -d every_election -t organisations_organisationgeography > /dev/null &
wait
