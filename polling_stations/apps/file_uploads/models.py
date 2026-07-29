import time
from datetime import timedelta

from commitment import GitHubClient, GitHubCredentials
from data_importers.import_script import ImportScript
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.contrib.postgres.aggregates import BoolAnd, StringAgg
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.db.models import Case, Exists, Func, OuterRef, Q, Value, When
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.timezone import now
from pollingstations.models import PollingStation, VisibilityChoices
from requests import HTTPError
from sentry_sdk import capture_message

status_map = {
    "Pending": "⌛",
    "Waiting": "⌛ waiting for second file",
    "Error": "❌",
    "Error One File": "❌ only one file uploaded",
    "OK": "✔️",
}


class UploadStatusChoices(models.TextChoices):
    OK = "OK", "✔️"
    ERROR = "ERROR", "❌"
    PENDING = "PENDING", "⌛"
    WAITING_SECOND_FILE = "WAITING", "⌛ waiting for second file"
    ERROR_ONE_FILE = (
        "ERROR_ONE_FILE",
        "❌ only one file uploaded",
    )


def status_to_emoji(status):
    if status in status_map:
        return status_map[status]
    return status


class UploadQuerySet(models.QuerySet):
    def future(self):
        return self.filter(election_date__gte=now())

    def pending_upload_qs(self):
        from_time = now() - timedelta(minutes=20)
        return self.filter(timestamp__lte=from_time, warning_about_pending_sent=False)

    def with_status(self):
        file_subquery = File.objects.filter(upload_id=OuterRef("pk"))
        file_errors_subquery = (
            File.objects.filter(upload_id=OuterRef("pk"))
            .values("upload_id")
            .annotate(errors_agg=StringAgg("errors", delimiter=",", distinct=True))
            .values("errors_agg")
        )
        files_valid_subquery = (
            File.objects.filter(upload_id=OuterRef("pk"))
            .annotate(all_valid=Func("csv_valid", function="BOOL_AND"))
            .values("all_valid")
        )
        return self.annotate(
            file_errors=file_errors_subquery, all_files_valid=files_valid_subquery
        ).annotate(
            status=Case(
                When(all_files_valid=True, then=Value(UploadStatusChoices.OK)),
                When(~Exists(file_subquery), then=Value(UploadStatusChoices.PENDING)),
                When(
                    Q(file_errors__contains="Expected 2 files, found 1")
                    & Q(timestamp__gte=timezone.now() - timedelta(seconds=180)),
                    then=Value(UploadStatusChoices.WAITING_SECOND_FILE),
                ),
                When(
                    Q(file_errors__contains="Expected 2 files, found 1")
                    & Q(timestamp__lt=timezone.now() - timedelta(seconds=180)),
                    then=Value(UploadStatusChoices.ERROR_ONE_FILE),
                ),
                When(all_files_valid=False, then=Value(UploadStatusChoices.ERROR)),
            )
        )


