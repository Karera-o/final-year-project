from django.shortcuts import render

# Create your views here.

# def signUp(request):

#     pageTitle = 'SignUp'
#     context = {
#         'pageTitle': pageTitle,
#     }
    
#     return render(request, 'pages/signUp.html',context)

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

def signUp(request):
    pageTitle = 'SignUp'

    if request.method == 'POST':
        print('received')
      
        form = SignupForm(request.POST)
        if form.is_valid():
            print('valid')
            user = form.save()
            print('received')
            login(request, user)
            return redirect('admin-dashboard')  # Replace 'home' with the name of your home view
        else:
            print(form.errors)

    else:
        form = SignupForm()
    
    context = {
        'pageTitle': pageTitle,
        'form': form
    }
    
    return render(request, 'pages/signUp.html',context)

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

def adminDashboard(request):
    
    return render(request, 'pages/userDashboard.html')