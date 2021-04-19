from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from WearWareRESTAPI.serializers import *
from WearWareRESTAPI.models import *
from django.shortcuts import render
from rest_framework import generics
import django_filters
from django_filters import rest_framework as filters
from django_filters.views import FilterView
import time
from rest_framework.renderers import AdminRenderer, TemplateHTMLRenderer, JSONRenderer
from django.contrib.admin.views.main import PAGE_VAR
from django.http import HttpResponseRedirect
from .forms import QueryForm
from .forms import ParticipantInviteForm
from requests_oauthlib import OAuth2Session
from sqlalchemy import create_engine, insert
import os
import json

#Fitbit Client secret, authentication URLs, Database URI
CLIENT_ID = '22C4KD'
CLIENT_SECRET = 'd25cd8564b744d78b92b920e074bb555'
FITBIT_AUTH_URL = 'https://www.fitbit.com/oauth2/authorize'
FITBIT_AUTH_TOKEN = 'https://api.fitbit.com/oauth2/token'
DATABASE_URI = 'postgresql://wearware:databit!@wearware.cqr2btyia7sd.us-west-1.rds.amazonaws.com:5432/wearware'


def results(request):
    return render(request, "reults.html")

def get_form(request):
    results = None

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = QueryForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            results = form.clean()
    # if a GET (or any other method) we'll create a blank form
    else:
        form = QueryForm()

    return render(request,'query_form.html', {'form':form, 'results':results})

def index(request):
    return render(request, "index.html")

def participantinvite(request):
    formInput = None
    if request.method == 'POST':
        form = ParticipantInviteForm(request.POST, request.FILES)
        if form.is_valid():
            formInput = form.clean()
    else:
        form = ParticipantInviteForm()
    return render(request, "participantinvite.html", {'form':form, 'results':formInput})

def callbackauthentication(request):
    fitbit = OAuth2Session(CLIENT_ID)
    token = fitbit.fetch_token(FITBIT_AUTH_TOKEN, client_secret=CLIENT_SECRET,
                               authorization_response=request.get_full_path())
    
    fitbit = OAuth2Session(CLIENT_ID, token=token)
    response = fitbit.get('https://api.fitbit.com/1/user/-/profile.json')
    response = json.loads(response.text)
    user_timezone = response['user']['timezone']
    user_fullname = response['user']['fullName']
    user_fullname = user_fullname.split(' ')
    
    #connecting to our database and setting access_token + refresh_token
    #plus basic user profile information
    engine = create_engine(DATABASE_URI)
    sql_command_participant = 'INSERT INTO public.\"WearWareRESTAPI_participant\" VALUES (1339,\''+user_fullname[0]+'\',\''+user_fullname[1]+'\',\'jensenroe@gmail.com\',\'M\',\'M\',\'40e6215d-b5c6-4896-987c-f30f3678f608\')'

    engine.execute(sql_command_participant)

    sql_command_fitbitaccount = 'INSERT INTO public.\"WearWareRESTAPI_fitbitaccount\" VALUES (DEFAULT,9998887,True,\''+user_timezone+'\',\'auth_token\',\''+str(token['oauth_token']['refresh_token'])+'\',\''+str(token['oauth_token']['refresh_token'])+'\','+str(1339)+')'
                   
    engine.execute(sql_command_fitbitaccount)
    return render(request, "callbackauthentication.html")

class CustomSerializerViewSet(APIView):
    serializers = {
        'default' : None,
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])

class ParticipantDataAPIView(CustomSerializerViewSet):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'query_form.html'

    serializers = {
        'study': StudySerializer,
        'participant': ParticipantSerializer,

    }



class StudyAPIView(APIView):
    serializer_class = StudySerializer
    renderer_classes = [AdminRenderer, JSONRenderer]

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

class StudyAPIListView(generics.ListCreateAPIView):
    serializer_class = StudySerializer
    queryset = Study.objects.all()
    renderer_classes = [AdminRenderer, JSONRenderer]

    #Return only studies from a user
    def get_queryset(self):
        user = self.request.user
        return Study.objects.filter()

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
    queryset = Participant.objects.all()
    renderer_classes = [AdminRenderer, JSONRenderer]

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

