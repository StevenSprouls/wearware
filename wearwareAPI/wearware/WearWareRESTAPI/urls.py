from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from WearWareRESTAPI import views


urlpatterns = [

    url(r'^activitylevel/(?P<pk>[0-9]+)/$', views.activitylevel_detail),
    url(r'^activitylevel/$', views.activitylevel_list),

    url(r'^heartrate/(?P<pk>[0-9]+)/$', views.heartrate_detail),
    url(r'^heartrate/$', views.heartrate_list),

    url(r'^participant/(?P<pk>[0-9]+)/$', views.participant_detail),
    url(r'^participant/$', views.participant_list),

    url(r'^participantstudy/(?P<pk>[0-9]+)/$', views.participantstudy_detail),
    url(r'^participantstudy/$', views.participantstudy_list),

    url(r'^researcher/(?P<pk>[0-9]+)/$', views.researcher_detail),
    url(r'^researcher/$', views.researcher_list),

    url(r'^researcherstudy/(?P<pk>[0-9]+)/$', views.researcherstudy_detail),
    url(r'^researcherstudy/$', views.researcherstudy_list),

    url(r'^sleepdata/(?P<pk>[0-9]+)/$', views.sleepdata_detail),
    url(r'^sleepdata/$', views.sleepdata_list),

    url(r'^study/(?P<pk>[0-9]+)/$', views.study_detail),
    url(r'^study/$', views.study_list),

]

urlpatterns = format_suffix_patterns(urlpatterns)
