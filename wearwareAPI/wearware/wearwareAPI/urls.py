from django.conf.urls import include, url
from WearWareRESTAPI import views


urlpatterns = [

  url(r'^activitylevel/(?P<id>[0-9]+)/$', views.ActivityLevelAPIView.as_view()),
  url(r'^activitylevel/$', views.ActivityLevelAPIListView.as_view()),

  url(r'^heartrate/(?P<id>[0-9]+)/$', views.HeartRateAPIView.as_view()),
  url(r'^heartrate/$', views.HeartRateAPIListView.as_view()),

  url(r'^participant/(?P<id>[0-9]+)/$', views.ParticipantAPIView.as_view()),
  url(r'^participant/$', views.ParticipantAPIListView.as_view()),

  url(r'^participantstudy/(?P<id>[0-9]+)/$', views.ParticipantStudyAPIView.as_view()),
  url(r'^participantstudy/$', views.ParticipantStudyAPIListView.as_view()),

  url(r'^researcher/(?P<id>[0-9]+)/$', views.ResearcherAPIView.as_view()),
  url(r'^researcher/$', views.ResearcherAPIListView.as_view()),

  url(r'^researcherstudy/(?P<id>[0-9]+)/$', views.ResearcherStudyAPIView.as_view()),
  url(r'^researcherstudy/$', views.ResearcherStudyAPIListView.as_view()),

  url(r'^sleepdata/(?P<id>[0-9]+)/$', views.SleepDataAPIView.as_view()),
  url(r'^sleepdata/$', views.SleepDataAPIListView.as_view()),

  url(r'^study/(?P<id>[0-9]+)/$', views.StudyAPIView.as_view()),
  url(r'^study/$', views.StudyAPIListView.as_view()),

]
