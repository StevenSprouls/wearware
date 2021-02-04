from WearWareRESTAPI.viewsets import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register('Participant', ParticipantViewSet)
router.register('ParticipantStudy', ParticipantStudyViewSet)
router.register('Study', StudyViewSet)
router.register('Researcher_Study', ResearcherStudyViewSet)
router.register('Researcher', ResearcherViewSet)
router.register('Activity_Level', ActivityLevelViewSet)
router.register('Heart_Rate', HeartRateViewSet)
router.register('Sleep_Data', SleepDataViewSet)

