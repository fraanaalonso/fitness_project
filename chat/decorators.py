from django.shortcuts import redirect, reverse
from django.core.exceptions import PermissionDenied

def mixChat(view_funtion):
    def session(request, *args, **kwargs):
        user = request.session['username']
        path = request.path
        recop = '/index_users/' + user
        if str(path) != str(recop):
            raise PermissionDenied
        else:
            return view_funtion(request, *args, **kwargs)
    return session


