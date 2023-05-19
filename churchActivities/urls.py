from django.urls import path
from . import views
urlpatterns = [
    path('', views.signUp, name='signUp'),
    path('sign-in/', views.signIn, name='sign-in'),
    path('admin-dashboard/', views.adminDashboard, name='admin-dashboard'),
    path('user-dashboard/', views.userDashboard, name='user-dashboard'),

]