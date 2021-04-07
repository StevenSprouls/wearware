from django import forms
from WearWareRESTAPI import models, queries

class QueryForm(forms.Form):
    study_id = forms.CharField(max_length=100)
    participant_id = forms.CharField(max_length=100)
    start_date = forms.DateField()
    end_date = forms.DateField()

    field1 = forms.CharField(max_length=255)
    field2 = forms.CharField(max_length=255)

    def __init__(self,*args,**kwargs):
        super(QueryForm,self).__init__(*args,**kwargs)

        self.fields['field1'].initial = queries.query_all_participants('study_id')
        self.fields['field2'].initial = queries.query_data('study_id','participant_id', 'start_date', 'end_date')
