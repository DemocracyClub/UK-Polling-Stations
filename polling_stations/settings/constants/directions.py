import os

# Mapbox settings used by directions helper
MAPBOX_API_KEY = os.environ.get("MAPBOX_API_KEY", "")
BASE_MAPBOX_URL = "https://api.mapbox.com/directions/v5/mapbox"
