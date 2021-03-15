import uuid
import random
import string
from django.contrib.auth.models import User
from django.contrib.auth import admin
from django.db import models
from datetime import timedelta
from django.utils.timezone import now
import django_filters
from django_filters import rest_framework as filters



class Study(models.Model):
    #a study owns subjects
    name = models.CharField(max_length=150, default='')
    creation_time = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()
    comment = models.CharField(max_length=2000, default='', blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        permissions = (
            ('view_study_data', 'View and export study data.'),
            ('add_subject_to_study', 'Create a new subject and add to study.'),
        )


class Participant(models.Model):
    #subject in a study, owns a fitbit account
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, db_index=True, unique=True)
    sex = models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female')))
    gender = models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female'), ('O', 'Other')))
    pairing_token = models.UUIDField(default=uuid.uuid4, editable=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.email

class FitbitAccount(models.Model):
    #fitbit acc owned by subject
    identifier = models.CharField(max_length=10, db_index=True)
    subject = models.ForeignKey(Participant, db_index=True, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)
    timezone = models.CharField(max_length=50)
    token_type = models.CharField(max_length=20, blank=True)
    refresh_token = models.CharField(max_length=100, blank=True)
    access_token = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.subject.first_name + '\'s fitbit'

class FitbitMinuteRecord(models.Model):
    #a single minute record owned by a fitbit account
    device = models.ForeignKey(FitbitAccount, db_index=True, on_delete=models.PROTECT)
    timestamp = models.DateTimeField(db_index=True)
    steps = models.IntegerField(db_index=True, null=True, blank=True)
    calories = models.FloatField(null=True, blank=True)
    mets = models.FloatField(null=True, blank=True)
    activity_level = models.IntegerField(null=True, blank=True)
    distance = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.device.subject.email + ' fitbit @ ' + str(self.timestamp)

class FitbitHeartRecord(models.Model):
    #a single heart rate record owned by a minute record...owned by the minute record rather than the participant as this is where the timestamp is located
    device = models.ForeignKey(FitbitMinuteRecord, db_index=True, on_delete=models.PROTECT)
    second = models.IntegerField()
    bpm = models.IntegerField()

class FitbitSleepRecord(models.Model):
    #a single sleep record related to a fitbit account
    device = models.ForeignKey(FitbitAccount, db_index=True, on_delete=models.PROTECT)
    timestamp = models.DateField()
    record_number = models.IntegerField()
    deep_sleep_minutes = models.IntegerField(null=True, blank=True)
    light_sleep_minutes = models.IntegerField(null=True, blank=True)
    rem_sleep_minutes = models.IntegerField(null=True, blank=True)
    awake_minutes = models.IntegerField(null=True, blank=True)
    total_sleep_minutes = models.IntegerField(null=True, blank=True)
    time_in_bed = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('timestamp', 'record_number')

class SyncRecord(models.Model):
    #A metadata record for a given sync interval.
    device = models.ForeignKey(FitbitAccount, on_delete=models.PROTECT)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    sync_type = models.CharField(max_length=100, db_index=True)
    successful = models.BooleanField(default=True)
    message = models.CharField(max_length=10000, default='')

class StudyHasParticipant(models.Model):
    class Meta:
        unique_together = (('study', 'participant'),)

    study = models.ForeignKey(Study, on_delete=models.PROTECT)
    participant = models.ForeignKey(Participant, on_delete=models.PROTECT)
    active = models.BooleanField(default=True)
    data_collection_start_date = models.DateField(verbose_name='earliest date for data sync')

class ResearcherHasStudy(models.Model):

    class Meta:
        unique_together = (('researcher', 'study'),)

    researcher = models.ForeignKey(User, on_delete=models.PROTECT)
    study = models.ForeignKey(Study, on_delete=models.PROTECT)

    def __str__(self):
        return self.researcher.email

class ParticipantData(models.Model):
    objects = FitbitHeartRecord(), FitbitMinuteRecord(), FitbitSleepRecord()
    device = models.ManyToManyField(FitbitHeartRecord, related_name='+')
    steps = models.ManyToManyField(FitbitMinuteRecord, related_name='+')
    calories = models.ManyToManyField(FitbitMinuteRecord, related_name='+')
    mets = models.ManyToManyField(FitbitMinuteRecord, related_name='+')
    activity_level = models.ManyToManyField(FitbitMinuteRecord, related_name='+')
    distance = models.ManyToManyField(FitbitMinuteRecord, related_name='+')
    bpm = models.ManyToManyField(FitbitHeartRecord, related_name='+')
#for the researcher model, first a user needs to be created by typing "python manage.py shell" and
# then from django.contrib.auth.models import User
# then User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
# delete a user with User.objects.get(username="john").delete()