class Upload(models.Model):
    gss = models.ForeignKey(
        "councils.Council",
        null=True,
        db_constraint=False,
        on_delete=models.DO_NOTHING,
    )
    timestamp = models.DateTimeField()
    election_date = models.DateField(null=True)
    github_issue = models.CharField(blank=True, max_length=100)
    warning_about_pending_sent = models.BooleanField(default=False)
    upload_user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    objects = UploadQuerySet.as_manager()

    class Meta:
        get_latest_by = "timestamp"

    def __str__(self):
        return f"{self.timestamp}: {self.gss}"

    @property
    def fileset_valid(self):
        if self.file_set.exists():
            return (
                self.file_set.all()
                .aggregate(fileset_valid=BoolAnd("csv_valid"))
                .get("fileset_valid")
            )
        return False

    @property
    def import_script(self):
        if not self.fileset_valid:
            raise Exception("One or more uploaded files is not valid")

        elections = [str(self.election_date)]
        council_id = self.gss.council_id

        num_files = len(self.file_set.all())
        if num_files == 1:
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

        elif num_files == 2:
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
            raise Exception(f"expected 1 or 2 files, found {num_files}")

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
        if server_env in ["staging", "development", "test"]:
            return f"TEST/{title}"
        return f"LOCALTEST/{title}"

    @property
    def pr_body(self):
        message = f"PR triggered by upload at {self.github_issue}"
        server_env = getattr(settings, "SERVER_ENVIRONMENT", "unknown_env")
        if server_env == "production":
            return message
        if server_env in ["staging", "development", "test"]:
            return f"**NB triggered from {server_env} instance**\n{message}"
        f"**NB triggered from local machine**\n{message}"
        return None

    def send_confirmation_email(self):
        server_env = getattr(settings, "SERVER_ENVIRONMENT", "unknown_env")
        # If we're in production, and the user has been deleted, return early.
        # We don't want to send an email to a non-existent user and we already
        # have github issues to track successful uploads
        if server_env == "production" and self.upload_user is None:
            return
        # if we're in production, and the upload user exists, send them an email
        if server_env == "production" and self.upload_user.email:
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
                capture_message(
                    f"Branch {self.branch_name} already exists", level="warning"
                )
            else:
                raise e

        try:
            client.push_file(
                content=self.import_script,
                filename=self.gss.import_script_path,
                message=self.pr_title,
                branch=self.branch_name,
            )
        except HTTPError as e:
            status_code = e.response.status_code
            if status_code == 409:
                time.sleep(10)
                client.push_file(
                    content=self.import_script,
                    filename=self.gss.import_script_path,
                    message=self.pr_title,
                    branch=self.branch_name,
                )
            else:
                raise e

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
                capture_message(f"PR already exists for {self.branch_name}:\n{e}")
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


ELECTION_TYPES_REQUIRING_PERFORMANCE_REPORT = ("parl", "local")


class ElectionReturn(models.Model):
    """
    The parent record for a council's post-election reporting for a single
    (council, election) combination.

    This groups together the same broad categories of information that
    electoral services teams already report to the Electoral Commission
    after a poll (the "electoral data" return, the Voter ID evaluation data,
    and - for the larger scheduled polls - a performance report), so that a
    council can submit it once, here, alongside their polling station data.
    """

    council = models.ForeignKey(
        "councils.Council",
        db_constraint=False,
        on_delete=models.CASCADE,
    )
    # The EveryElection ballot id, e.g. "local.some-ward.2026-05-07"
    election_id = models.CharField(max_length=255)
    election_title = models.CharField(blank=True, max_length=255)
    poll_open_date = models.DateField()
    # The EveryElection `requires_voter_id` stub (e.g. "EA-2022"), or blank
    # if this ballot doesn't require voter ID.
    requires_voter_id = models.CharField(blank=True, max_length=100)
    submitted_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("council", "election_id")

    def __str__(self):
        return f"{self.council}: {self.election_title or self.election_id}"

    @property
    def election_type(self):
        """
        The EveryElection election_id "family" prefix, e.g. "local", "parl",
        "mayor", "pcc", "senedd", "sp", "gla", "nia".
        """
        return self.election_id.split(".")[0] if self.election_id else ""

    @property
    def requires_performance_report(self):
        """
        The Commission decides which elections need a performance report by
        periodic direction under s.71 Electoral Administration Act 2006, so
        this is a best-effort default (the two recurring, legislatively
        named cases: UK Parliamentary general elections and local government
        elections in England/Wales) rather than a definitive list - it can
        be overridden per election if the Commission directs otherwise.
        """
        return self.election_type in ELECTION_TYPES_REQUIRING_PERFORMANCE_REPORT

    @property
    def known_polling_stations(self):
        """
        The polling stations already known for this council from uploaded
        data, so we don't have to ask again how many stations were used.
        """
        return self.council.pollingstation_set.filter(
            visibility=VisibilityChoices.PUBLISHED
        )

    @property
    def known_polling_station_count(self):
        return self.known_polling_stations.count()


