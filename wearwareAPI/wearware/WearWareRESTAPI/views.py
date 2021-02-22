from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from WearWareRESTAPI.serializers import ActivityLevelSerializer, HeartRateSerializer, ParticipantSerializer, ParticipantStudySerializer, ResearcherSerializer, ResearcherStudySerializer, SleepDataSerializer, StudySerializer
from WearWareRESTAPI.models import ActivityLevel, HeartRate, Participant, ParticipantStudy, Researcher, ResearcherStudy, SleepData, Study
from django.shortcuts import render

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


class ActivityLevelAPIListView(APIView):

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


class HeartRateAPIListView(APIView):

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


class ParticipantAPIListView(APIView):

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


class ParticipantStudyAPIListView(APIView):

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


class ResearcherAPIListView(APIView):

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


class ResearcherStudyAPIListView(APIView):

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


class SleepDataAPIListView(APIView):

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


class StudyAPIListView(APIView):

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
