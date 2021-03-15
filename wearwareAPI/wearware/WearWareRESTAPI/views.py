from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from WearWareRESTAPI.serializers import ActivityLevelSerializer, HeartRateSerializer, ParticipantSerializer, ParticipantStudySerializer, ResearcherSerializer, ResearcherStudySerializer, SleepDataSerializer, StudySerializer
from WearWareRESTAPI.models import ActivityLevel, HeartRate, Participant, ParticipantStudy, Researcher, ResearcherStudy, SleepData, Study
from django.shortcuts import render
from rest_framework import generics
import django_filters
from django_filters import rest_framework as filters
from django_filters.views import FilterView

def index(request):
    return render(request, "index.html")

class ActivityLevelAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = ActivityLevel.objects.filter(pk=id)
            serializer = ActivityLevelSerializer(item, many=True)
            return Response(serializer.data)
        except ActivityLevel.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = ActivityLevel.objects.get(pk=id)
        except ActivityLevel.DoesNotExist:
            return Response(status=404)
        serializer = ActivityLevelSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = ActivityLevel.objects.get(pk=id)
        except ActivityLevel.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)

class StudyFilter(filters.FilterSet):
    #start_date = filters.DateFilter()
    class Meta:
        model = Study
        fields = ['name', 'active', 'start_date', 'end_date']


class StudyAPIListView(APIView):
    serializer_class = StudySerializer
    queryset = Study.objects.all()
    #Filter for Studies
    filter_backends = [filters.DjangoFilterBackend, filters.OrderingFilter]
    filter_class = StudyFilter

    #Return only studies from a user
    def get_queryset(self):
        user = self.request.user
        return Study.objects.filter()

    def get(self, request, format=None):
        items = ActivityLevel.objects.order_by('pk')
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = ActivityLevelSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = ActivityLevelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class HeartRateAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = HeartRate.objects.filter(pk=id)
            serializer = HeartRateSerializer(item, many=True)
            return Response(serializer.data)
        except HeartRate.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = HeartRate.objects.get(pk=id)
        except HeartRate.DoesNotExist:
            return Response(status=404)
        serializer = HeartRateSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = HeartRate.objects.get(pk=id)
        except HeartRate.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)

#Participant Filter
class ParticipantFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='iexact')
    class Meta:
        model = Participant
        fields = ['first_name', 'last_name', 'email', 'sex', 'active']

class ParticipantList(FilterView):
    model = Participant
    paginate_by = 20
    filterset_class = ParticipantFilter
    strict = False


class ParticipantAPIListView(APIView):
    serializer_class = ParticipantSerializer
    #Filter for Participants
    filter_backends = [filters.DjangoFilterBackend,]
    filter_class = ParticipantFilter
    queryset = Participant.objects.all()

    #Return only participants in a study from a user
    def get_queryset(self):
        user = self.request.user
        return Participant.objects.filter()

    def get(self, request, format=None):
        items = HeartRate.objects.order_by('pk')
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = HeartRateSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = HeartRateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ParticipantAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = Participant.objects.get(pk=id)
            serializer = ParticipantSerializer(item)
            return Response(serializer.data)
        except Participant.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = Participant.objects.get(pk=id)
        except Participant.DoesNotExist:
            return Response(status=404)
        serializer = ParticipantSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = Participant.objects.get(pk=id)
        except Participant.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)

class FitbitMinuteRecordFilter(filters.FilterSet):
    class Meta:
        model = FitbitMinuteRecord
        fields = ['device', 'steps', 'calories', 'mets', 'activity_level', 'distance']

class FitbitMinuteRecordAPIListView(APIView):
    serializer_class = MinuteRecordSerializer
    queryset = FitbitMinuteRecord.objects.all()
    #Filter for Minute Record
    filter_backends = [filters.DjangoFilterBackend, filters.OrderingFilter,]
    filter_class = FitbitMinuteRecordFilter
    ordering_fields = ['device', 'steps', 'calories', 'mets', 'activity_level', 'distance']

    #Return only data in a study from a user
    def get_queryset(self):
        user = self.request.user
        return FitbitMinuteRecord.objects.filter()

    def get(self, request, format=None):
        items = Participant.objects.order_by('pk')
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = ParticipantSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = ParticipantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ParticipantStudyAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = ParticipantStudy.objects.get(pk=id)
            serializer = ParticipantStudySerializer(item)
            return Response(serializer.data)
        except ParticipantStudy.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = ParticipantStudy.objects.get(pk=id)
        except ParticipantStudy.DoesNotExist:
            return Response(status=404)
        serializer = ParticipantStudySerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = ParticipantStudy.objects.get(pk=id)
        except ParticipantStudy.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)

