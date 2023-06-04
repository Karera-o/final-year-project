from django.shortcuts import render

# Create your views here.

def signUp(request):

    pageTitle = 'SignUp'
    context = {
        'pageTitle': pageTitle,
    }
    
    return render(request, 'pages/signUp.html',context)

def signIn(request):

    pageTitle = 'SignIn'
    context = {
        'pageTitle': pageTitle,
    }
    
    return render(request, 'pages/signIn.html',context) 

def adminDashboard(request):
    
    return render(request, 'pages/adminDashboard.html')

def userDashboard(request):
    
    return render(request, 'pages/userDashboard.html')