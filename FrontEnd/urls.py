from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('tasks/', views.tasks, name='tasks'),
    path('team/', views.team, name='team'),
    path('help/', views.help, name='help'),
    #Session URLs
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout,
         name='logout'),
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)