class FitbitHeartRecordFilter(filters.FilterSet):
    class Meta:
        model = FitbitHeartRecord
        fields = ['device']


class FitbitHeartRecordAPIListView(APIView):
    serializer_class = HeartRateRecordSerializer
    queryset = FitbitHeartRecord.objects.all()
    #Filter for HeartRecord
    filter_backends = [filters.DjangoFilterBackend, filters.OrderingFilter,]
    filter_class = FitbitHeartRecordFilter
    ordering_fields = ['device', 'bpm']

    #Return only HR in a study from a user
    def get_queryset(self):
        user = self.request.user
        return FitbitHeartRecord.objects.filter()

    def get(self, request, format=None):
        items = ParticipantStudy.objects.order_by('pk')
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = ParticipantStudySerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = ParticipantStudySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ResearcherAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = Researcher.objects.get(pk=id)
            serializer = ResearcherSerializer(item)
            return Response(serializer.data)
        except Researcher.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = Researcher.objects.get(pk=id)
        except Researcher.DoesNotExist:
            return Response(status=404)
        serializer = ResearcherSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = Researcher.objects.get(pk=id)
        except Researcher.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)

class FitbitSleepRecordFilter(filters.FilterSet):
    class Meta:
        model = FitbitSleepRecord
        fields = ['device', 'record_number']


class FitbitSleepRecordAPIListView(APIView):
    serializer_class = SleepRecordSerializer
    queryset = FitbitSleepRecord.objects.all()
    #Filter for Sleep Record
    filter_backends = [filters.DjangoFilterBackend, filters.OrderingFilter,]
    filter_class = FitbitSleepRecordFilter
    ordering_fields = ['device', 'record_number']

    #Return only sleep record in a study from a user
    def get_queryset(self):
        user = self.request.user
        return FitbitHeartRecord.objects.filter()

    def get(self, request, format=None):
        items = Researcher.objects.order_by('pk')
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = ResearcherSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = ResearcherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ResearcherStudyAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = ResearcherStudy.objects.get(pk=id)
            serializer = ResearcherStudySerializer(item)
            return Response(serializer.data)
        except ResearcherStudy.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = ResearcherStudy.objects.get(pk=id)
        except ResearcherStudy.DoesNotExist:
            return Response(status=404)
        serializer = ResearcherStudySerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = ResearcherStudy.objects.get(pk=id)
        except ResearcherStudy.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)

class SyncRecordFilter(filters.FilterSet):
    class Meta:
        model = SyncRecord
        fields = ['device', 'timestamp', 'sync_type', 'successful']


class SyncRecordAPIListView(APIView):
    serializer_class = SyncRecordSerializer
    queryset = SyncRecord.objects.all()
    #Filter for Sleep Record
    filter_backends = [filters.DjangoFilterBackend, filters.OrderingFilter,]
    filter_class = SyncRecordFilter
    ordering_fields = ['device', 'timestamp', 'sync_type', 'successful']

    #Return only sync record in a study from a user
    def get_queryset(self):
        user = self.request.user
        return SyncRecord.objects.filter()

    def get(self, request, format=None):
        items = ResearcherStudy.objects.order_by('pk')
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = ResearcherStudySerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = ResearcherStudySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    #returns only studies by the authenticated researcher
    def get_queryset(self):
        user = self.request.user
        return ResearcherStudy.objects.filter(study_id, researcher_id)


class SleepDataAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = SleepData.objects.get(pk=id)
            serializer = SleepDataSerializer(item)
            return Response(serializer.data)
        except SleepData.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = SleepData.objects.get(pk=id)
        except SleepData.DoesNotExist:
            return Response(status=404)
        serializer = SleepDataSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = SleepData.objects.get(pk=id)
        except SleepData.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)

class StudyHasParticipantFilter(filters.FilterSet):
    class Meta:
        model = StudyHasParticipant
        fields = ['study', 'participant', 'active', 'data_collection_start_date']


