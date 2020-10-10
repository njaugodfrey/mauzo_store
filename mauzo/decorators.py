from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import redirect
from userprofile.models import Profile

def allowed_user(allowed_roles=[]):
    # decorator that looks for user role
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            department = None
            if request.user.groups.exists():
                department = request.user.groups.all()[0].name
            
            if department in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('Request access denied')
        return wrapper_func
    return decorator
