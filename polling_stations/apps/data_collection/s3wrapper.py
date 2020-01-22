import glob
import os
import shutil
from boto.pyami.config import Config
from boto.s3.connection import S3Connection
from django.conf import settings


class S3Wrapper:
    def __init__(self):
        config = Config()
        access_key = config.get_value(settings.BOTO_SECTION, "aws_access_key_id")
        secret_key = config.get_value(settings.BOTO_SECTION, "aws_secret_access_key")

        # connect to S3 + get ref to our data bucket
        conn = S3Connection(access_key, secret_key)
        self.bucket = conn.get_bucket(settings.S3_DATA_BUCKET)

        # this is where our local data will live
        self.base_path = os.path.abspath("./s3cache/")

    @property
    def data_path(self):
        return os.path.abspath(self.base_path)

    def fetch_data(self, prefix):
        local_pattern = os.path.abspath("%s/%s*" % (self.base_path, prefix))
        local_paths = glob.glob(local_pattern)

        if len(local_paths) == 1:
            # if local dir already exists, delete it to
            # remove any existing (potentially stale) data
            shutil.rmtree(local_paths[0])
        elif len(local_paths) > 1:
            raise ValueError(
                "Pattern '%s' matched more than one directory" % local_pattern
            )
        else:
            # if local dir does not exist, no worries. We will create
            # any necessary directories when we pull data down from s3
            pass

        # fetch data for this prefix
        keys = self.bucket.list(prefix=prefix)
        count = 0
        for key in keys:

            # ignore directories
            if key.key[-8:] == "$folder$" or key.key[-1] == "/":
                continue

            local_file = os.path.join(self.base_path, key.key)
            os.makedirs(os.path.dirname(local_file), exist_ok=True)
            key.get_contents_to_filename(local_file)
            # We have to manually build a count of the number of items:
            # A BucketListResultSet does not have a len() because it is
            # a generator expression, not a list
            count = count + 1

        if count == 0:
            raise ValueError("Couldn't find any data to import")

    def fetch_data_by_council(self, council_id):
        prefix = "%s" % (council_id)
        self.fetch_data(prefix)
