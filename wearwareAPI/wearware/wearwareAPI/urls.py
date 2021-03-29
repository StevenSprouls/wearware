import debug_toolbar
from django.conf import settings
from django.conf.urls import include, url
from django.urls import path
from WearWareRESTAPI import views,urls
from django.contrib import admin

urlpatterns = [

  path("", views.index, name="index"),
  path('WearWareRESTAPI', include('WearWareRESTAPI.urls')),

  path('admin/', admin.site.urls),
  path('accounts/', include('django.contrib.auth.urls')),

  path('__debug__/', include(debug_toolbar.urls)),
]
