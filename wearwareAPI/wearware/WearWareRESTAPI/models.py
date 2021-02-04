from django.db import models

# Create your models here.

#CRUD API IMPLEMENTATION......
#Create / Insert / Add - POST
#Retrieve / Fetch - GET
#Update / Edit - PUT
#Delete / Remove - DELETE

class Participant(models.Model):
    participant_id = models.IntegerField() #pk
    subscriber_id = models.IntegerField()
    device_model = models.CharField()
    device_version = models.CharField()
    device_status = models.CharField()
    last_logged_activity = models.DateTimeField()
    email = models.EmailField()
    join_date = models.DateTimeField()
    gender = models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female')))

class ParticipantStudy(models.Model): 
    participant_id_pk = models.IntegerField() #pk fk
    study_id_pk = models.IntegerField() #pk fk
    participant_id = models.CharField()

class Study(models.Model): 
    study_id = models.IntegerField() #pk
    study_title = models.CharField()
    short_name = models.CharField()
    study_desc = models.CharField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    study_url = models.CharField()
    researcher_id = models.IntegerField()   

class Researcher_Study(models.Model): 
    researcher_id = models.IntegerField() #pk fk
    study_id = models.IntegerField() #pk fk

class Researcher(models.Model): 
    researcher_id = models.IntegerField() #pk
    name = models.CharField()
    email = models.EmailField()
    permissions = models.CharField()  

class Activity_Level(models.Model): 
    participant_id = models.IntegerField() #pk fk
    timestamp = models.DateTimeField() #pk
    activity_level = models.IntegerField()
    steps = models.IntegerField()
    METS = models.FloatField()
    calories = models.IntegerField()

class Heart_Rate(models.Model): 
    participant_id = models.IntegerField #pk fk
    timestamp = models.DateTimeField() #pk
    bpm = models.IntegerField()

class Sleep_Data(models.Model):
    participant_id = models.IntegerField() #pk fk
    timestamp = models.DateTimeField() #pk
    light_sleep = models.IntegerField()
    REM = models.IntegerField()
    restless = models.IntegerField()
    deep_sleep = models.IntegerField()
    wake = models.IntegerField()

    



