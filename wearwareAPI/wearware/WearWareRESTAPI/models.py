from django.db import models

# Create your models here.

#CRUD API IMPLEMENTATION......
#Create / Insert / Add - POST
#Retrieve / Fetch - GET
#Update / Edit - PUT
#Delete / Remove - DELETE

class ActivityLevel(models.Model):
    participant_id = models.OneToOneField('Participant', models.DO_NOTHING, primary_key=True)
    datetime = models.DateTimeField()
    activity_level = models.IntegerField(blank=True, null=True)
    steps = models.IntegerField(blank=True, null=True)
    mets = models.FloatField(blank=True, null=True)
    calories = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'activity_level'
        unique_together = (('participant_id', 'datetime'),)


class HeartRate(models.Model):
    participant_id = models.OneToOneField('participant', models.DO_NOTHING, primary_key=True)
    datetime = models.DateTimeField()
    bpm = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'heart_rate'
        unique_together = (('participant_id', 'datetime'), ('participant_id', 'datetime'),)


class Participant(models.Model):
    participant_id = models.IntegerField(primary_key=True)
    subscriber_id = models.IntegerField(blank=True, null=True)
    device_model = models.CharField(max_length=20, blank=True, null=True)
    device_version = models.CharField(max_length=20, blank=True, null=True)
    device_status = models.CharField(max_length=20, blank=True, null=True)
    last_logged_activity = models.DateTimeField(blank=True, null=True)
    email = models.CharField(max_length=20, blank=True, null=True)
    join_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'participant'


class ParticipantStudy(models.Model):
    participant_id = models.ForeignKey(Participant, models.DO_NOTHING)
    study_id = models.OneToOneField('Study', models.DO_NOTHING, primary_key=True)
    enrollment_id = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        db_table = 'participant_study'
        unique_together = (('study_id', 'participant_id'),)


class Researcher(models.Model):
    researcher_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=20, blank=True, null=True)
    permissions = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'researcher'


class ResearcherStudy(models.Model):
    researcher_id = models.OneToOneField(Researcher, models.DO_NOTHING, primary_key=True)
    study_id = models.ForeignKey('Study', models.DO_NOTHING)

    class Meta:
        db_table = 'researcher_study'
        unique_together = (('researcher_id', 'study_id'),)


class SleepData(models.Model):
    participant_id = models.OneToOneField(Participant, models.DO_NOTHING, primary_key=True)
    datetime = models.DateTimeField()
    light_sleep = models.IntegerField(blank=True, null=True)
    rem = models.IntegerField(blank=True, null=True)
    restless = models.IntegerField(blank=True, null=True)
    deep_sleep = models.IntegerField(blank=True, null=True)
    wake = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'sleep_data'
        unique_together = (('participant_id', 'datetime'),)

class Study(models.Model):
    study_id = models.IntegerField(primary_key=True)
    study_title = models.CharField(max_length=20, blank=True, null=True)
    short_name = models.CharField(max_length=20, blank=True, null=True)
    study_desc = models.CharField(max_length=20, blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    study_url = models.CharField(max_length=20, blank=True, null=True)
    researcher_id = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'study'