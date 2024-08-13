"""
Amazon S3 config:
By default, we will look for a section

[wheredoivote]
aws_access_key_id = xxxx
aws_secret_access_key = xxxx

in a /etc/boto.cfg or ~/.boto file, etc
See: http://boto.cloudhackers.com/en/latest/boto_config_tut.html

We can change the section name using the BOTO_SECTION setting
"""

import os

BOTO_SECTION = "wheredoivote"

if SERVER_ENVIRONMENT := os.environ.get("DC_ENVIRONMENT"):
    S3_DATA_BUCKET = f"pollingstations.elections.{SERVER_ENVIRONMENT}"
else:
    S3_DATA_BUCKET = os.environ.get(
        "S3_DATA_BUCKET", "pollingstations.elections.development"
    )
