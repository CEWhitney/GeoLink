from django import forms
from django.forms import NumberInput


class PageForm(forms.Form):
    new_page = forms.CharField(label='Page', max_length=4,
                                widget=NumberInput(attrs={'autocomplete': 'off', 'width': '50px', 'min': '0', 'max': '9999'}))

class SearchForm(forms.Form):
    search = forms.CharField(label='Search', max_length=100)