from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.http import Http404



def listT(view_function):
    def sesion(request, *args, **kwargs):
        path = request.path
        session = '/list_training/' + request.session['username']

        if str(path) == str(session) or request.user.grupo.id==3:
            return view_function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return sesion