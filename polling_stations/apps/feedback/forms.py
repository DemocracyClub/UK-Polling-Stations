import uuid

from django import forms

from .models import Feedback, FOUND_USEFUL_CHOICES


class FeedbackForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.fields['token'].initial = uuid.uuid4().hex

    class Meta:
        model = Feedback
        fields = ['found_useful', 'comments', 'source_url']

    found_useful = forms.ChoiceField(
        choices=FOUND_USEFUL_CHOICES,
        widget=forms.RadioSelect(
            attrs={
                'data-toggle': "button",
                'required': 'true',
            }
        )
    )
    source_url = forms.CharField(widget=forms.HiddenInput())
    token = forms.CharField(widget=forms.HiddenInput())
    comments = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 10}),
        required=False
    )
