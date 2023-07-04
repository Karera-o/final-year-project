from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm, SigninForm



#Signup
def signUp(request):
    pageTitle = 'SignUp'

    if request.method == 'POST':
        print('received')
      
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            password = form.cleaned_data['password1']
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
        else:
            print(form.errors)

    else:
        form = SignupForm()
    
    context = {
        'pageTitle': pageTitle,
        'form': form
    }
    
    return render(request, 'pages/signUp.html',context)

#Signin Page
def signIn(request):
    print('signin')
    if request.method == 'POST':
        print('received')
        form = SigninForm(request, data=request.POST)
        if form.is_valid():
            print('valid')
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  
            else:
                print('The user does not exit')
                return render(request, 'pages/signIn.html', {'form': form, 'error': 'Invalid email or password.'})
        else:
            print('error')
            print(form.errors)
    else:
        form = SigninForm()
    return render(request, 'pages/signIn.html', {'form': form})

#Signout 
def signout(request):
    logout(request)
    return redirect('home')  # Replace 'home' with the name of your home view

    
    return render(request, 'pages/index.html')

#User dashboard
def userDashboard(request):
    
    return render(request, 'pages/index.html')

#Admin dashboard
def adminDashboard(request):

    if request.headers.get('HX-Request'):
        return render(request, 'pages/index-template.html')
    
    return render(request, 'pages/index.html')

#Members page
def members(request):
    
    return render(request, 'pages/members.html')

#Events Page
def events(request):
    
    return render(request, 'pages/events.html')

#Activities Page
def activities(request):
    
    return render(request, 'pages/activities.html')

#Announcements Page
def announcements(request):
    
    return render(request, 'pages/announcements.html')

#Logs Page
def logs(request):
    
    return render(request, 'pages/logs.html')
