import os
from pathlib import Path

EE_BASE = os.environ.get("EE_BASE", "https://elections.democracyclub.org.uk/")
"""
Every Election settings

Set CHECK to True to check Every Election to see if there is
an election happening before serving a poling station result

Set CHECK to False to return the value of HAS_ELECTION instead

This is mostly useful in development when we want
to see results even if there is no election happening
"""
EVERY_ELECTION = {"CHECK": True, "HAS_ELECTION": True}

ELECTION_BLACKLIST = [
    "local.epping-forest.moreton-and-fyfield.by.2018-05-03"  # uncontested
]

NEXT_CHARISMATIC_ELECTION_DATES = []

SHOW_GB_ID_MESSAGING = True

if data_path := os.environ.get("ELECTION_PARQUET_DATA_PATH", False):
    ELECTION_PARQUET_DATA_PATH = Path(data_path)
    USE_LOCAL_PARQUET_ELECTIONS = False
WCIVF_BALLOT_CACHE_URL = (
    "https://wcivf-ballot-cache.s3.eu-west-2.amazonaws.com/ballot_data/"
)

DEVS_DC_BASE = os.environ.get("DEVS_DC_BASE", "https://developers.democracyclub.org.uk")
