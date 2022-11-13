from django import forms
from django.forms import NumberInput
from django.forms import TextInput


class PageForm(forms.Form):
    new_page = forms.CharField(label='Page', max_length=4, required=False,
                                widget=NumberInput(attrs={'autocomplete': 'off', 'width': '50px', 'min': '1', 'max': '9999', 'placeholder': '1'}))

    search_query = forms.CharField(label='Search', max_length=100, required=False,
                                    widget=TextInput(attrs={'autocomplete': 'off', 'width': '50px', 'placeholder': 'City or Country'}))