class StudyHasParticipantAPIListView(APIView):
    serializer_class = StudyHasParticipantSerializer
    queryset = StudyHasParticipant.objects.all()
    #Filter for participants in study
    filter_backends = [filters.DjangoFilterBackend, filters.OrderingFilter,]
    filter_class = StudyHasParticipantFilter
    ordering_fields = ['study', 'participant', 'active', 'data_collection_start_date']

    #Return only Researcher study record in a study from a user
    def get_queryset(self):
        user = self.request.user
        return StudyHasParticipant.objects.filter()

    def get(self, request, format=None):
        items = SleepData.objects.order_by('pk')
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = SleepDataSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = SleepDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class StudyAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = Study.objects.filter(pk=id)
            serializer = StudySerializer(item, many=True)
            return Response(serializer.data)
        except Study.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = Study.objects.get(pk=id)
        except Study.DoesNotExist:
            return Response(status=404)
        serializer = StudySerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = Study.objects.get(pk=id)
        except Study.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)

class ResearcherHasStudyFilter(filters.FilterSet):
    class Meta:
        model = ResearcherHasStudy
        fields = ['researcher', 'study']


class ResearcherHasStudyAPIListView(APIView):
    serializer_class = ResearcherHasStudySerializer
    queryset = ResearcherHasStudy.objects.all()
    #Filter for Researcher Study
    filter_backends = [filters.DjangoFilterBackend, filters.OrderingFilter,]
    filter_class = ResearcherHasStudyFilter
    ordering_fields = ['researcher', 'study']

    #Return only Researcher study record in a study from a user
    def get_queryset(self):
        user = self.request.user
        return ResearcherHasStudy.objects.filter()

    def get(self, request, format=None):
        items = Study.objects.order_by('pk')
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = StudySerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = StudySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class FitbitAccountAPIView(APIView):
    serializer_class = AccSerializer
    def get(self, request, id, format=None):
        try:
            item = FitbitAccount.objects.get(pk=id)
            serializer = AccSerializer(item)
            return Response(serializer.data)
        except FitbitAccount.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = FitbitAccount.objects.get(pk=id)
        except FitbitAccount.DoesNotExist:
            return Response(status=404)
        serializer = AccSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = FitbitAccount.objects.get(pk=id)
        except FitbitAccount.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class FitbitAccountAPIListView(APIView):
    serializer_class = AccSerializer
    def get(self, request, format=None):
        items = FitbitAccount.objects.order_by('pk')
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = AccSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = AccSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

#Views for all of the participant data
class ParticipantDataAPIView(APIView):
    serializer_class = ParticipantDataSerializer

    def get(self, request, id, format=None):
        try:
            item = ParticipantData.objects.get(pk=id)
            serializer = ParticipantDataSerializer(item)
            return Response(serializer.data)
        except ParticipantData.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = ParticipantData.objects.get(pk=id)
        except ParticipantData.DoesNotExist:
            return Response(status=404)
        serializer = ParticipantDataSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = ParticipantData.objects.get(pk=id)
        except ParticipantData.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)

#Filter class for participant data
class ParticipantDataFilter(filters.FilterSet):
    class Meta:
        model = ParticipantData
        fields = ['device', 'steps', 'calories', 'mets',
                  'activity_level', 'distance', 'bpm' ]

class ParticipantDataAPIListView(generics.ListCreateAPIView):
        serializer_class = ParticipantDataSerializer
        queryset = ParticipantData.objects.all()
        #Filter for participant
        filter_backends = [filters.DjangoFilterBackend,]
        filter_class = ParticipantDataFilter

        def get(self, request, format=None):
            item = Participant.objects.get(first_name=first_name)
            device = FitbitAccount.objects.get(subject=item)

            minute_records = FitbitMinuteRecord.objects.filter(device=device, timestamp__gte=start_date, timestamp__lte=end_date)
            heart_records = FitbitHeartRecord.objects.filter(minute_record__in=minute_records)
            sleep_records = FitbitSleepRecord.objects.filter(device=device, timestamp__gte=start_date, timestamp__lte=end_date)
            data = {
                'minute_records': minute_records,
                'heart_records': heart_records,
                'sleep_records': sleep_records,
            }
            #serializer = ParticipantDataSerializer(data)
            items = StudyHasParticipant.objects.order_by('pk')
            paginator = PageNumberPagination()
            result_page = paginator.paginate_queryset(items, request)
            serializer = ParticipantDataSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)

        def post(self, request, format=None):
            serializer = ParticipantDataSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)

        #Return only Researcher study record in a study from a user
        def get_queryset(self):
            user = self.request.user
            return ParticipantData.objects.filter()
