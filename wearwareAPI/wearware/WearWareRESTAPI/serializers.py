from rest_framework import serializers
from WearWareRESTAPI.models import *

class AccSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FitbitAccount
        fields = '__all__'

class StudySerializer(serializers.ModelSerializer):
    active = serializers.SerializerMethodField()
    start_date = serializers.SerializerMethodField()
    end_date = serializers.SerializerMethodField()

    class Meta:
        model = Study
        fields = '__all__'

    def get_active(self,obj):
        return obj.active

    def get_start_date(self,obj):
        return obj.start_date

    def get_end_date(self,obj):
        return obj.end_date

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

#Serializer for all of the participant data so it can more easily be sorted
class ParticipantDataSerializer(serializers.ModelSerializer):
    minute_records = MinuteRecordSerializer( many = True, read_only = True )
    heart_records = HeartRateRecordSerializer( many = True, read_only = True )
    sleep_records = SleepRecordSerializer( many = True, read_only = True )

    class Meta:
        model = ParticipantData
        fields = ['minute_records', 'heart_records', 'sleep_records']

