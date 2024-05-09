import os

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
