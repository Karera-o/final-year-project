from django.urls import path
from . import views
urlpatterns = [
    path('', views.signUp, name='signup'),
    path('signin/', views.signIn, name='signin'),
    path('signout/',views.signout,name='signout'),
    path('dashboard/', views.adminDashboard, name='dashboard'),
    path('user-dashboard/', views.userDashboard, name='user-dashboard'),
    path('hod-dashboard/', views.hodDashboard, name='hod-dashboard'),
    path('assign-group/',views.assignGroup,name='assign-group'),
    path('members/',views.members,name='members'),
    path('events/',views.events,name='events'),
    path('activities/',views.activities,name='activities'),
    path('logs/',views.logs, name='logs'),
    path('announcements/',views.announcements,name='announcements'),
    path('add-event/',views.addEvent,name='add-event'),
    path('add-activity/',views.addActivity,name='add-activity'),
    path('add-announcement/',views.addAnnouncement,name='add-announcement'),
    path('del-event/<int:id>',views.deletingEvent, name='del-event'),
    path('update-event/<int:id>',views.updateEvent, name='update-event'),
    path('del-activity/<int:id>',views.deletingActivity, name='del-activity'),
    path('update-activity/<int:id>',views.updateActivity, name='update-activity'),
    path('del-announcement/<int:id>',views.deletingAnnouncement, name='del-announcement'),
    path('update-announcement/<int:id>',views.updateAnnouncement, name='update-announcement'),
    path('download/',views.html_to_pdf_view.as_view(),name='download')
]