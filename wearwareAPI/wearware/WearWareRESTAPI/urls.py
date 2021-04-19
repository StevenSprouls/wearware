import debug_toolbar
from django.conf import settings
from django.conf.urls import include, url
from WearWareRESTAPI import views
from django.urls import path
from django_filters.views import FilterView
#from WearWareRESTAPI.models import Study



app_name= 'WearWareRESTAPI'
urlpatterns = [
  path("", views.index, name='index'),
  path('__debug__/', include(debug_toolbar.urls)),

  url('/query/', views.get_form, name='query'),
  url('/results/', views.results, name='results'),

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

  url(r'^participantdata/$', views.ParticipantDataAPIView.as_view(), name='participantdata'),

]
