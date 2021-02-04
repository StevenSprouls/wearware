# API <--> APPLICATION....json format

from rest_framework import serializers
from .models import *

class ParticipantSerializer(serializers.ModelSerializer):
    model = Participant
    fields = '__all__'

class ParticipantStudySerializer(serializers.ModelSerializer):
    model = ParticipantStudy
    fields = '__all__'

class StudySerializer(serializers.ModelSerializer):
    model = Study
    fields = '__all__'

class ResearcherStudySerializer(serializers.ModelSerializer):
    model = Researcher_Study
    fields = '__all__'

class ResearcherSerializer(serializers.ModelSerializer):
    model = Researcher
    fields = '__all__'

class ActivityLevelSerializer(serializers.ModelSerializer):
    model = Activity_Level
    fields = '__all__'

class HeartRateSerializer(serializers.ModelSerializer):
    model = Heart_Rate
    fields = '__all__'

class SleepDataSerializer(serializers.ModelSerializer):
    model = Sleep_Data
    fields = '__all__'