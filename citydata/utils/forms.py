from django import forms
from django.forms import NumberInput, TextInput


class PageForm(forms.Form):
    new_page = forms.CharField(label='Page', max_length=4, required=False,
                                widget=NumberInput(attrs={'autocomplete': 'off', 'width': '50px', 'min': '1', 'max': '9999', 'placeholder': '1'}))

    search_query = forms.CharField(label='Search', max_length=100, required=False,
                                    widget=TextInput(attrs={'autocomplete': 'off', 'width': '50px', 'placeholder': 'City or Country'}))

class InitForm(forms.Form):
    air_num = forms.CharField(label='Air City Connections', max_length=2, required=False,
                                widget=NumberInput(attrs={'autocomplete': 'off', 'width': '50px', 'min': '1', 'max': '10', 'placeholder': '3'}))
    
    land_num = forms.CharField(label='Land City Connections', max_length=2, required=False,
                                widget=NumberInput(attrs={'autocomplete': 'off', 'width': '50px', 'min': '1', 'max': '10', 'placeholder': '2'}))

    land_range = forms.CharField(label='Land City Range', max_length=3, required=False,
                                widget=NumberInput(attrs={'autocomplete': 'off', 'width': '50px', 'min': '1', 'max': '999', 'placeholder': '75'}))
