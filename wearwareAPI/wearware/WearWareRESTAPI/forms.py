from django import forms
from WearWareRESTAPI import models, query_utils
import csv
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper

class QueryForm(forms.Form):
    RECORD_CHOICES=[
        ('participant', 'Participants'),
        ('hr','Heart Records'),
        ('sleep','Sleep Records'),
        ('activity', 'Activity Level Records'),
    ]

    record_type = forms.CharField(label='Record Type', widget=forms.Select(choices=RECORD_CHOICES))
    short_name= forms.CharField(max_length=15)
    nickname = forms.CharField(max_length=15, required=False)
    start_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)

    class Echo:
        #An object that implements just the write method of the file-like interface.

        def write(self, value):
            #Write the value by returning it, instead of storing in a buffer.
            return value

    def query(self):

        db = query_utils.MyDBUtil()
        #self.clean()

        record_type = self.data['record_type']
        short_name = self.data['short_name']
        nickname = self.data['nickname']
        start_date = self.data['start_date']
        end_date = self.data['end_date']

        if(record_type == 'participant'):
            results = query_utils.query_all_participants(db, short_name).all()
        else:
            results = query_utils.query_data(db, short_name, record_type, nickname, start_date, end_date).all()

        results_list = []

        for row in results:
            #output YYYY-MM-DD HH:MM:SS
            record = row.__dict__
            if record_type != 'participant':
                record['timestamp'] = record['timestamp'].strftime('%Y-%m-%d, %H:%M:%S')
            results_list.append(record)
        #self.csv_response(results_list)
        return results_list


    def clean(self):
        cleaned_data = self.cleaned_data
        short_name = cleaned_data.get('short_name')
        nickname = cleaned_data.get('nickname')
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        return cleaned_data

        if not short_name and not participant_id and not start_date:
            raise forms.ValidationError('No such exists')

class ParticipantInviteForm(forms.Form):
    participant_email = forms.CharField(max_length=100)
    participant_study = forms.CharField(max_length=100)

class DownloadForm(forms.Form):
    RECORD_CHOICES=[
        ('participant', 'Participants'),
        ('hr','Heart Records'),
        ('sleep','Sleep Records'),
        ('activity', 'Activity Level Records'),
    ]
    record_type = forms.CharField(widget=forms.HiddenInput())
    short_name= forms.CharField(widget=forms.HiddenInput())
    nickname = forms.CharField(widget=forms.HiddenInput(), required=False)
    start_date = forms.DateField(widget=forms.HiddenInput(), required=False)
    end_date = forms.DateField(widget=forms.HiddenInput(), required=False)

    def clean(self):
        cleaned_data = self.cleaned_data
        short_name = cleaned_data.get('short_name')
        nickname = cleaned_data.get('nickname')
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        return cleaned_data

        if not short_name and not participant_id and not start_date:
            raise forms.ValidationError('No such exists')
