import uuid

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import FOUND_USEFUL_CHOICES, VOTE_CHOICES, Feedback, NoElectionFeedback


class FeedbackForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.fields["token"].initial = uuid.uuid4().hex

    class Meta:
        model = Feedback
        fields = ["found_useful", "vote", "comments", "source_url"]

    found_useful = forms.ChoiceField(
        label=_("Did you find this useful?"),
        choices=FOUND_USEFUL_CHOICES,
        widget=forms.RadioSelect(attrs={"data-toggle": "button", "required": "true"}),
    )
    vote = forms.ChoiceField(
        choices=VOTE_CHOICES,
        widget=forms.RadioSelect(attrs={"data-toggle": "button"}),
    )
    source_url = forms.CharField(widget=forms.HiddenInput())
    token = forms.CharField(widget=forms.HiddenInput())
    comments = forms.CharField(
        label=_("Comments"),
        widget=forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
        required=False,
    )


class NoElectionFeedbackForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NoElectionFeedbackForm, self).__init__(*args, **kwargs)
        self.fields["token"].initial = uuid.uuid4().hex

    class Meta:
        model = NoElectionFeedback
        fields = ["no_election_feedback_text", "source_url"]

    no_election_feedback_text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 4,
                "cols": 40,
            }
        ),
        required=True,
    )
    source_url = forms.CharField(widget=forms.HiddenInput())
    token = forms.CharField(widget=forms.HiddenInput())
