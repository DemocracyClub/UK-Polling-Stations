from commitment import GitHubCredentials, GitHubClient
from django.conf import settings
from django.contrib.gis.db import models

from requests import HTTPError

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
    election_date = models.DateField(null=True)
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

    @property
    def branch_name(self):
        return f"import-{self.gss.short_name}-{self.election_date}".lower().replace(
            " ", "-"
        )

    @property
    def pr_title(self):
        title = f"Import script for {self.gss.short_name} ({self.election_date})"
        server_env = getattr(settings, "SERVER_ENVIRONMENT", None)
        if server_env == "prod":
            return title
        elif server_env == "test":
            return f"TEST/{title}"
        else:
            return f"LOCALTEST/{title}"

    @property
    def pr_body(self):
        message = f"PR triggered by upload at #{self.github_issue}"
        server_env = getattr(settings, "SERVER_ENVIRONMENT", None)
        if server_env == "prod":
            return message
        elif server_env == "test":
            return f"**NB triggered from staging instance**\n{message}"
        else:
            return f"**NB triggered from local machine**\n{message}"

    def make_pull_request(self):
        print("creating pull request")
        if getattr(settings, "RUNNING_TESTS", False):
            return

        creds = GitHubCredentials(
            repo=settings.GITHUB_REPO,
            name=settings.GITHUB_USERNAME,
            api_key=settings.GITHUB_API_KEY,
            email=settings.GITHUB_EMAIL,
        )
        client = GitHubClient(creds)
        try:
            client.create_branch(self.branch_name)
        except HTTPError as e:
            if e.response.json()["message"] == "Reference already exists":
                print("Branch already exists")
            else:
                raise e

        client.push_file(
            content=self.import_script,
            filename=self.gss.import_script_path,
            message=self.pr_title,
            branch=self.branch_name,
        )

        try:
            client.open_pull_request(
                head_branch=self.branch_name,
                title=self.pr_title,
                body=self.pr_body,
            )
        except HTTPError as e:
            if (
                e.response.json()["errors"][0]["message"]
                == f"A pull request already exists for DemocracyClub:{self.branch_name}."
            ):
                print("PR already exists.")
            else:
                raise e


class File(models.Model):
    upload = models.ForeignKey(Upload, on_delete=models.CASCADE)
    version = models.PositiveIntegerField(default=1)
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
