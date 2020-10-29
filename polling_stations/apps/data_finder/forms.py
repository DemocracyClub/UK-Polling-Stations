from django import forms

from localflavor.gb.forms import GBPostcodeField


class PostcodeLookupForm(forms.Form):
    postcode = GBPostcodeField(label="Enter your postcode")
    required_css_class = "required"
    error_css_class = "error"


class AddressSelectForm(forms.Form):
    address = forms.ChoiceField(
        choices=(),
        label="",
        initial="",
        widget=forms.Select(
            attrs={
                "class": "select_multirow",
                "size": 10,
                "aria-describedby": "address_picker",
            }
        ),
        required=True,
    )
    postcode = None

    def __init__(self, choices, postcode, *args, **kwargs):
        super(AddressSelectForm, self).__init__(*args, **kwargs)
        self.fields["address"].choices = choices
        self.postcode = postcode
