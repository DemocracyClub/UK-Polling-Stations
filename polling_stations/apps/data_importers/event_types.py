from django.db import models


class DataEventType(models.TextChoices):
    # Data imported
    IMPORT = "IMPORT", "Import script run"
    # Data torn down
    TEARDOWN = "TEARDOWN", "Council data torn down"
    # Set polling station visibility
    SET_STATION_VISIBILITY = "SET_STATION_VISIBILITY", "Station visibility changed"

    @classmethod
    def station_update_event_types(cls):
        return (cls.SET_STATION_VISIBILITY,)


class EventUserType(models.TextChoices):
    ADMIN = "ADMIN", "Admin Panel User"
    COUNCIL = "COUNCIL", "Council User"


class StationCorrectionSource(models.TextChoices):
    COUNCIL = "COUNCIL", "Report from council"
    DEMOCRACY_CLUB = "DEMOCRACY_CLUB", "Report from Democracy Club"
    PUBLIC = "PUBLIC", "Report from public"
