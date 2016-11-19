import os

# Google maps settings used by directions helper
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY', "")
BASE_GOOGLE_URL = "https://maps.googleapis.com/maps/api/directions/json?mode=walking&units=imperial&key={}&origin=".format(GOOGLE_API_KEY)
ORS_ROUTE_URL_TEMPLATE = "http://openls.geog.uni-heidelberg.de/route?start={},{}&end={},{}&via=&lang=en&distunit=MI&routepref=Pedestrian&weighting=Fastest&avoidAreas=&useTMC=false&noMotorways=false&noTollways=false&noUnpavedroads=false&noSteps=false&noFerries=false&instructions=false"
