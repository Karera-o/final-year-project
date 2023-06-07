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

# def adminDashboard(request):

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import SignupForm, SigninForm

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Replace 'home' with the name of your home view
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def signin(request):
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Replace 'home' with the name of your home view
            else:
                return render(request, 'signin.html', {'form': form, 'error': 'Invalid email or password.'})
    else:
        form = SigninForm()
    return render(request, 'signin.html', {'form': form})

def signout(request):
    logout(request)
    return redirect('home')  # Replace 'home' with the name of your home view

    
    return render(request, 'pages/adminDashboard.html')

def userDashboard(request):
    
    return render(request, 'pages/userDashboard.html')