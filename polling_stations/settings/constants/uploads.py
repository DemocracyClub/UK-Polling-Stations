import os

if SERVER_ENVIRONMENT := os.environ.get("DC_ENVIRONMENT"):
    S3_UPLOADS_BUCKET = f"pollingstations.uploads.{SERVER_ENVIRONMENT}"
else:
    S3_UPLOADS_BUCKET = "pollingstations.uploads.development"

MAX_FILE_SIZE = 150000000  # 150Mb
GITHUB_USERNAME = "polling-bot-4000"
GITHUB_EMAIL = "developers@democracyclub.org.uk"
GITHUB_REPO = "DemocracyClub/UK-Polling-Stations"
GITHUB_API_KEY = os.environ.get("GITHUB_API_KEY", "")

# update this constant with email domains
# (i.e. the bit after '@') and the corresponding
# three letter council_ids in a list as shown below:
CUSTOM_DOMAINS = {
    # "example.com": ["EXC"],
    # "example.org": ["EXO", "EXP"],
}
