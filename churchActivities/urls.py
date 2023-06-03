from django.urls import path
from . import views
urlpatterns = [
    path('', views.signUp, name='signup'),
    path('signin/', views.signIn, name='signin'),
    path('admin-dashboard/', views.adminDashboard, name='admin-dashboard'),
    path('user-dashboard/', views.userDashboard, name='user-dashboard'),

]