class ElectoralDataReturn(models.Model):
    """
    Mirrors the Commission's post-election "electoral data" return: the
    turnout, postal voting and rejected ballot statistics that the
    Commission requests from Returning Officers/ EROs after each set of
    scheduled elections, via its online data portal (see EA Bulletins).
    """

    election_return = models.OneToOneField(
        ElectionReturn, related_name="electoral_data", on_delete=models.CASCADE
    )

    electorate = models.PositiveIntegerField(
        help_text="Total number of registered electors."
    )
    postal_electorate = models.PositiveIntegerField(
        null=True, blank=True, help_text="Number of electors registered to vote by post."
    )

    postal_votes_issued = models.PositiveIntegerField(null=True, blank=True)
    postal_votes_returned = models.PositiveIntegerField(null=True, blank=True)
    postal_votes_rejected_no_signature = models.PositiveIntegerField(default=0)
    postal_votes_rejected_no_dob = models.PositiveIntegerField(default=0)
    postal_votes_rejected_signature_mismatch = models.PositiveIntegerField(default=0)
    postal_votes_rejected_dob_mismatch = models.PositiveIntegerField(default=0)
    postal_votes_rejected_late = models.PositiveIntegerField(
        default=0, help_text="Received after close of poll."
    )

    ballot_papers_issued = models.PositiveIntegerField(
        null=True, blank=True, help_text="Total number of ballot papers issued (turnout)."
    )
    # The four statutory rejection categories (Representation of the People
    # Act 1983, sch.1 r.46/47 and equivalents).
    rejected_ballots_no_official_mark = models.PositiveIntegerField(default=0)
    rejected_ballots_voted_for_too_many = models.PositiveIntegerField(default=0)
    rejected_ballots_identifying_mark = models.PositiveIntegerField(default=0)
    rejected_ballots_unmarked_or_void = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Electoral data return"

    def __str__(self):
        return f"Electoral data return: {self.election_return}"

    @property
    def postal_votes_rejected_total(self):
        return (
            self.postal_votes_rejected_no_signature
            + self.postal_votes_rejected_no_dob
            + self.postal_votes_rejected_signature_mismatch
            + self.postal_votes_rejected_dob_mismatch
            + self.postal_votes_rejected_late
        )

    @property
    def rejected_ballots_total(self):
        return (
            self.rejected_ballots_no_official_mark
            + self.rejected_ballots_voted_for_too_many
            + self.rejected_ballots_identifying_mark
            + self.rejected_ballots_unmarked_or_void
        )

    @property
    def turnout_percentage(self):
        if not self.electorate or self.ballot_papers_issued is None:
            return None
        return round(self.ballot_papers_issued / self.electorate * 100, 2)

    def clean(self):
        errors = {}

        if self.postal_electorate is not None and self.postal_electorate > self.electorate:
            errors["postal_electorate"] = (
                "Postal electorate can't be more than the total electorate."
            )

        if (
            self.postal_votes_issued is not None
            and self.postal_electorate is not None
            and self.postal_votes_issued > self.postal_electorate
        ):
            errors["postal_votes_issued"] = (
                "Postal votes issued can't be more than the postal electorate."
            )

        if (
            self.postal_votes_returned is not None
            and self.postal_votes_issued is not None
            and self.postal_votes_returned > self.postal_votes_issued
        ):
            errors["postal_votes_returned"] = (
                "Postal votes returned can't be more than postal votes issued."
            )

        if (
            self.postal_votes_returned is not None
            and self.postal_votes_rejected_total > self.postal_votes_returned
        ):
            errors["postal_votes_rejected_no_signature"] = (
                "Rejected postal votes (all reasons combined) can't be more "
                "than postal votes returned."
            )

        if self.ballot_papers_issued is not None:
            if self.ballot_papers_issued > self.electorate:
                errors["ballot_papers_issued"] = (
                    "Ballot papers issued can't be more than the electorate."
                )
            elif self.rejected_ballots_total > self.ballot_papers_issued:
                errors["rejected_ballots_no_official_mark"] = (
                    "Rejected ballot papers (all reasons combined) can't be "
                    "more than ballot papers issued."
                )

        if errors:
            raise ValidationError(errors)


