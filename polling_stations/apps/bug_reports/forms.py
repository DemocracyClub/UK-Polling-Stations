from django import forms
from django.utils.translation import gettext_lazy as _

from .models import BugReport


class BugReportForm(forms.ModelForm):
    class Meta:
        model = BugReport
        fields = ["description", "email", "source_url", "source"]

    description = forms.CharField(
        label=_("Description"), widget=forms.Textarea(attrs={"rows": 3}), required=True
    )
    source_url = forms.CharField(widget=forms.HiddenInput(), required=False)
    source = forms.CharField(widget=forms.HiddenInput(), required=False)
