from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('tasks/', views.tasks, name='tasks'),
    #Team URLs
    path('team/', views.team, name='team'),
    path('team/join/', views.join_team, name='join_team'),
    path('team/create/', views.create_team, name='create_team'),
    path('team/edit/', views.edit_team, name='edit_team'),
    #Help URLs
    path('help/', views.help, name='help'),
    #Session URLs
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)