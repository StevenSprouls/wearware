from django import forms
from WearWareRESTAPI import models, query_utils

class QueryForm(forms.Form):
    study_id = forms.CharField(max_length=100)
    participant_id = forms.CharField(max_length=100, required=False)
    start_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)

    def query(self):

        db = query_utils.MyDBUtil()

        self.fields['study_id'] = query_utils.query_all_participants(db, study_id)

    def clean(self):
        cleaned_data = super(QueryForm, self).clean()
        study_id = cleaned_data.get('study_id')
        participant_id = cleaned_data.get('participant_id')
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        return cleaned_data

        if not study_id and not participant_id and not start_date:
            raise forms.ValidationError('No such exists')
#form for inviting a participant into a study (starts oauth2 process)       
class ParticipantInviteForm(forms.Form):
    participant_email = forms.CharField(max_length=100)
    participant_study = forms.CharField(max_length=100)
