from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from WearWareRESTAPI.serializers import *
from WearWareRESTAPI.models import *
from django.shortcuts import render

def index(request):
    return render(request, "index.html")

class StudyAPIView(APIView):
    serializer_class = StudySerializer
    def get(self, request, id, format=None):
        try:
            item = Study.objects.filter(pk=id)
            serializer = StudySerializer(item,many=True)
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
    serializer_class = StudySerializer
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


class ParticipantAPIView(APIView):
    serializer_class = ParticipantSerializer

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
    serializer_class = ParticipantSerializer
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

class FitbitMinuteRecordAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = FitbitMinuteRecord.objects.filter(pk=id)
            serializer = MinuteRecordSerializer(item, many=True)
            return Response(serializer.data)
        except FitbitMinuteRecord.DoesNotExist:
            return Response(status=404)


    def delete(self, request, id, format=None):
        try:
            item = FitbitMinuteRecord.objects.get(pk=id)
        except FitbitMinuteRecord.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class FitbitMinuteRecordAPIListView(APIView):
    serializer_class = MinuteRecordSerializer
    def get(self, request, format=None):
        items = FitbitMinuteRecord.objects.order_by('pk')
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = MinuteRecordSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class FitbitHeartRecordAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = FitbitHeartRecord.objects.filter(pk=id)
            serializer = HeartRateRecordSerializer(item, many=True)
            return Response(serializer.data)
        except FitbitHeartRecord.DoesNotExist:
            return Response(status=404)

    def delete(self, request, id, format=None):
        try:
            item = FitbitHeartRecord.objects.get(pk=id)
        except FitbitHeartRecord.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class FitbitHeartRecordAPIListView(APIView):
    serializer_class = HeartRateRecordSerializer
    def get(self, request, format=None):
        items = FitbitHeartRecord.objects.order_by('pk')
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = HeartRateRecordSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class FitbitSleepRecordAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = FitbitSleepRecord.objects.filter(pk=id)
            serializer = FitbitSleepRecordSerializer(item)
            return Response(serializer.data)
        except FitbitSleepRecord.DoesNotExist:
            return Response(status=404)

    def delete(self, request, id, format=None):
        try:
            item = FitbitSleepRecord.objects.get(pk=id)
        except FitbitSleepRecord.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class FitbitSleepRecordAPIListView(APIView):
    serializer_class = SleepRecordSerializer
    def get(self, request, format=None):
        items = FitbitSleepRecord.objects.order_by('pk')
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = SleepRecordSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class SyncRecordAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = SyncRecord.objects.get(pk=id)
            serializer = SyncRecordSerializer(item)
            return Response(serializer.data)
        except SyncRecord.DoesNotExist:
            return Response(status=404)

    def delete(self, request, id, format=None):
        try:
            item = SyncRecord.objects.get(pk=id)
        except SyncRecord.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class SyncRecordAPIListView(APIView):
    serializer_class = SyncRecordSerializer
    def get(self, request, format=None):
        items = SyncRecord.objects.order_by('pk')
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = SyncRecordSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

class StudyHasParticipantAPIView(APIView):
    serializer_class = StudyHasParticipantSerializer

    def get(self, request, id, format=None):
        try:
            item = StudyHasParticipant.objects.get(pk=id)
            serializer = StudyHasParticipantSerializer(item)
            return Response(serializer.data)
        except StudyHasParticipant.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = StudyHasParticipant.objects.get(pk=id)
        except StudyHasParticipant.DoesNotExist:
            return Response(status=404)
        serializer = StudyHasParticipantSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = StudyHasParticipant.objects.get(pk=id)
        except StudyHasParticipant.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class StudyHasParticipantAPIListView(APIView):
    serializer_class = StudyHasParticipantSerializer
    def get(self, request, format=None):
        items = StudyHasParticipant.objects.order_by('pk')
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = StudyHasParticipantSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = StudyHasParticipantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ResearcherHasStudyAPIView(APIView):
    serializer_class = ResearcherHasStudySerializer

    def get(self, request, id, format=None):
        try:
            item = ResearcherHasStudy.objects.get(pk=id)
            serializer = ResearcherHasStudySerializer(item)
            return Response(serializer.data)
        except ResearcherHasStudy.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = ResearcherHasStudy.objects.get(pk=id)
        except ResearcherHasStudy.DoesNotExist:
            return Response(status=404)
        serializer = ResearcherHasStudySerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = ResearcherHasStudy.objects.get(pk=id)
        except ResearcherHasStudy.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class ResearcherHasStudyAPIListView(APIView):
    serializer_class = ResearcherHasStudySerializer

    def get(self, request, format=None):
        items = ResearcherHasStudy.objects.order_by('pk')
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = ResearcherHasStudySerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = ResearcherHasStudySerializer(data=request.data)
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
