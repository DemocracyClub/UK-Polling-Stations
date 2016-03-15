from django import forms

from localflavor.gb.forms import GBPostcodeField


class PostcodeLookupForm(forms.Form):
    postcode = GBPostcodeField(label="Enter your postcode")

class AddressSelectForm(forms.Form):
    address = forms.ChoiceField(
        choices=(),
        label="",
        initial="",
        widget=forms.Select(attrs={
            'class': 'select_multirow',
            'size': 10,
            'aria-describedby': "address_picker",
        }),
        required=True
    )

    def __init__(self, choices, *args, **kwargs):
        super(AddressSelectForm, self).__init__(*args, **kwargs)
        self.fields['address'].choices = choices
