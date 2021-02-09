from rest_framework.serializers import ModelSerializer
from WearWareRESTAPI.models import ActivityLevel, HeartRate, Participant, ParticipantStudy, Researcher, ResearcherStudy, SleepData, Study


class ActivityLevelSerializer(ModelSerializer):

    class Meta:
        model = ActivityLevel
        depth = 2
        fields = '__all__'


class HeartRateSerializer(ModelSerializer):

    class Meta:
        model = HeartRate
        depth = 2
        fields = '__all__'


class ParticipantSerializer(ModelSerializer):

    class Meta:
        model = Participant
        depth = 2
        fields = '__all__'


class ParticipantStudySerializer(ModelSerializer):

    class Meta:
        model = ParticipantStudy
        depth = 2
        fields = '__all__'


class ResearcherSerializer(ModelSerializer):

    class Meta:
        model = Researcher
        depth = 2
        fields = '__all__'


class ResearcherStudySerializer(ModelSerializer):

    class Meta:
        model = ResearcherStudy
        depth = 2
        fields = '__all__'


class SleepDataSerializer(ModelSerializer):

    class Meta:
        model = SleepData
        depth = 2
        fields = '__all__'


class StudySerializer(ModelSerializer):

    class Meta:
        model = Study
        depth = 2
        fields = '__all__'
