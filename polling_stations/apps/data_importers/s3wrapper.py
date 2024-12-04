import glob
import os
import shutil
from pathlib import Path
from typing import Tuple
from urllib.parse import urlparse

import boto3
from botocore.client import Config
from django.conf import settings


def parse_s3_uri(uri: str) -> tuple[str, str]:
    """
    Parse an S3 URI into bucket_name and key.
    's3://bucket_name/key/to/my/object' ---> ('bucket_name', 'key/to/my/object')
    Doesn't check for existence of object or connect to AWS.
    """
    parsed = urlparse(uri)
    if parsed.scheme != "s3":
        raise ValueError(f"Invalid S3 URI scheme: {uri}. Must start with s3://")

    bucket = parsed.netloc
    # Remove leading slash from key
    key = parsed.path.lstrip("/")

    if not bucket or not key:
        raise ValueError(
            f"Invalid S3 URI format: {uri}. Must be s3://bucket_name/key/to/my/object"
        )

    return bucket, key


class S3Wrapper:
    def __init__(self, bucket_name=None, cache_dir=None):
        """
        Args:
            bucket_name: Optional bucket_name name. Defaults to settings.S3_DATA_BUCKET
            cache_dir: Optional base path for S3 URIs. Defaults to ./s3cache/
        """
        s3 = boto3.resource(
            "s3",
            region_name=os.environ.get("AWS_REGION", "eu-west-2"),
            config=Config(s3={"addressing_style": "path"}),
        )
        self.bucket_name = bucket_name or settings.S3_DATA_BUCKET
        self.bucket = s3.Bucket(self.bucket_name)

        # this is where our local data will live
        if not cache_dir:
            self.base_path = os.path.abspath(f"./s3cache/{self.bucket_name}")
        else:
            self.base_path = os.path.abspath(f"{cache_dir}/{self.bucket_name}")

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

    def download_file(self, key: str, force: bool = False) -> Tuple[str, bool]:
        """
        Returns local file path and bool for whether file was actually downloaded or not.
        """
        local_path = Path(self.base_path) / key
        if local_path.exists() and not force:
            return str(local_path.resolve()), False

        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        self.bucket.download_file(key, local_path)
        return str(local_path.resolve()), True
