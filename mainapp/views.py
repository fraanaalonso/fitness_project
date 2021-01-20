from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.http import Http404
import datetime
from django.db.models import Max
from payment.models import Payment
from user.models import User
# Create your views here.


def index(request):
    return render(request, 'index.html', {
        'title': 'Inicio'
    })

def pageNotFound(request, exception):
    route = request.build_absolute_uri
    h1 = ''
    if 'username' in request.session:
        usuario = User.objects.get(email=request.session['email'])
        if request.user.grupo.id == 2:
            if Payment.objects.filter(id_client=usuario.email).exists():
                x = Payment.objects.filter(id_client=usuario.email).aggregate(Max('dead_line'))
                payment = Payment.objects.get(id_client=usuario.email, dead_line=x['dead_line__max'])
                if datetime.date.today() > payment.dead_line:
                    h1 = 'layout-errors.html'
                else:
                    h1 = 'inicio.html'
            else:
                h1 = 'layout-errors.html'
        else:
            h1 = 'inicio.html'
    else:
        h1 = 'layout-errors.html'

    return render(request, 'errors/404.html', {
        'title': 'Página no encontrada',
        'route': route,
        'h1': h1
    })

def page500(request):
    route = request.build_absolute_uri
    h1 = ''
    if 'username' in request.session:
        usuario = User.objects.get(email=request.session['email'])
        if request.user.grupo.id == 2:
            if Payment.objects.filter(id_client=usuario.email).exists():
                x = Payment.objects.filter(id_client=usuario.email).aggregate(Max('dead_line'))
                payment = Payment.objects.get(id_client=usuario.email, dead_line=x['dead_line__max'])
                if datetime.date.today() > payment.dead_line:
                    h1 = 'layout-errors.html'
                else:
                    h1 = 'inicio.html'
            else:
                h1 = 'layout-errors.html'
        else:
            h1 = 'inicio.html'
    else:
        h1 = 'layout-errors.html'

    return render(request, 'errors/500.html', {
        'title': 'Error 500',
        'h1': h1
    })



