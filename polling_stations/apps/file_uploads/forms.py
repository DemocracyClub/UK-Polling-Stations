import re

from django import forms
from django.contrib.auth import get_user_model
from django.core import validators
from django.core.validators import EmailValidator
from django.forms import modelformset_factory
from django.utils.regex_helper import _lazy_re_compile

from .models import ElectoralDataReturn, PerformanceReport, PollingStationVoterIDReturn

User = get_user_model()


class CouncilEmailValidator(EmailValidator):
    domain_regex = _lazy_re_compile(
        r"^(electoralcommission\.org\.uk|democracyclub\.org\.uk|.*\.gov\.uk|publicagroup\.uk|\.llyw\.cymru)$",
        re.IGNORECASE,
    )
    message = "Please enter an email address for a UK council or VJB"


class CouncilEmailField(forms.EmailField):
    default_validators = [validators.validate_email, CouncilEmailValidator()]


class CouncilLoginForm(forms.Form):
    """
    Login form for a User.
    """

    email = CouncilEmailField(
        required=True,
        help_text="""Enter your council email address and we will send you a
        magic link to log in with. Please make sure you have access to the
        email address you enter.""",
    )

    def clean_email(self):
        """
        Normalize the entered email
        """
        email = self.cleaned_data["email"]
        return User.objects.normalize_email(email)


class CSVUploadForm(forms.Form):
    csv_file = forms.FileField()


class ElectoralDataReturnForm(forms.ModelForm):
    """
    Mirrors the Commission's post-election "electoral data" return. Cross-
    field validation (e.g. rejected ballots can't exceed ballot papers
    issued) lives on the model's clean() method, and is surfaced here as
    normal field errors because ModelForm validation calls it for us.
    """

    class Meta:
        model = ElectoralDataReturn
        exclude = ["election_return"]


class PollingStationVoterIDReturnForm(forms.ModelForm):
    """
    One polling station's close-of-poll VIDEF summary. `polling_station` is
    deliberately not an editable field here - it's pre-filled from data the
    council has already uploaded, and shown read-only in the template.
    """

    class Meta:
        model = PollingStationVoterIDReturn
        fields = [
            "meeter_greeter_employed",
            "vac_used",
            "aed_used",
            "privacy_requests",
            "not_issued_ballot_total",
            "not_issued_then_returned",
            "refused_ballot_total",
            "refused_then_returned",
        ]


PollingStationVoterIDReturnFormSet = modelformset_factory(
    PollingStationVoterIDReturn,
    form=PollingStationVoterIDReturnForm,
    extra=0,
)


class PerformanceReportForm(forms.ModelForm):
    """
    A council's report against the Commission's four published performance
    standard outcomes. See ElectionReturnOutcomeContextView/template for the
    figures from the other two returns that are surfaced alongside each
    outcome, rather than asked for again here.
    """

    class Meta:
        model = PerformanceReport
        fields = [
            "outcome_1_summary",
            "outcome_2_summary",
            "outcome_3_summary",
            "outcome_4_summary",
            "submitted",
        ]
        widgets = {
            "outcome_1_summary": forms.Textarea(attrs={"rows": 4}),
            "outcome_2_summary": forms.Textarea(attrs={"rows": 4}),
            "outcome_3_summary": forms.Textarea(attrs={"rows": 4}),
            "outcome_4_summary": forms.Textarea(attrs={"rows": 4}),
        }