class ParticipantAPIListView(generics.ListCreateAPIView):
    serializer_class = ParticipantSerializer
    queryset = Participant.objects.all()
    renderer_classes = [AdminRenderer, JSONRenderer]

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        return Participant.objects.filter(first_name=user)

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
    renderer_classes = [AdminRenderer, JSONRenderer]

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


class FitbitMinuteRecordAPIListView(generics.ListCreateAPIView):
    serializer_class = MinuteRecordSerializer
    queryset = FitbitMinuteRecord.objects.all()
    renderer_classes = [AdminRenderer, JSONRenderer]

    #Return only data in a study from a user
    def get_queryset(self):
        user = self.request.user
        return FitbitMinuteRecord.objects.filter()

    def get(self, request, format=None):
        items = FitbitMinuteRecord.objects.order_by('pk')
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = MinuteRecordSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class FitbitHeartRecordAPIView(APIView):
    renderer_classes = [AdminRenderer, JSONRenderer]

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


class FitbitHeartRecordAPIListView(generics.ListCreateAPIView):
    serializer_class = HeartRateRecordSerializer
    queryset = FitbitHeartRecord.objects.all()
    renderer_classes = [AdminRenderer, JSONRenderer]

    #Return only HR in a study from a user
    def get_queryset(self):
        user = self.request.user
        return FitbitHeartRecord.objects.filter()

    def get(self, request, format=None):
        items = FitbitHeartRecord.objects.order_by('pk')
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = HeartRateRecordSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class FitbitSleepRecordAPIView(APIView):
    renderer_classes = [AdminRenderer, JSONRenderer]

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


class FitbitSleepRecordAPIListView(generics.ListCreateAPIView):
    serializer_class = SleepRecordSerializer
    queryset = FitbitSleepRecord.objects.all()
    renderer_classes = [AdminRenderer, JSONRenderer]

    #Return only sleep record in a study from a user
    def get_queryset(self):
        user = self.request.user
        return FitbitSleepRecord.objects.filter()

    def get(self, request, format=None):
        items = FitbitSleepRecord.objects.order_by('pk')
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = SleepRecordSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class SyncRecordAPIView(APIView):
    renderer_classes = [AdminRenderer, JSONRenderer]

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

class SyncRecordAPIListView(generics.ListCreateAPIView):
    serializer_class = SyncRecordSerializer
    queryset = SyncRecord.objects.all()
    renderer_classes = [AdminRenderer, JSONRenderer]

    #Return only sync record in a study from a user
    def get_queryset(self):
        user = self.request.user
        return SyncRecord.objects.filter()

    def get(self, request, format=None):
        items = SyncRecord.objects.order_by('pk')
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = SyncRecordSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

class StudyHasParticipantAPIView(APIView):
    serializer_class = StudyHasParticipantSerializer
    renderer_classes = [AdminRenderer, JSONRenderer]

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


class StudyHasParticipantAPIListView(generics.ListCreateAPIView):
    serializer_class = StudyHasParticipantSerializer
    queryset = StudyHasParticipant.objects.all()
    renderer_classes = [AdminRenderer, JSONRenderer]

    #Return only Researcher study record in a study from a user
    def get_queryset(self):
        user = self.request.user
        return StudyHasParticipant.objects.filter()

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
    renderer_classes = [AdminRenderer, JSONRenderer]

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


class ResearcherHasStudyAPIListView(generics.ListCreateAPIView):
    serializer_class = ResearcherHasStudySerializer
    queryset = ResearcherHasStudy.objects.all()
    renderer_classes = [AdminRenderer, JSONRenderer]

    #Return only Researcher study record in a study from a user
    def get_queryset(self):
        user = self.request.user
        return ResearcherHasStudy.objects.filter()

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
    renderer_classes = [AdminRenderer, JSONRenderer]

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


class FitbitAccountAPIListView(generics.ListCreateAPIView):
    serializer_class = AccSerializer
    queryset = FitbitAccount.objects.all()
    renderer_classes = [AdminRenderer, JSONRenderer]

    #Return only fitbitt account record from user
    def get_queryset(self):
        user = self.request.user
        return FitbitAccount.objects.filter()

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


        
