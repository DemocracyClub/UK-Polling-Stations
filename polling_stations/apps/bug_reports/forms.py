from django import forms
from .models import BugReport


class BugReportForm(forms.ModelForm):
    class Meta:
        model = BugReport
        fields = ["description", "email", "source_url", "source"]

    description = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 3}), required=True
    )
    source_url = forms.CharField(widget=forms.HiddenInput(), required=False)
    source = forms.CharField(widget=forms.HiddenInput(), required=False)
    required_css_class = "required"
    error_css_class = "error"
