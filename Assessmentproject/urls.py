from django.contrib import admin
from . import views
from django.urls import path,include 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('Users/',include('Client.urls')),
    path('Corporate/',include('Corporate.urls')),
    path('User-pref/',include('ClientPreferences.urls')),
    path('Assessment/',include('questions.urls')),
    path('',views.index,name = "homepage")
]

from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)