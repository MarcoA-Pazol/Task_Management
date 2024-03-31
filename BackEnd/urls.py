from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/', views.api, name='api'),
]

urlpatterns+=static(settings.MEDIA_URL, documentroot=settings.MEDIA_ROOT)