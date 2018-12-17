import os

"""
Map tiles config:
-----------

Set a shell environment variable TILE_LAYER
to configure which tile layer is used by leaflet.

Supported values are:
'MapQuestSDK'
'OpenStreetMap' (default)
"""
TILE_LAYER = os.environ.get("TILE_LAYER", "OpenStreetMap")
"""
Set a shell environment variable MQ_KEY
to specify MapQuestSDK API key.
"""
MQ_KEY = os.environ.get("MQ_KEY", None)
