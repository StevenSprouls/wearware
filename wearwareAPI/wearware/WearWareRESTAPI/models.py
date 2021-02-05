from django.db import models

# Create your models here.

#CRUD API IMPLEMENTATION......
#Create / Insert / Add - POST
#Retrieve / Fetch - GET
#Update / Edit - PUT
#Delete / Remove - DELETE

class Participant(models.Model):
    participant_id = models.IntegerField(primary_key=True) #pk
    subscriber_id = models.IntegerField()
    device_model = models.CharField(max_length=20)
    device_version = models.CharField(max_length=20)
    device_status = models.CharField(max_length=20)
    last_logged_activity = models.DateTimeField()
    email = models.EmailField()
    join_date = models.DateTimeField()
    gender = models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female'), ('O', 'Other')))
    sex = models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female')))

class ParticipantStudy(models.Model):
    participant_id_pk = models.IntegerField(primary_key=True) #pk fk
    study_id_pk = models.IntegerField() #pk fk
    participant_id = models.CharField(max_length=20)

class Study(models.Model):
    study_id = models.IntegerField(primary_key=True) #pk
    study_title = models.CharField(max_length=20)
    short_name = models.CharField(max_length=20)
    study_desc = models.CharField(max_length=20)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    study_url = models.CharField(max_length=20)
    researcher_id = models.IntegerField()

class Researcher_Study(models.Model):
    researcher_id = models.IntegerField() #pk fk
    study_id = models.IntegerField() #pk fk

class Researcher(models.Model):
    researcher_id = models.IntegerField(primary_key=True) #pk
    name = models.CharField(max_length=20)
    email = models.EmailField()
    permissions = models.CharField(max_length=20)

class Activity_Level(models.Model):
    participant_id = models.IntegerField() #pk fk
    timestamp = models.DateTimeField(primary_key=True) #pk
    activity_level = models.IntegerField()
    steps = models.IntegerField()
    METS = models.FloatField()
    calories = models.IntegerField()

class Heart_Rate(models.Model):
    participant_id = models.IntegerField #pk fk
    timestamp = models.DateTimeField(primary_key=True) #pk
    bpm = models.IntegerField()

class Sleep_Data(models.Model):
    participant_id = models.IntegerField() #pk fk
    timestamp = models.DateTimeField(primary_key=True) #pk
    light_sleep = models.IntegerField()
    REM = models.IntegerField()
    restless = models.IntegerField()
    deep_sleep = models.IntegerField()
    wake = models.IntegerField()
