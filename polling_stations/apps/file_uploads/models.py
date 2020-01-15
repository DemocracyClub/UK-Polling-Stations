from django.contrib.gis.db import models

from councils.models import Council


class Upload(models.Model):
    gss = models.ForeignKey(
        Council, null=True, db_constraint=False, on_delete=models.DO_NOTHING,
    )
    timestamp = models.DateTimeField()
    github_issue = models.CharField(blank=True, max_length=100)

    def __str__(self):
        return f"{self.timestamp}: {self.gss}"


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
