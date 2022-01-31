from django.contrib.gis.db import models

from councils.models import Council
from data_importers.import_script import ImportScript

status_map = {
    "Pending": "⌛",
    "Error": "❌",
    "OK": "✔️",
}


def status_to_emoji(status):
    if status in status_map:
        return status_map[status]
    return status


class Upload(models.Model):
    gss = models.ForeignKey(
        Council,
        null=True,
        db_constraint=False,
        on_delete=models.DO_NOTHING,
    )
    timestamp = models.DateTimeField()
    github_issue = models.CharField(blank=True, max_length=100)

    class Meta:
        get_latest_by = "timestamp"

    def __str__(self):
        return f"{self.timestamp}: {self.gss}"

    @property
    def status(self):
        if not self.file_set.all():
            return "Pending"
        for f in self.file_set.all():
            if not f.csv_valid:
                return "Error"
        return "OK"

    @property
    def status_emoji(self):
        return status_to_emoji(self.status)

    @property
    def import_script(self):
        if not self.status == "OK":
            return None

        elections = [str(self.election_date)]
        council_id = self.gss.council_id

        if len(self.file_set.all()) == 1:
            file = self.file_set.first()
            path = "/".join(file.key.split("/")[1:])
            import_script = ImportScript(
                **{
                    "council_id": council_id,
                    "ems": file.ems,
                    "addresses_name": path,
                    "stations_name": path,
                    "encoding": file.csv_encoding,
                    "elections": elections,
                }
            )

        elif len(self.file_set.all()) == 2:
            stations_file, addresses_file = sorted(
                self.file_set.all(), key=lambda f: f.csv_rows
            )
            import_script = ImportScript(
                **{
                    "council_id": council_id,
                    "ems": stations_file.ems,
                    "addresses_name": "/".join(addresses_file.key.split("/")[1:]),
                    "stations_name": "/".join(stations_file.key.split("/")[1:]),
                    "encoding": stations_file.csv_encoding,
                    "elections": elections,
                }
            )
        else:
            return None

        return import_script.script


class File(models.Model):
    upload = models.ForeignKey(Upload, on_delete=models.CASCADE)
    csv_valid = models.BooleanField()
    csv_rows = models.IntegerField(default=0)
    csv_encoding = models.CharField(max_length=20, blank=True)
    ems = models.CharField(max_length=40)
    key = models.CharField(max_length=255)
    errors = models.TextField(blank=True)

    def __str__(self):
        return self.key

    @property
    def filename(self):
        return self.key.split("/")[-1]

    @property
    def path(self):
        return "/".join(self.key.split("/")[:-1]) + "/"

    @property
    def status(self):
        if self.csv_valid:
            return "OK"
        return "Error"

    @property
    def status_emoji(self):
        return status_to_emoji(self.status)
