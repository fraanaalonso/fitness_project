from django.core.exceptions import PermissionDenied



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