from django import forms
from WearWareRESTAPI import models, query_utils
import csv
from django.http import StreamingHttpResponse

class QueryForm(forms.Form):
    RECORD_CHOICES=[
        ('participant', 'Participants'),
        ('hr','Heart Records'),
        ('sleep','Sleep Records'),
        ('activity', 'Activity Level Records'),
    ]

    record_type = forms.CharField(label='Record Type', widget=forms.Select(choices=RECORD_CHOICES))
    study_id = forms.IntegerField()
    nickname = forms.CharField(max_length=15, required=False)
    start_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)

    class Echo:
        #An object that implements just the write method of the file-like interface.

        def write(self, value):
            #Write the value by returning it, instead of storing in a buffer.
            return value

    def csv_response(request, results_list):
        #A view that streams a large CSV file.
        # Generate a sequence of rows. The range is based on the maximum number of
        # rows that can be handled by a single sheet in most spreadsheet applications.
        #rows = (["Row {}".format(idx), str(idx)] for idx in range(65536))
        pseudo_buffer = QueryForm.Echo()
        writer = csv.writer(pseudo_buffer)
        rows = (csv_writer.writerow(row) for row in results_list)

        response = StreamingHttpResponse(rows, content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="query_results.csv"'
        return response

    def query(self):

        db = query_utils.MyDBUtil()
        self.clean()

        record_type = self.data['record_type']
        study_id = self.data['study_id']
        nickname = self.data['nickname']
        start_date = self.data['start_date']
        end_date = self.data['end_date']

        if(record_type == 'participant'):
            results = query_utils.query_all_participants(db, study_id).all()
        else:
            results = query_utils.query_data(db, study_id, record_type, nickname, start_date, end_date).all()

        results_list = []
        for row in results:
            #output YYYY-MM-DD HH:MM:SS
            record = row.__dict__
            if record_type != 'participant':
                record['timestamp'] = record['timestamp'].strftime('%Y-%m-%d, %H:%M:%S')
            results_list.append(record)
            self.csv_response(results_list)
        return results_list

    def clean(self):
        cleaned_data = super(QueryForm, self).clean()
        study_id = cleaned_data.get('study_id')
        nickname = cleaned_data.get('nickname')
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        return cleaned_data

        if not study_id and not participant_id and not start_date:
            raise forms.ValidationError('No such exists')

class ParticipantInviteForm(forms.Form):
    participant_email = forms.CharField(max_length=100)
    participant_study = forms.CharField(max_length=100)
