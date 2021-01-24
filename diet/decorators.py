from django.core.exceptions import PermissionDenied
import datetime
from django.db.models import Max
from payment.models import Payment
from user.models import User


def has_perm(view_function):
    def joshuas(request, *args, **kwargs):
        if request.user.grupo.id == 2:
            raise PermissionDenied
        else:
            return view_function(request, *args, **kwargs)

    return joshuas

def not_admin(view_function):
    def notAdmin(request, *args, **kwargs):
        if request.user.grupo.id == 1:
            raise PermissionDenied
        else:
            return view_function(request, *args, **kwargs)
    return notAdmin


def not_trainer(view_function):
    def notTrainer(request, *args, **kwargs):
        if request.user.grupo.id != 3:
            raise PermissionDenied
        else:
            return view_function(request, *args, **kwargs)
    return notTrainer


def listDietC(view_function):
    def sesion(request, *args, **kwargs):
        path = request.path
        session = '/listar_dieta/' + request.session['email']

        if str(path) == str(session) or request.user.grupo.id==3:
            return view_function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return sesion


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