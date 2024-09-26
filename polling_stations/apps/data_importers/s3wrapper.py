import glob
import os
import shutil

import boto3
from botocore.client import Config
from django.conf import settings


class S3Wrapper:
    def __init__(self):
        s3 = boto3.resource(
            "s3",
            region_name=os.environ.get("AWS_REGION", "eu-west-2"),
            config=Config(s3={"addressing_style": "path"}),
        )
        self.bucket = s3.Bucket(settings.S3_DATA_BUCKET)

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
        keys = self.bucket.objects.filter(Prefix=prefix)
        count = 0
        for key in keys:
            # ignore directories
            if key.key[-8:] == "$folder$" or key.key[-1] == "/":
                continue

            local_file = os.path.join(self.base_path, key.key)
            os.makedirs(os.path.dirname(local_file), exist_ok=True)
            self.bucket.download_file(key.key, local_file)
            # We have to manually build a count of the number of items:
            # A s3.Bucket.objectsCollection does not have a len() because it is
            # a generator expression, not a list
            count = count + 1

        if count == 0:
            raise ValueError("Couldn't find any data to import")

    def fetch_data_by_council(self, council_id):
        prefix = "%s" % (council_id)
        self.fetch_data(prefix)
