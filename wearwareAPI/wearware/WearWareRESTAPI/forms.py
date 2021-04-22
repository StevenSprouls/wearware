from django import forms
from WearWareRESTAPI import models, query_utils

class QueryForm(forms.Form):
    RECORD_CHOICES=[
        ('participant', 'Participants'),
        ('hr','Heart Records'),
        ('sleep','Sleep Records'),
        ('activity', 'Activity Level Records'),
    ]

    record_type = forms.CharField(label='Record Type', widget=forms.Select(choices=RECORD_CHOICES))
    study_id = forms.IntegerField()
    participant_id = forms.IntegerField(required=False)
    start_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)


    def query(self):

        db = query_utils.MyDBUtil()
        self.clean()

        record_type = self.data['record_type']
        study_id = self.data['study_id']
        participant_id = self.data['participant_id']
        start_date = self.data['start_date']
        end_date = self.data['end_date']

        if(record_type == 'participant'):
            results = query_utils.query_all_participants(db, study_id).all()
        else:
            results = query_utils.query_data(db, study_id, record_type, participant_id, start_date, end_date).all()

        results_list = []
        for row in results:
            #output YYYY-MM-DD HH:MM:SS
            record = row.__dict__
            record['timestamp'] = record.strftime('%Y-%m-%d %H:%M:%S') #this might break
            results_list.append(record)
        return results_list



    def clean(self):
        cleaned_data = super(QueryForm, self).clean()
        study_id = cleaned_data.get('study_id')
        participant_id = cleaned_data.get('participant_id')
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        return cleaned_data

        if not study_id and not participant_id and not start_date:
            raise forms.ValidationError('No such exists')
