from rest_framework import serializers
from WearWareRESTAPI.models import *

class StudySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Study
        fields = '__all__'

class StudyHasParticipantSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = StudyHasParticipant
        fields = ['study', 'participant']

class ResearcherHasStudySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ResearcherHasStudy
        fields = '__all__'
    

class ParticipantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Participant
        fields = ['pk', 'email', 'sex', 'gender']

class HeartRateRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = FitbitHeartRecord
        fields = '__all__'

class MinuteRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = FitbitMinuteRecord
        fields = ['pk', 'timestamp', 'steps', 'calories', 'mets', 'activity_level', 'distance']

class SleepRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = FitbitSleepRecord
        exclude = ['device']

class SyncRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = SyncRecord
        exclude = ['device']
