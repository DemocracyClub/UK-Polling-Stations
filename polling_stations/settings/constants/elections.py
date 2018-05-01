EE_BASE = 'https://elections.democracyclub.org.uk/'

"""
Every Election settings

Set CHECK to True to check Every Election to see if there is
an election happening before serving a poling station result

Set CHECK to False to return the value of HAS_ELECTION instead

This is mostly useful in development when we want
to see results even if there is no election happening
"""
EVERY_ELECTION = {
    'CHECK': True,
    'HAS_ELECTION': True
}

ELECTION_BLACKLIST = [
    'local.epping-forest.moreton-and-fyfield.by.2018-05-03',  # uncontested

    'local.stockport.edgeley-and-cheadle-heath.2018-05-03',  # cancelled
    'local.cherwell.bicester-west.2018-05-03',  # cancelled
    'local.tamworth.glascote.2018-05-03',  # cancelled
    'local.brent.willesden-green.2018-05-03',  # cancelled
    'local.southwark.london-bridge-west-bermondsey.2018-05-03',  # cancelled
]
