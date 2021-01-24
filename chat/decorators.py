from django.shortcuts import redirect, reverse
from django.core.exceptions import PermissionDenied
import datetime
from django.db.models import Max
from payment.models import Payment
from user.models import User



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


def notPay(view_function):
    def session(request, *args, **kwargs):
        if request.user.grupo.id == 2:
            if Payment.objects.filter(id_client=request.user.email).exists():
                x = Payment.objects.filter(id_client=request.user.email).aggregate(Max('dead_line'))
                payment = Payment.objects.get(id_client=request.user.email, dead_line=x['dead_line__max'])
                if datetime.date.today() > payment.dead_line:
                    raise PermissionDenied
                else:
                    return view_function(request, *args, **kwargs)
            else:
                raise PermissionDenied
        elif request.user.grupo.id == 3:
            return view_function(request, *args, **kwargs)
        
    return session