from django.db import models


class DataEventType(models.TextChoices):
    # Data imported
    IMPORT = "IMPORT", "Import script run"
    # Date torn down
    TEARDOWN = "TEARDOWN", "Council data torn down"
    # Data marked as public
    # Data marked as not public
    # Polling station unpublished
    # Polling station published
