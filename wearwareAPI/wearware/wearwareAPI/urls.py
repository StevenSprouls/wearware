from rest_framework.routers import SimpleRouter
from WearWareRESTAPI import views


router = SimpleRouter()

router.register(r'activitylevel', views.ActivityLevelViewSet)
router.register(r'heartrate', views.HeartRateViewSet)
router.register(r'participant', views.ParticipantViewSet)
router.register(r'participantstudy', views.ParticipantStudyViewSet)
router.register(r'researcher', views.ResearcherViewSet)
router.register(r'researcherstudy', views.ResearcherStudyViewSet)
router.register(r'sleepdata', views.SleepDataViewSet)
router.register(r'study', views.StudyViewSet)

urlpatterns = router.urls
