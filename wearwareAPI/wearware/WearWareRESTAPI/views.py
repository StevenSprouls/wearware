from rest_framework.decorators import api_view
from rest_framework.response import Response
from WearWareRESTAPI.models import ActivityLevel, HeartRate, Participant, ParticipantStudy, Researcher, ResearcherStudy, SleepData, Study
from WearWareRESTAPI.serializers import ActivityLevelSerializer, HeartRateSerializer, ParticipantSerializer, ParticipantStudySerializer, ResearcherSerializer, ResearcherStudySerializer, SleepDataSerializer, StudySerializer


@api_view(['GET', 'POST'])
def activitylevel_list(request):
    if request.method == 'GET':
        items = ActivityLevel.objects.order_by('pk')
        serializer = ActivityLevelSerializer(items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ActivityLevelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def activitylevel_detail(request, pk):
    try:
        item = ActivityLevel.objects.get(pk=pk)
    except ActivityLevel.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = ActivityLevelSerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ActivityLevelSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=204)


@api_view(['GET', 'POST'])
def heartrate_list(request):
    if request.method == 'GET':
        items = HeartRate.objects.order_by('pk')
        serializer = HeartRateSerializer(items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = HeartRateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def heartrate_detail(request, pk):
    try:
        item = HeartRate.objects.get(pk=pk)
    except HeartRate.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = HeartRateSerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = HeartRateSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=204)


@api_view(['GET', 'POST'])
def participant_list(request):
    if request.method == 'GET':
        items = Participant.objects.order_by('pk')
        serializer = ParticipantSerializer(items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ParticipantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def participant_detail(request, pk):
    try:
        item = Participant.objects.get(pk=pk)
    except Participant.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = ParticipantSerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ParticipantSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=204)


@api_view(['GET', 'POST'])
def participantstudy_list(request):
    if request.method == 'GET':
        items = ParticipantStudy.objects.order_by('pk')
        serializer = ParticipantStudySerializer(items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ParticipantStudySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def participantstudy_detail(request, pk):
    try:
        item = ParticipantStudy.objects.get(pk=pk)
    except ParticipantStudy.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = ParticipantStudySerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ParticipantStudySerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=204)


@api_view(['GET', 'POST'])
def researcher_list(request):
    if request.method == 'GET':
        items = Researcher.objects.order_by('pk')
        serializer = ResearcherSerializer(items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ResearcherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def researcher_detail(request, pk):
    try:
        item = Researcher.objects.get(pk=pk)
    except Researcher.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = ResearcherSerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ResearcherSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=204)


@api_view(['GET', 'POST'])
def researcherstudy_list(request):
    if request.method == 'GET':
        items = ResearcherStudy.objects.order_by('pk')
        serializer = ResearcherStudySerializer(items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ResearcherStudySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def researcherstudy_detail(request, pk):
    try:
        item = ResearcherStudy.objects.get(pk=pk)
    except ResearcherStudy.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = ResearcherStudySerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ResearcherStudySerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=204)


@api_view(['GET', 'POST'])
def sleepdata_list(request):
    if request.method == 'GET':
        items = SleepData.objects.order_by('pk')
        serializer = SleepDataSerializer(items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SleepDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def sleepdata_detail(request, pk):
    try:
        item = SleepData.objects.get(pk=pk)
    except SleepData.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = SleepDataSerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SleepDataSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=204)


@api_view(['GET', 'POST'])
def study_list(request):
    if request.method == 'GET':
        items = Study.objects.order_by('pk')
        serializer = StudySerializer(items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = StudySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def study_detail(request, pk):
    try:
        item = Study.objects.get(pk=pk)
    except Study.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = StudySerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = StudySerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        item.delete()
        return Response(status=204)
