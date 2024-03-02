from django.urls import path
from . import views, botview
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
    path('tithe/',views.titheOfferings,name='tithe'),
    path('add-tithe/',views.addTitheOfferings,name='add-tithe'),
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
    path('download/',views.html_to_pdf_view.as_view(),name='download'),
    
    path('email/',views.sendEmail,name='email'),

    #Payment
    path('payment/',views.payment,name='payment'),
    path('payment-wave/',views.paymentFlutterWave,name='payment-wave'),
    path('donation/<str:link>',views.redirectPayment,name='donation'),

    #Budget
    path('add-budget/',views.addBudget,name='add-budget'),
    path('budget/',views.budget,name='budget'),

    #Reports
    path('budget-report/',views.BudgetReport.as_view(),name='budget-report'),
    path('events-report/',views.EventReport.as_view(),name='events-report'),
    path('activity-report/',views.ActivityReport.as_view(),name='activity-report'),
    path('donation-report/',views.DonationReport.as_view(),name='donation-report'),
    path('paypack/',views.paypack,name='paypack'),
<<<<<<< HEAD
     path('webhook/',views.paypack1,name='webhook'),
    #  path('openai/', botview.openaiView, name='openai'),
          
=======
>>>>>>> parent of acd46e6 (Presented version of the project)

    
]