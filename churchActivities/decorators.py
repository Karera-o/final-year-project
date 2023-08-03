# decorators.py

from functools import wraps
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse

def is_admin(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            
            return HttpResponse("You don't have permission to access this page.")
    return _wrapped_view

def is_hod(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.groups.filter(name='HOD').exists():
            return view_func(request, *args, **kwargs)
        else:
            # Redirect or raise PermissionDenied as per your requirements
            return HttpResponse("You don't have permission to access this page.")
    return _wrapped_view

def is_church_board(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.groups.filter(name='ChurchBoard').exists():
            return view_func(request, *args, **kwargs)
        else:
            # Redirect or raise PermissionDenied as per your requirements
            return HttpResponse("You don't have permission to access this page.")
    return _wrapped_view

def is_normal_user(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.groups.filter(name='HOD').exists() or request.user.groups.filter(name='ChurchBoard').exists()):
            return view_func(request, *args, **kwargs)
        else:
            # Redirect or raise PermissionDenied as per your requirements
            return HttpResponse("You don't have permission to access this page.")
    return _wrapped_view
