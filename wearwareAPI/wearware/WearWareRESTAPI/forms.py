from django import forms

class QueryForm(forms.Form):
    participant = forms.CharField(label='Participant', max_length=100)
