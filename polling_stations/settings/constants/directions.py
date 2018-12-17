import os

# Google maps settings used by directions helper
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")
BASE_GOOGLE_URL = "https://maps.googleapis.com/maps/api/directions/json?units=imperial"

MAPZEN_API_KEY = os.environ.get("MAPZEN_API_KEY", "")
BASE_MAPZEN_URL = "https://valhalla.mapzen.com/route"
