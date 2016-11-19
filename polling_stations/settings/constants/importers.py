import os

# settings used by import scripts

# Morph API key used for downloading scraped data in import scripts
MORPH_API_KEY = os.environ.get('MORPH_API_KEY', "")

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
BOTO_SECTION = 'wheredoivote'
S3_DATA_BUCKET = 'pollingstations-data'
