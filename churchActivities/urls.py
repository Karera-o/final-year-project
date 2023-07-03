from django.urls import path
from . import views
urlpatterns = [
    path('', views.signUp, name='signup'),
    path('signin/', views.signIn, name='signin'),
    path('dashboard/', views.adminDashboard, name='dashboard'),
    path('user-dashboard/', views.userDashboard, name='user-dashboard'),
    path('members/',views.members,name='members'),
    path('events/',views.events,name='events'),
    path('activities/',views.activities,name='activities'),
    path('logs/',views.logs, name='logs'),
    path('announcements/',views.announcements,name='announcements'),

]