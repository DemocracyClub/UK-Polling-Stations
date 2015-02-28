from django import forms

from localflavor.gb.forms import GBPostcodeField

class PostcodeLookupForm(forms.Form):
    postcode = GBPostcodeField(label="Enter your postcode")
