from django.conf.urls import include, url
from WearWareRESTAPI import views
from django.urls import path
from django_filters.views import FilterView
from django_filters.views import object_filter



app_name= 'WearWareRESTAPI'
urlpatterns = [
  path("", views.index, name="index"),

  url(r'^fitbitaccount/(?P<id>[0-9]+)/$', views.FitbitAccountAPIView.as_view()),
  url(r'^fitbitaccount/$', views.FitbitAccountAPIListView.as_view(), name='account'),

  url(r'^study/(?P<id>[0-9]+)/$', views.StudyAPIView.as_view()),
  url(r'^study/$', views.StudyAPIListView.as_view(), name='study'),

  url(r'^participant/(?P<id>[0-9]+)/$', views.ParticipantAPIView.as_view()),
  url(r'^participant/$', views.ParticipantAPIListView.as_view(), name='participant'),

  url(r'^fitbitminuterecord/(?P<id>[0-9]+)/$', views.FitbitMinuteRecordAPIView.as_view()),
  url(r'^fitbitminuterecord/$', views.FitbitMinuteRecordAPIListView.as_view(),name='fitbitactivityrecord'),

  url(r'^fitbitheartrecord/(?P<id>[0-9]+)/$', views.FitbitHeartRecordAPIView.as_view()),
  url(r'^fitbitheartrecord/$', views.FitbitHeartRecordAPIListView.as_view(),name='fitbitheartrecord'),

  url(r'^fitbitsleeprecord/(?P<id>[0-9]+)/$', views.FitbitSleepRecordAPIView.as_view()),
  url(r'^fitbitsleeprecord/$', views.FitbitSleepRecordAPIListView.as_view(),name='fitbitsleeprecord'),

  url(r'^syncrecord/(?P<id>[0-9]+)/$', views.SyncRecordAPIView.as_view()),
  url(r'^syncrecord/$', views.SyncRecordAPIListView.as_view(),name='syncrecord'),

  url(r'^studyhasparticipant/(?P<id>[0-9]+)/$', views.StudyHasParticipantAPIView.as_view()),
  url(r'^studyhasparticipant/$', views.StudyHasParticipantAPIListView.as_view(),name='studyhasparticipant'),

  url(r'^researcherhasstudy/(?P<id>[0-9]+)/$', views.ResearcherHasStudyAPIView.as_view()),
  url(r'^researcherhasstudy/$', views.ResearcherHasStudyAPIListView.as_view(),name='researcherhasstudy'),

  url(r'^participantdata/(?P<id>[0-9]+)/$', views.ParticipantDataAPIView.as_view()),
  url(r'^participantdata/$', views.ParticipantDataAPIListView.as_view(),name='participantdata'),

]