class PollingStationVoterIDReturn(models.Model):
    """
    One row per polling station, mirroring the close-of-poll summary
    figures on the Commission's Voter Identification Evaluation Form
    (VIDEF), which are themselves collated from the Ballot Paper Refusal
    List (BPRL) and the VIDEF notes sheet used throughout polling day.

    Where we can match it to a polling station this council has already
    uploaded, `polling_station` is pre-filled - there's no need to ask the
    council to re-key the station number/address.
    """

    election_return = models.ForeignKey(
        ElectionReturn, related_name="voter_id_returns", on_delete=models.CASCADE
    )
    polling_station = models.ForeignKey(
        PollingStation, null=True, blank=True, on_delete=models.SET_NULL
    )
    # Fallback for a station we don't already have a record for.
    polling_station_label = models.CharField(blank=True, max_length=255)

    meeter_greeter_employed = models.BooleanField(
        null=True,
        blank=True,
        help_text="Was a meeter/greeter employed for most of the day?",
    )

    # Section 1: electoral identity documents
    vac_used = models.PositiveIntegerField(
        default=0, verbose_name="1a. Voter Authority Certificates used"
    )
    aed_used = models.PositiveIntegerField(
        default=0, verbose_name="1b. Anonymous Elector's Documents used"
    )
    # Section 2: privacy
    privacy_requests = models.PositiveIntegerField(
        default=0, verbose_name="2. Voters who asked to show ID in private"
    )
    # Section 3: unable to issue a ballot paper (no/unaccepted ID)
    not_issued_ballot_total = models.PositiveIntegerField(
        default=0, verbose_name="3a. Not issued with a ballot paper"
    )
    not_issued_then_returned = models.PositiveIntegerField(
        default=0, verbose_name="3b. ...who later returned with accepted ID"
    )
    # Section 4: refusals recorded on the BPRL
    refused_ballot_total = models.PositiveIntegerField(
        default=0, verbose_name="4a. Refused a ballot paper (from the BPRL)"
    )
    refused_then_returned = models.PositiveIntegerField(
        default=0, verbose_name="4b. ...who later returned and were issued one"
    )

    class Meta:
        verbose_name = "Polling station Voter ID return (VIDEF)"
        unique_together = ("election_return", "polling_station")

    def __str__(self):
        return f"VIDEF: {self.polling_station or self.polling_station_label} ({self.election_return})"

    def clean(self):
        errors = {}
        if self.not_issued_then_returned > self.not_issued_ballot_total:
            errors["not_issued_then_returned"] = (
                "Can't be more than the total not issued with a ballot paper (3a)."
            )
        if self.refused_then_returned > self.refused_ballot_total:
            errors["refused_then_returned"] = (
                "Can't be more than the total refused a ballot paper (4a)."
            )
        if errors:
            raise ValidationError(errors)


class PerformanceReport(models.Model):
    """
    A council's report against the Commission's four published performance
    standard outcomes for Returning Officers, required (at the Commission's
    direction under s.71 Electoral Administration Act 2006) for the larger
    scheduled polls.

    The Commission's own "information needed to understand the impact"
    lists for these outcomes overlap heavily with the electoral data and
    VIDEF returns above (e.g. "ballot paper rejection rates and postal vote
    rejection rates", "records of those refused a ballot paper, by reason"),
    so those figures are surfaced alongside each outcome rather than
    re-requested here.
    """

    election_return = models.OneToOneField(
        ElectionReturn, related_name="performance_report", on_delete=models.CASCADE
    )
    outcome_1_summary = models.TextField(
        blank=True,
        verbose_name="Outcome 1",
        help_text="Electoral services are robust and support the delivery of well-run elections.",
    )
    outcome_2_summary = models.TextField(
        blank=True,
        verbose_name="Outcome 2",
        help_text="Everybody who is eligible and wants to vote is able to do so and has confidence in the voting process.",
    )
    outcome_3_summary = models.TextField(
        blank=True,
        verbose_name="Outcome 3",
        help_text="Everybody who is eligible and wants to stand for election is able to do so and has confidence in the process.",
    )
    outcome_4_summary = models.TextField(
        blank=True,
        verbose_name="Outcome 4",
        help_text="Everyone can have confidence that the election process is well managed and in the accuracy of the results.",
    )
    submitted = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Performance report"

    def __str__(self):
        return f"Performance report: {self.election_return}"
