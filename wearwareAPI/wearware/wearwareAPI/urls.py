from django.conf.urls import include, url
from django.urls import path
from WearWareRESTAPI import views,urls
from django.contrib import admin

urlpatterns = [

  path("", views.index, name="index"),

  path('WearWareRESTAPI', include('WearWareRESTAPI.urls')),

  path('admin/', admin.site.urls),
]