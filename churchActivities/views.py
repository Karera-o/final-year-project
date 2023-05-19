from django.shortcuts import render

# Create your views here.

def signUp(request):
    
    return render(request, 'pages/signUp.html')

def signIn(request):
    
    return render(request, 'pages/signIn.html') 

def adminDashboard(request):
    
    return render(request, 'pages/adminDashboard.html')

def userDashboard(request):
    
    return render(request, 'pages/userDashboard.html')