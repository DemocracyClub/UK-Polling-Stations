import os

if SERVER_ENVIRONMENT := os.environ.get("DC_ENVIRONMENT"):
    S3_DATA_BUCKET = f"pollingstations.elections.{SERVER_ENVIRONMENT}"
else:
    S3_DATA_BUCKET = os.environ.get(
        "S3_DATA_BUCKET", "pollingstations.elections.development"
    )
