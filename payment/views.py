from django.shortcuts import render, redirect, reverse, get_object_or_404
from user.models import User, Tariff, Record
from .models import Payment
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
import datetime
from dateutil.relativedelta import relativedelta
from  fitness_project import settings
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from user.decorators import *
from django.db.models import Max
# Create your views here.
@login_required(login_url="login")
@diffClient
@is_client
def view_pago(request, id, email):
  try:  
    record = Record.objects.get(userID=email)
    payment = Tariff.objects.get(pk=id)
  except:
    return redirect(reverse('recopilacion', kwargs={'email': email}))
  usuario=get_object_or_404(User, email=email)
  if payment.pk == 4:
    return redirect(reverse('tarifas', kwargs={'email': usuario.email}))
  if Payment.objects.filter(id_client=email).exists():
    x = Payment.objects.filter(id_client=usuario.email).aggregate(Max('dead_line'))
    payment = Payment.objects.get(id_client=usuario.email, dead_line=x['dead_line__max'])
    if datetime.date.today() < payment.dead_line:
      return redirect(reverse('portal', kwargs={'username': usuario.username}))

  p_final = float(payment.price) * int(payment.duracion)
  return render(request, 'pago.html', {
    'title': 'Proceso de pago',
    'usuario': usuario,
    'payment': payment,
    'p_final':p_final
  })

@login_required(login_url="login")
@csrf_exempt
@is_client
def complete(request):
  body = json.loads(request.body)
  print(body)
  stripe.api_key = settings.STRIPE_PRIVATE_KEY
  session = stripe.checkout.Session.create(
  payment_method_types=['card'],
  line_items=[{
    'price': body['1'],
    'quantity': 1,
  }],
  mode='payment',
  success_url=request.build_absolute_uri(reverse('thanks', kwargs={'username': body['4'], 'id_tarifa': body['0']})),
  cancel_url=request.build_absolute_uri(reverse('tarifas', kwargs={'email': request.user.email})),
  )


  return JsonResponse({
    'session_id': session.id,
    'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    })
    
@login_required(login_url="login")
@is_client
def thanks(request, username, id_tarifa):

  usuario = User.objects.get(username=username)
  update_tariff = User.objects.raw(f"SELECT email, 1 id FROM user_user WHERE email='{usuario.email}'")
  tarifa = Tariff.objects.get(pk=id_tarifa)
  initial_date=datetime.date.today()
  dead_line=initial_date + relativedelta(months=int(tarifa.duracion))
  p_final = float(tarifa.price) * int(tarifa.duracion)
  Payment.objects.create(
      description='Pago',
      id_client=update_tariff[0],
      quantity=p_final,
      initial_date=initial_date,
      dead_line=dead_line

  )
  request.session['username'] = usuario.username
  update = Record.objects.get(userID=usuario.email)
  update.plan_id=tarifa.pk
  update.save()
  messages.success(request, 'El pago ha sido realizado con éxito')
  return redirect(reverse('portal', kwargs={'username': usuario.username}))


    
