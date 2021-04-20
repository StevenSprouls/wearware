from rest_framework import serializers
from WearWareRESTAPI.models import *

class AccSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    class Meta:
        model = FitbitAccount
        fields = '__all__'

class StudySerializer(serializers.ModelSerializer):
    start_date = serializers.SerializerMethodField()
    end_date = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    url = serializers.CharField(source='get_absolute_url', read_only=True)


    class Meta:
        model = Study
        fields = '__all__'

    def get_active(self,obj):
        return obj.active

    def get_start_date(self,obj):
        return obj.start_date

    def get_end_date(self,obj):
        return obj.end_date

    def get_name(self,obj):
        return obj.name

class StudyHasParticipantSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)

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
    url = serializers.CharField(source='get_absolute_url', read_only=True)

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
        fields = '__all__'

class SyncRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = SyncRecord
        fields = '__all__'
