from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    #Tasks URLs
    path('tasks/', views.tasks, name='tasks'),
    path('tasks/create_personal_task/', views.create_personal_task, name='create_personal_task'),
    path('tasks/create_team_task/', views.create_team_task, name='create_team_task'),
    #Team URLs
    path('team/', views.team, name='team'),
    path('team/join/', views.join_team, name='join_team'),
    path('team/create/', views.create_team, name='create_team'),
    path('team/edit/', views.edit_team, name='edit_team'),
    path('team/overview/<str:team_identifier>/', views.team_overview, name='team_overview'),
    path('team/kickoff/<str:team_identifier>/<str:member_identifier>/', views.kick_out_member, name='kickout_member'),
    path('team/invite/<str:team_identifier>/<str:member_identifier>/', views.invite_member, name="invite_member"),
    path('team/delete/<str:team_identifier>/', views.delete_team, name='delete_team'),
    #Help URLs
    path('help/', views.help, name='help'),
    #Session URLs
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    #Notifications URLs
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/mark_as_read_notification/<int:notification_identifier>/', views.mark_as_read_notification, name='mark_as_read_notification'),
    path('notifications/delete_notification/<int:notification_identifier>/', views.delete_notification, name='delete_notification')
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)