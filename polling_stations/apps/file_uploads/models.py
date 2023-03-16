from datetime import timedelta
from commitment import GitHubCredentials, GitHubClient
from django.conf import settings
from django.contrib.gis.db import models
from django.utils.timezone import now
from django.db import transaction
from django.core.mail import EmailMessage

from django.template.loader import render_to_string
from requests import HTTPError

from councils.models import Council
from data_importers.import_script import ImportScript
from django.contrib.auth.models import User

status_map = {
    "Pending": "⌛",
    "Waiting": "⌛ waiting for second file",
    "Error": "❌",
    "Error One File": "❌ only one file uploaded",
    "OK": "✔️",
}


def status_to_emoji(status):
    if status in status_map:
        return status_map[status]
    return status


class UploadQuerySet(models.QuerySet):
    def future(self):
        return self.filter(election_date__gte=now())

    def pending_upload_qs(self):
        from_time = now() - timedelta(minutes=20)
        qs = Upload.objects.filter(
            timestamp__lte=from_time, warning_about_pending_sent=False
        )
        return qs


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

    objects = UploadQuerySet.as_manager()
    warning_about_pending_sent = models.BooleanField(default=False)
    upload_user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    class Meta:
        get_latest_by = "timestamp"

    def __str__(self):
        return f"{self.timestamp}: {self.gss}"

    @property
    def status(self):
        if not self.file_set.all():
            return "Pending"
        for f in self.file_set.all():
            if ("Expected 2 files, found 1" in f.errors) and (
                self.timestamp + timedelta(seconds=180) > now()
            ):
                return "Waiting"
            elif ("Expected 2 files, found 1" in f.errors) and (
                self.timestamp + timedelta(seconds=180) < now()
            ):
                return "Error One File"

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
    def gh_issue_number(self):
        return self.github_issue.split("/")[-1]

    @property
    def pr_title(self):
        title = f"Import script for {self.gss.short_name} ({self.election_date}) (closes #{self.gh_issue_number})"
        server_env = getattr(settings, "SERVER_ENVIRONMENT", None)
        if server_env == "production":
            return title
        elif server_env in ["staging", "development", "test"]:
            return f"TEST/{title}"
        else:
            return f"LOCALTEST/{title}"

    @property
    def pr_body(self):
        message = f"PR triggered by upload at {self.github_issue}"
        server_env = getattr(settings, "SERVER_ENVIRONMENT", "unknown_env")
        if server_env == "production":
            return message
        elif server_env in ["staging", "development", "test"]:
            return f"**NB triggered from {server_env} instance**\n{message}"
        else:
            return f"**NB triggered from local machine**\n{message}"

    def send_confirmation_email(self):
        server_env = getattr(settings, "SERVER_ENVIRONMENT", "unknown_env")
        # If we're in production, and the user has been deleted, return early.
        # We don't want to send an email to a non-existent user and we already
        # have github issues to track successful uploads
        if server_env == "production" and self.upload_user is None:
            return
        # if we're in production, and the upload user exists, send them an email
        elif server_env == "production" and self.upload_user.email:
            to = self.upload_user.email
        # for all other environments, send the email to the default
        # from email with a subject line that makes it clear
        # we are not in production and testing is taking place
        else:
            to = settings.DEFAULT_FROM_EMAIL
        if server_env == "production":
            subject = f"Your file upload for {self.gss.short_name} ({self.election_date}) was successful"
        else:
            subject = f"**NB triggered from {server_env} instance** Your file upload for {self.gss.short_name} ({self.election_date}) was successful"

        email = EmailMessage(
            subject,
            render_to_string(
                template_name="file_uploads/email/upload_confirmation.txt"
            ),
            settings.DEFAULT_FROM_EMAIL,
            [to],
            reply_to=[settings.DEFAULT_FROM_EMAIL],
            headers={"Message-ID": subject},
        )
        email.send()

    @transaction.atomic
    def send_error_email(self):
        subject = "File upload failed"
        message = f"File upload failure: {self}. Please investigate further."
        email = EmailMessage(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.DEFAULT_FROM_EMAIL],
            reply_to=[settings.DEFAULT_FROM_EMAIL],
            headers={"Message-ID": subject},
        )

        email.send()
        self.warning_about_pending_sent = True
        self.save()

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
