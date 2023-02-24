import multiprocessing
import os
import subprocess
import tempfile
import time
from pathlib import Path

import boto3
from django.core.management import BaseCommand
from django.db import connections, DEFAULT_DB_ALIAS
from django.conf import settings


APPROX_ADDRESS_BASE_BYTES = 3_300_000_000


def import_single_file(file_name, table_name, database):
    file_sql_template = f"""
        BEGIN;
        SET LOCAL synchronous_commit TO OFF;
        COPY {table_name} FROM STDIN CSV;
        COMMIT;
    """
    host = settings.DATABASES[database]["HOST"]
    password = settings.DATABASES[database]["PASSWORD"]
    database_name = settings.DATABASES[database]["NAME"]

    command = f"""cat {file_name} | psql postgresql://postgres:{password}@{host}/{database_name} -c "{file_sql_template}" """
    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
    )
    process.communicate()
    return True


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--database",
            default=DEFAULT_DB_ALIAS,
            help=f"Nominates a database to import in to. Defaults to the '{DEFAULT_DB_ALIAS}' database.",
        )
        parser.add_argument(
            "--processes",
            default=10,
            type=int,
            help="The number of jobs to run in parallel",
        )
        parser.add_argument(
            "--import-type",
            choices=["addressbase", "uprntocouncil"],
            required=True,
            help="The type of data to import",
        )
        parser.add_argument(
            "--local-file-path",
            action="store",
            help="If provided, use a local file rather than downloading",
        )

    def handle(self, *args, **options):
        self.database = options["database"]
        self.processes = options["processes"]
        self.import_type = options["import_type"]
        _tmp_dir = tempfile.TemporaryDirectory()
        self.tmp_dir = Path(_tmp_dir.name)
        self.local_file_path = Path(options["local_file_path"])
        if self.local_file_path:
            self.file_path = self.local_file_path
        self.s3_client = boto3.client(
            "s3", region_name=os.environ.get("AWS_REGION", "eu-west-2")
        )
        if self.import_type == "addressbase":
            self.table_name = "addressbase_address"
        else:
            self.table_name = "addressbase_uprntocouncil"

        if not self.local_file_path:
            # Download the file to the tempdir
            self.download_file()
        # Split the file and save the parts in a list
        self.split_files = self.split_file()

        # Pass that list to the import function
        with connections[self.database].cursor() as cursor:
            self.cursor = cursor
            self.cursor.execute(
                f"ALTER TABLE {self.table_name} SET (autovacuum_enabled = false);"
            )
            self.stdout.write("clearing existing data..")
            cursor.execute(f"TRUNCATE TABLE {self.table_name} CASCADE;")
            self.run_processes()
            self.cursor.execute(
                f"ALTER TABLE {self.table_name} SET (autovacuum_enabled = true);"
            )

        _tmp_dir.cleanup()

    def download_file(self):
        """
        Find the latest file of the file type and download it to the temp_dir

        """
        files = self.s3_client.list_objects_v2(
            Bucket=settings.PRIVATE_DATA_BUCKET_NAME, Prefix=f"{self.import_type}/"
        )["Contents"]

        latest_file_key = sorted(files, key=lambda f: f["LastModified"])[0]["Key"]
        print(latest_file_key)
        file = Path(self.tmp_dir.name) / self.import_type / "full.csv"
        file.parent.mkdir(exist_ok=True, parents=True)
        self.file_path = file
        with file.open("wb") as f:
            self.s3_client.download_fileobj(
                settings.PRIVATE_DATA_BUCKET_NAME, latest_file_key, f
            )

    def run_processes(self):
        pool = multiprocessing.Pool(self.processes)
        results = []
        for file_name in self.split_files:
            result = pool.apply_async(
                import_single_file, (file_name, self.table_name, self.database)
            )
            results.append(result)
        pool.close()
        while True:
            time.sleep(1)
            # catch exception if results are not ready yet
            self.cursor.execute(
                f"select SUM(bytes_processed) / {APPROX_ADDRESS_BASE_BYTES} from pg_stat_progress_copy;"
            )
            self.stdout.write(f"Rough % done: {self.cursor.fetchone()}")
            ready = [result.ready() for result in results]
            successful = [result.successful() for result in results if result.ready()]
            self.stdout.write(f"{ready=}")
            self.stdout.write(f"{successful=}")

            # exit loop if all tasks returned success
            if len(successful) == self.processes and all(successful):
                break
            # raise exception reporting exceptions received from workers
            if len(successful) == self.processes:
                raise Exception(
                    f"Workers raised following exceptions {[result._value for result in results if not result.successful()]}"
                )

    def split_file(self):
        self.split_dir = self.tmp_dir / "split"
        self.split_dir.mkdir(parents=True, exist_ok=True)
        self.stdout.write(
            f"Splitting {self.file_path} in to {self.processes} parts, saving to {self.split_dir}"
        )
        args = [
            "split",
            "-n",
            f"l/{self.processes}",
            "--additional-suffix=.csv",
            f"{self.local_file_path}",
            f"{self.split_dir}/{self.import_type}_split_",
        ]
        command = subprocess.Popen(args)
        command.communicate()
        return list(self.split_dir.glob("*"))
