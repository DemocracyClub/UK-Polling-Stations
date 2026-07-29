import re

from django import forms
from django.contrib.auth import get_user_model
from django.core import validators
from django.core.validators import EmailValidator
from django.utils.regex_helper import _lazy_re_compile

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


class ElectionDateForm(forms.Form):
    election_date = forms.ChoiceField(
        choices=[],
        widget=forms.RadioSelect,
    )

    def __init__(self, *args, election_dates, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["election_date"].choices = [(date, date) for date in election_dates]


class ElectionForm(forms.Form):
    election_id = forms.ChoiceField(
        choices=[],
        widget=forms.RadioSelect,
    )

    def __init__(self, *args, elections, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["election_id"].choices = [(e["id"], e["name"]) for e in elections]
