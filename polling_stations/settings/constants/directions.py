import os

# Google maps settings used by directions helper
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY', "")
BASE_GOOGLE_URL = "https://maps.googleapis.com/maps/api/directions/json?mode=walking&units=imperial"
