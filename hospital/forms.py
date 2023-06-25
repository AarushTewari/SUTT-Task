from django import forms

class   PatientSearchForm(forms.Form):
    query = forms.CharField(label='Search')