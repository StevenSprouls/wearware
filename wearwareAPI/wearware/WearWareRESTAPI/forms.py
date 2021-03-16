from bootstrap_datepicker_plus import DatePickerInput
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from .models import *
from datetime import timedelta
from itertools import chain
from django.utils import timezone

class StudyCreateForm(forms.ModelForm):
    skip_date_validation = forms.BooleanField(
        widget=forms.HiddenInput, required=False)

    class Meta:
        model = Study
        fields = ['name', 'start_date', 'end_date',
                  'comment', 'skip_date_validation']
        widgets = {
            'start_date': DatePickerInput(format='%m/%d/%Y'),
            'end_date': DatePickerInput(format='%m/%d/%Y'),
            'comment': forms.Textarea(),
            'active': forms.HiddenInput()
        }
    def is_valid(self):
        if(self.data['start_date'] <= self.data['end_date']):
            return True
        else:
            return False
    def clean(self):
        cleaned_data = super(StudyCreateForm, self).clean()

        if not self.data['skip_date_validation']:

            overlaps_start_date = Study.objects.filter(start_date__lte=cleaned_data['start_date'],
                                                       end_date__gte=cleaned_data['start_date'])

            overlaps_end_date = Study.objects.filter(start_date__lte=cleaned_data['end_date'],
                                                     end_date__gte=cleaned_data['end_date'])

            overlaps_contained = Study.objects.filter(start_date__gte=cleaned_data['start_date'],
                                                      start_date__lte=cleaned_data['end_date'],
                                                      end_date__gte=cleaned_data['start_date'],
                                                      end_date__lte=cleaned_data['end_date'])

            overlaps = []
            overlaps.extend(s.name for s in overlaps_start_date)
            overlaps.extend(s.name for s in overlaps_end_date)
            overlaps.extend(s.name for s in overlaps_contained)

            if len(overlaps) > 0:
                self.data = self.data.copy()
                self.data['skip_date_validation'] = True
                raise forms.ValidationError('This study overlaps with dates of existing studies: {} '
                                            'Click Confirm to acknowledge that these studies overlap.'.format(overlaps))

        return cleaned_data

class CreateParticipantForm(forms.ModelForm):
    active = forms.BooleanField(
        widget=forms.HiddenInput, initial=True, required=False)

    class Meta:
        model = Participant
        fields = ['first_name', 'last_name',
                  'sex', 'gender',
                  'email', 'active',
                  ]
        widgets = {
            'email': forms.EmailInput(),
        }

class AddParticipantToStudyForm(forms.ModelForm):
    participant = forms.ModelChoiceField(
        queryset=Participant.objects.none())

    def __init__(self, *args, **kwargs):
        researcher = kwargs.pop('researcher')

        research_participants = ResearcherHasParticipant.objects.values_list(
            'participant').filter(researcher=researcher)

        participants = [entry[0] for entry in research_participants]

        qs = Participant.objects.filter(pk__in=participants)

        super(AddParticipantToStudyForm, self).__init__(*args, **kwargs)
        self.fields['participant'].queryset = qs

    class Meta:
        model = StudyHasParticipant
        fields = ['study', 'participant', 'data_collection_start_date', 'active']
        widgets = {
            'study': forms.HiddenInput(),
            'active': forms.HiddenInput(),
            'data_collection_start_date': DatePickerInput(format='%m/%d/%Y')
        }

class AddResearcherToStudyForm(forms.ModelForm):

    class Meta:
        model = ResearcherHasStudy
        fields = ['researcher', 'study']
        widgets = {
            'researcher': forms.HiddenInput(),
            'study': forms.HiddenInput()
        }

class RemoveResearcherFromStudy(forms.Form):
    researcher = forms.ModelChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        study = kwargs.pop('study')
        user = kwargs.pop('user')

        super().__init__(*args, **kwargs)

        self.fields['researcher'].queryset = ResearcherHasStudy.objects.filter(study=study).exclude(researcher=user)    

class StudyDownloadDataForm(forms.Form):
    download = forms.BooleanField(widget=forms.HiddenInput())
    start_date = forms.CharField(required=True, widget=DatePickerInput(format='%Y-%m-%d'))
    end_date = forms.CharField(required=True, widget=DatePickerInput(format='%Y-%m-%d'))