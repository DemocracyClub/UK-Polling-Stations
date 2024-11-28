import os
from django.db import models


if SERVER_ENVIRONMENT := os.environ.get("DC_ENVIRONMENT"):
    S3_DATA_BUCKET = f"pollingstations.elections.{SERVER_ENVIRONMENT}"
else:
    S3_DATA_BUCKET = os.environ.get(
        "S3_DATA_BUCKET", "pollingstations.elections.development"
    )


class EONIImportScheme(models.TextChoices):
    NATIONAL = ("NATIONAL", "National (NI Assembly and Westminster Elections)")
    LOCAL = ("LOCAL", "Local (Council Elections)")


EONI_IMPORT_SCHEME = EONIImportScheme.NATIONAL
