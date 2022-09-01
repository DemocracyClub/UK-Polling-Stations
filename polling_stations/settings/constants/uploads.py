import os

MAX_FILE_SIZE = 150000000  # 150Mb
S3_UPLOADS_BUCKET = "pollingstations-uploads-dev"
GITHUB_USERNAME = "polling-bot-4000"
GITHUB_EMAIL = "developers@democracyclub.org.uk"
GITHUB_REPO = "DemocracyClub/UK-Polling-Stations"
GITHUB_API_KEY = os.environ.get("GITHUB_API_KEY", "")
