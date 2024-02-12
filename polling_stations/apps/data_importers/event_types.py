from django.db import models


class DataEventType(models.TextChoices):
    # Data imported
    IMPORT = "IMPORT", "Import script run"
    # Data torn down
    TEARDOWN = "TEARDOWN", "Council data torn down"
    # Set polling station visibility
    SET_STATION_VISIBILITY = "SET_STATION_VISIBILITY", "Station visibility changed"
