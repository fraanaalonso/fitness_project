from django.shortcuts import redirect, reverse
from django.core.exceptions import PermissionDenied
import re

def is_admin(view_function):
    def joshuas(request, *args, **kwargs):
        if request.user.grupo.id != 1:
            raise PermissionDenied
        else:
            return view_function(request, *args, **kwargs)

    return joshuas

def is_client(view_function):
    def client(request, *args, **kwargs):
        if request.user.grupo.id != 2:
            raise PermissionDenied
        else:
            return view_function(request, *args, **kwargs)

    return client

def diffClient(view_function):
    def client_session(request, *args, **kwargs):
        if request.user.email != request.session['email']:
            raise PermissionDenied
        else:
            return view_function(request, *args, **kwargs)
    return client_session


def mixRecop(view_funtion):
    def session(request, *args, **kwargs):
        user = request.session['email']
        path = request.path
        recop = '/recopilacion/' + user
        if str(path) != str(recop):
            raise PermissionDenied
        else:
            return view_funtion(request, *args, **kwargs)
    return session


