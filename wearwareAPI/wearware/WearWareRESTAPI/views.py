from rest_framework.viewsets import ModelViewSet
from WearWareRESTAPI.serializers import ActivityLevelSerializer, HeartRateSerializer, ParticipantSerializer, ParticipantStudySerializer, ResearcherSerializer, ResearcherStudySerializer, SleepDataSerializer, StudySerializer
from WearWareRESTAPI.models import ActivityLevel, HeartRate, Participant, ParticipantStudy, Researcher, ResearcherStudy, SleepData, Study


class ActivityLevelViewSet(ModelViewSet):
    queryset = ActivityLevel.objects.order_by('pk')
    serializer_class = ActivityLevelSerializer


class HeartRateViewSet(ModelViewSet):
    queryset = HeartRate.objects.order_by('pk')
    serializer_class = HeartRateSerializer


class ParticipantViewSet(ModelViewSet):
    queryset = Participant.objects.order_by('pk')
    serializer_class = ParticipantSerializer


class ParticipantStudyViewSet(ModelViewSet):
    queryset = ParticipantStudy.objects.order_by('pk')
    serializer_class = ParticipantStudySerializer


class ResearcherViewSet(ModelViewSet):
    queryset = Researcher.objects.order_by('pk')
    serializer_class = ResearcherSerializer


class ResearcherStudyViewSet(ModelViewSet):
    queryset = ResearcherStudy.objects.order_by('pk')
    serializer_class = ResearcherStudySerializer


class SleepDataViewSet(ModelViewSet):
    queryset = SleepData.objects.order_by('pk')
    serializer_class = SleepDataSerializer


class StudyViewSet(ModelViewSet):
    queryset = Study.objects.order_by('pk')
    serializer_class = StudySerializer
