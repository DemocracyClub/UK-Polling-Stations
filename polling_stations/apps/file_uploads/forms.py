import re

from django import forms
from django.contrib.auth import get_user_model
from django.core import validators
from django.core.validators import EmailValidator
from django.utils.regex_helper import _lazy_re_compile

User = get_user_model()

__all__ = ["LoginForm"]


class CouncilEmailValidator(EmailValidator):
    domain_regex = _lazy_re_compile(r".*\.gov\.uk$", re.IGNORECASE)
    message = "Please enter an email address for a UK council or VJB"


class CouncilEmailField(forms.EmailField):
    default_validators = [validators.validate_email, CouncilEmailValidator()]


class CouncilLoginForm(forms.Form):
    """
    Login form for a User.
    """

    email = CouncilEmailField(required=True)

    def clean_email(self):
        """
        Normalize the entered email
        """
        email = self.cleaned_data["email"]
        return User.objects.normalize_email(email)
