from . import models
from rest_framework import viewsets
from . import models
from . import serializers

class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = models.Participant.objects.all()
    serializer_class = serializers.ParticipantSerializer

class ParticipantStudyViewSet(viewsets.ModelViewSet):
    queryset = models.ParticipantStudy.objects.all()
    serializer_class = serializers.ParticipantStudySerializer

class StudyViewSet(viewsets.ModelViewSet):
    queryset = models.Study.objects.all()
    serializer_class = serializers.StudySerializer

class ResearcherStudyViewSet(viewsets.ModelViewSet):
    queryset = models.Researcher_Study.objects.all()
    serializer_class = serializers.ResearcherStudySerializer

class ResearcherViewSet(viewsets.ModelViewSet):
    queryset = models.Researcher.objects.all()
    serializer_class = serializers.ResearcherSerializer

class ActivityLevelViewSet(viewsets.ModelViewSet):
    queryset = models.Activity_Level.objects.all()
    serializer_class = serializers.ActivityLevelSerializer

class HeartRateViewSet(viewsets.ModelViewSet):
    queryset = models.Heart_Rate.objects.all()
    serializer_class = serializers.HeartRateSerializer

class SleepDataViewSet(viewsets.ModelViewSet):
    queryset = models.Sleep_Data.objects.all()
    serializer_class = serializers.SleepDataSerializer