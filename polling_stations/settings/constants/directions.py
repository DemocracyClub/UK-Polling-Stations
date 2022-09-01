import os

# Google maps settings used by directions helper
GOOGLE_API_KEYS = []
BASE_GOOGLE_URL = "https://maps.googleapis.com/maps/api/directions/json?units=imperial"

# Mapbox settings used by directions helper
MAPBOX_API_KEY = os.environ.get("MAPBOX_API_KEY", "")
BASE_MAPBOX_URL = "https://api.mapbox.com/directions/v5/mapbox"


MAPZEN_API_KEY = os.environ.get("MAPZEN_API_KEY", "")
BASE_MAPZEN_URL = "https://valhalla.mapzen.com/route"
