from django.contrib.gis.db import models

from councils.models import Council


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
        Council, null=True, db_constraint=False, on_delete=models.DO_NOTHING,
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


class File(models.Model):
    upload = models.ForeignKey(Upload, on_delete=models.CASCADE)
    csv_valid = models.BooleanField()
    csv_rows = models.IntegerField(default=0)
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
