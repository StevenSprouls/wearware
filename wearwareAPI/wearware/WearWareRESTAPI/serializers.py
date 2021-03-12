from rest_framework import serializers
from WearWareRESTAPI.models import *

class AccSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FitbitAccount
        fields = '__all__'

class StudySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Study
        fields = '__all__'

class StudyHasParticipantSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = StudyHasParticipant
        fields = '__all__'

class ResearcherHasStudySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ResearcherHasStudy
        fields = '__all__'
    

class ParticipantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Participant
        fields = '__all__'

class HeartRateRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = FitbitHeartRecord
        fields = '__all__'

class MinuteRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = FitbitMinuteRecord
        fields = '__all__'

class SleepRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = FitbitSleepRecord
        exclude = '__all__'

class SyncRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = SyncRecord
        exclude = '__all__'
