import os

from django.conf import settings

MAPIT_URL = os.environ.get('MAPIT_URL', "http://mapit.democracyclub.org.uk/")
MAPIT_UA = os.environ.get('MAPIT_UA', None)

GOV_UK_LA_URL = "https://www.registertovote.service.gov.uk/register-to-vote/local-authority/"

COUNCIL_TYPES = [
    "LBO",
    "DIS",
    "MTD",
    "LGD",
    "UTA",
]
GOOGLE_API_KEY = getattr(settings, 'GOOGLE_API_KEY', '')

BASE_GOOGLE_URL = "https://maps.googleapis.com/maps/api/directions/json?mode=walking&units=imperial&key={}&origin=".format(GOOGLE_API_KEY)
ORS_ROUTE_URL_TEMPLATE = "http://openls.geog.uni-heidelberg.de/route?start={},{}&end={},{}&via=&lang=en&distunit=MI&routepref=Pedestrian&weighting=Fastest&avoidAreas=&useTMC=false&noMotorways=false&noTollways=false&noUnpavedroads=false&noSteps=false&noFerries=false&instructions=false"
