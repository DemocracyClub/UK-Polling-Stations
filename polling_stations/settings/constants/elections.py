EE_BASE = "https://elections.democracyclub.org.uk/"

"""
Every Election settings

Set CHECK to True to check Every Election to see if there is
an election happening before serving a poling station result

Set CHECK to False to return the value of HAS_ELECTION instead

This is mostly useful in development when we want
to see results even if there is no election happening

THRESHOLD_DAYS allows us to ignore elections which are
more than N days in the future when determining has_election.
Set to None or zero to ignore
"""
EVERY_ELECTION = {"CHECK": True, "HAS_ELECTION": True, "THRESHOLD_DAYS": 90}

ELECTION_BLACKLIST = []
