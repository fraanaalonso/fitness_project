from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect, HttpResponse, Http404
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.forms import UserCreationForm
from user.forms import *
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from user.models import User, Record, Tariff, Image
from django.contrib.auth import views as vistas
from django.urls import reverse
from payment.models import Payment
import datetime
from datetime import date, timedelta
from django.core.paginator import Paginator
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.hashers import make_password
from django.views.generic import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from user.decorators import *
from diet.decorators import not_admin, not_trainer
from django.db.models import Max
from dateutil.relativedelta import relativedelta
from django.contrib.auth import update_session_auth_hash
# Create your views here.


def registerApp(request):

    if request.user.is_authenticated:
        return redirect(reverse('portal', kwargs={'username':request.session['username']}))
    else:
        if request.method == 'POST':
            try:
                correo = request.POST.get('email')
                login = User.objects.get(email=correo)
                messages.error(request, "El correo ya existe")
                return redirect('register')          
            except User.DoesNotExist:
                form_Register = registerForm(request.POST)
                if form_Register.is_valid():
                    grupo = Group.objects.raw(f"SELECT id FROM auth_group WHERE id='2'")
                    user = form_Register.save(commit=False)
                    user.active = False
                    user.staff= False
                    user.grupo = grupo[0]
                    user.is_superuser = False
                    user.guardarUsername()
                    user.save()
                    current_site = get_current_site(request)
                    mail_subject = 'Activacion de cuenta Bulk&Shred'
                    message = render_to_string('users/activacion.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                        'token':account_activation_token.make_token(user),
                    })
                    to_email = form_Register.cleaned_data.get('email')
                    email = EmailMessage(mail_subject, message, to=[to_email])
                    messages.success(request, "Email enviado. Consulte su buzón de entrada.")
                    email.send()
                    return redirect('inicio')
        else:
            form_Register = registerForm()
        return render(request, 'users/register.html', {'form_Register': form_Register, 'title': 'Registro'})

def reset_password(request):
    form = PasswordResetForm()

    if request.method == 'POST':
        form=PasswordResetForm(request.POST)
        if form.is_valid():
            correo = request.POST.get('email')
            try:
                user = get_object_or_404(User,email=correo)
                current_site = get_current_site(request)
                mail_subject = 'Solicitud de cambio de contraseña'
                message = render_to_string('users/passwords/password_reset_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':account_activation_token.make_token(user),

                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()
                return redirect('password-done')
            
            except User.DoesNotExist:
                messages.error(request, "Esta cuenta no existe")
                return redirect('password_reset')

    return render(request, 'users/passwords/reset_password.html', {
        'title': 'Nueva Contraseña',
        'form': form
    })

def pasword_done(request):
    return render(request, 'users/passwords/password_reset_done.html', {
        'title': 'Email enviado'
    })

def password_reset_confirm(request,  uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        form = PasswordCorfirmForm()
        return render(request, 'users/passwords/password_reset_confirm.html', {
            'title': 'Cambio de Contraseña',
            'form': form,
            'uidb64': uidb64,
            'token': token})
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        return redirect('login')
    
    
        


def password_reset_complete(request):
    uidb64 = request.POST.get('uidb64')
    token = request.POST.get('token')
    if request.method == 'POST':
        form = PasswordCorfirmForm(request.POST)
        if form.is_valid():
            password = request.POST['password']
            password_confirm = request.POST['password_confirm']
            if password != password_confirm:
                messages.error(request, 'Las contraseñas no coinciden')
                return redirect(reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token}))
            else:
                uid = force_text(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=uid)
                key = make_password(password)
                user.password = key
                user.save()
                messages.success(request, 'Contraseña actualizada')
                return redirect('login')
        else:
            messages.error(request, 'Las contraseñas no cumplen las condiciones')
            form = PasswordCorfirmForm()
            return render(request, 'users/passwords/password_reset_confirm.html', {
            'form': form,
            'uidb64': uidb64,
            'token': token})
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.active = True
        user.save()
        return render(request, 'users/messages.html',{
            'content':'Has confirmado la cuenta. Ya puedes iniciar sesión',
            'title': 'Confirmación Cuenta Bulk & Shred'
            })
    else:
        
        return render(request, 'users/messages.html',{
            'content':'Ha habido un error. No puedes iniciar sesión',
            'title': 'Confirmación Cuenta Bulk & Shred'
            })



def LoginApp(request):
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:

            if user.active==True and user.grupo.id == 2:
                login(request, user)
                username=user.username
                mail = user.email
                request.session['username'] = username
                request.session['email'] = mail
                return redirect(reverse('recopilacion', kwargs={"email": email})) 
            elif user.active==True and (user.grupo.id == 3 or user.grupo.id==1):
                login(request, user)
                username=user.username
                mail = user.email
                request.session['username'] = username
                request.session['email'] = mail
                return redirect(reverse('portal', kwargs={'username': request.session['username']}))
            else:
                messages.error(request, 'Activa tu cuenta')
                return redirect('login')
        else:
            messages.error(request, 'Credenciales erróneas')
    
    else:
        if 'username' in request.session and request.user.grupo.id == 2:
            return redirect(reverse('recopilacion', kwargs={"email": request.user.email}))
        elif 'username' in request.session and (request.user.grupo.id == 1 or request.user.grupo.id == 3):
            return redirect(reverse('portal', kwargs={'username': request.session['username']}))

                
    return render(request, 'users/login.html',
    {
        'title': 'Identifícate'
    })


@login_required(login_url="login")
def logoutApp(request):
    try:
        auth.logout(request)
        del request.session['username']
    except KeyError:
        pass
    return redirect('login')

@login_required(login_url="login")
@is_admin
def showUsers(request):
    users = User.objects.all()
    paginator = Paginator(users, 10)

    page = request.GET.get('page')
    page_users = paginator.get_page(page)
    sesion = User.objects.get(username=request.session['username'])
    return render(request, 'users/crud/users.html', {
        'title': 'Listado de Usuarios',
        'users': page_users,
        'sesion': sesion
    })

    return render(request, 'users/crud/users.html', {
        'title': 'Gestión de Usuarios',
        'users': users,
    })

@login_required(login_url="login")
@is_admin
def eraseUser(request, email):
    try:
        user_email=User.objects.get(pk=email)
        user_email.delete()
    except User.DoesNotExist:
        messages.error(request, 'El usuario no existe')
        return redirect('show-users')
    except:
        messages.error(request, 'Ha ocurrido un problema')
        return redirect('show-users')
    messages.success(request, f'El usuario {user_email.first_name} ha sido eliminado')
    return redirect('show-users')

@login_required(login_url="login")
@is_admin
def addUser(request):
    
    if request.method == 'POST':
        form_user = addUserForm(request.POST)
        form_ficha = editFicha2(request.POST, request.FILES)
        if  form_user.is_valid and form_ficha.is_valid:

            try:  
                    
                usuario = form_user.save(commit=False)
                grupo = Group.objects.raw(f"SELECT id FROM auth_group WHERE id='{request.POST['grupo']}'")
                usuario.grupo = grupo[0]
                usuario.save()
                password = make_password(usuario.password)
                usuario.password = password
                usuario.save()
                ficha = form_ficha.save(commit=False)
                user_id = User.objects.raw(f"SELECT email FROM user_user WHERE email='{request.POST['userID']}'")
                ficha.userID = user_id[0]
                ficha.save()

                if grupo[0].id == 2:
                    tarifa = Tariff.objects.get(pk=request.POST['plan'])
                    initial_date=datetime.date.today()
                    dead_line=initial_date + relativedelta(months=int(tarifa.duracion))
                    precio = float(tarifa.price) * int(tarifa.duracion)
                    Payment.objects.create(description="Por admin", id_client=user_id[0], quantity=precio, initial_date=initial_date, dead_line=dead_line)
                messages.success(request, f"Usuario con nombre {usuario.first_name} ha sido añadido correctamente")

                return redirect('show-users')
            except:
                try:
                    cliente_fallo = User.objects.get(email=request.POST['email'])
                    cliente_fallo.delete()
                except:
                    return render(request, 'users/crud/add-user.html', {
                        'title': 'Añadir Usuario',
                        'form_user': form_user,
                        'form_ficha':form_ficha,

                    })
                    
                return render(request, 'users/crud/add-user.html', {
                'title': 'Añadir Usuario',
                'form_user': form_user,
                'form_ficha':form_ficha,

            })
        else:
            return render(request, 'users/crud/add-user.html', {
                'title': 'Añadir Usuario',
                'form_user': form_user,
                'form_ficha':form_ficha,

            })
        
    else:
        form_ficha = editFicha2()
        form_user = addUserForm()      
        return render(request, 'users/crud/add-user.html', {
            'title': 'Añadir Usuario',
            'form_user': form_user,
            'form_ficha':form_ficha,

        })

@login_required(login_url="login")
@is_admin
def editUser(request, email):
    try:
        usuario = User.objects.get(pk=email)
        form_user = editUserForm(instance=usuario)
        ficha = Record.objects.get(userID=email)
        form_ficha = editFicha2(instance=ficha)

        if request.method == 'POST':
            form_user = editUserForm(request.POST, instance=usuario)
            form_ficha = editFicha2(request.POST, request.FILES, instance=ficha)
            if  form_user.is_valid:

                try: 
                    usuario = form_user.save(commit=False)
                    grupo = Group.objects.raw(f"SELECT id FROM auth_group WHERE id='{request.POST['grupo']}'")
                    usuario.grupo = grupo[0]
                    usuario.save()
                    ficha = form_ficha.save(commit=False)
                    ficha.save()

                    messages.success(request, f"Usuario con nombre {usuario.first_name} ha sido modificado correctamente")

                    return redirect('show-users')
                
                except:
                    
                    return render(request, 'users/crud/edit-user.html', {
                        'title': 'Edición Usuario',
                        'usuario':usuario,
                        'form_user': form_user,
                        'form_ficha':form_ficha,

                    })
                
                
        else:      
            return render(request, 'users/crud/edit-user.html', {
                'title': 'Edición Usuario',
                'usuario':usuario,
                'form_user': form_user,
                'form_ficha':form_ficha,

            })
    except Record.DoesNotExist:
        messages.warning(request, "El usuario no ha completado su proceso de registro")
        return redirect('show-users')


@login_required(login_url="login")
def portal(request, username):
    uid = request.path
     
    user = get_object_or_404(User, username=request.session['username'])
    user_data = get_object_or_404(Record, userID=user.email)
    plan = Payment.objects.filter(id_client=user.email).aggregate(Max('dead_line'))
    
    return render(request, 'users/portal.html', {
        'title': 'Portal de Inicio',
        'user':user,
        'user_data':user_data,
        'plan': plan['dead_line__max']
    })

@login_required(login_url="login")
@is_client
@mixRecop
def recopilacion(request, email):
    message_count = len(Record.objects.filter(userID=email))
    if message_count==0:
        usuario = get_object_or_404(User, pk=email)
        form_user = UserRecopilacionForm(instance=usuario)
        form_ficha = editFicha()

        if request.method=='POST':
            form_user = UserRecopilacionForm(request.POST, instance=usuario)
            form_ficha = editFicha(request.POST, request.FILES)

            if  form_user.is_valid and form_ficha.is_valid:
                try:
                    usuario = form_user.save(commit=False)
                    usuario.save()
                    ficha = form_ficha.save(commit=False)
                    email_user = User.objects.raw(f"SELECT email FROM user_user WHERE email='{request.POST['userID']}'")
                    plan = Tariff.objects.raw("SELECT id FROM user_tariff where id='4'")
                    ficha.userID = email_user[0]
                    ficha.plan = plan[0]
                    ficha.save() 

                    return redirect(reverse('tarifas', kwargs={"email": email}))
                except:
                    return render(request, 'users/recopilacion.html', {
                    'title': 'Recopilación de Datos',
                    'form_user': form_user,
                    'form_ficha':form_ficha,
                    'usuario':usuario,

                })
            
            
            else:
                return render(request, 'users/recopilacion.html', {
                    'title': 'Recopilación de Datos',
                    'form_user': form_user,
                    'form_ficha':form_ficha,
                    'usuario':usuario,

                })
        else:

            return render(request, 'users/recopilacion.html', {
                'title': 'Recopilación de Datos',
                'usuario':usuario,
                'form_user': form_user,
                'form_ficha':form_ficha,

            })
    else:
        return redirect(reverse('tarifas', kwargs={"email": email}))


    

@login_required(login_url="login")
@is_client
def seleccionarTarifa(request, email):
    user = User.objects.get(pk=email)
    tarifas = Tariff.objects.filter(id__lt=4) #ids menores a 4
    try:
        if Payment.objects.filter(id_client=email).exists():
            x = Payment.objects.filter(id_client=user.email).aggregate(Max('dead_line'))
            payment = Payment.objects.get(id_client=user.email, dead_line=x['dead_line__max'])
            if datetime.date.today() >= payment.dead_line:

                return render(request, 'users/tariff_selection.html', {
                'title': 'Selecciona la Tarifa',
                'tarifas': tarifas,
                'user':user
                })
                
            else:
                return redirect(reverse('portal', kwargs={"username": user.username}))
        else:
            record =Record.objects.filter(userID=email)
            if len(record) == 0:
                return redirect(reverse('recopilacion', kwargs={'email': user.email}))
            else:
                return render(request, 'users/tariff_selection.html', {
                'title': 'Selecciona la Tarifa',
                'tarifas': tarifas,
                'user':user
                })
    except:
        return render(request, 'users/tariff_selection.html', {
                'title': 'Selecciona la Tarifa',
                'tarifas': tarifas,
                'user':user
                })
        


@login_required(login_url="login")
@not_trainer
def getUsuarios(request, username):
    usuario = User.objects.get(username=username)
    asigned_users = User.objects.filter(is_trainer_id=usuario.email)
    return render(request, 'trainers/usuarios_asignados.html', {
        'title':'Mis Clientes',
        'users':asigned_users
    })

@login_required(login_url="login")
def userDetail(request, email):
    try:
        usuario=User.objects.get(email=email)
        ficha=Record.objects.get(userID=usuario.email)
        staff=User.objects.get(username=usuario.username)
    except Record.DoesNotExist:
        
        messages.warning(request, "El usuario aún no ha completado el proceso de registro")
        return redirect('show-users')
    return render(request, 'users/detail.html', {
        'title': f"Usuario {usuario.username}",
        'username':usuario,
        'ficha':ficha,
        'staff':staff,
    })


@login_required(login_url="login")
@not_trainer
def calculate(request, username):
    usuario=User.objects.get(username=username)
    ficha=Record.objects.get(userID=usuario.email)
    tmb=0
    peso=int(ficha.weight)
    altura=int(ficha.height)
    fecha_nac = ficha.date
    edad = usuario.calc_edad(fecha_nac.year)
    
    if ficha.gender=="Hombre":
        tmb=10*peso + 6.25*altura - 5*edad + 5
    elif ficha.gender=="Mujer":
        tmb=10*peso + 6.25*altura - 5*edad - 161
    
    coeficientes = {
        'Poco o ningún Ejercicio': '1.2',
        'Ejercicio ligero - 1-3 días/semana': '1.375',
        'Ejercicio moderado - 3-5 días/semana': '1.55',
        'Ejercicio fuerte - 6-7 días/semana': '1.725',
        'Ejercicio muy fuerte - 2 veces al día': '1.9'
    }

    

    return render(request, 'users/diet/calculate.html', {
        'title': 'Añadir Dieta',
        'ficha':ficha,
        'usuario':usuario,
        'tmb':tmb,
        'coeficientes': coeficientes,

    })

@login_required(login_url="login")
def misFotos(request, username): 
    try:
        user = User.objects.get(username=username)
        listado = Image.objects.filter(user=user.email)
        

        return render(request, 'users/photos/list-photos.html', {
                'title': 'Listado de Fotos',
                'listado':listado,
                'user':user,
            })

    except Image.DoesNotExist:
        return render(request, 'users/photos/list-photos.html', {
            'title': 'Listado de Fotos',
            'user':user,
        })
@login_required(login_url="login")
@is_client
def upload_image(request, username):
    form = ImageForm()
    if request.method == 'POST':

        form = ImageForm(request.POST, request.FILES)
        email_user = User.objects.get(username=username)
        if form.is_valid():
            new_image = form.save()
            new_image.user.add(email_user.email)
            new_image.save() #Almacenamos la img y datos de usuario

            return redirect(reverse('mis-fotos', kwargs={"username": email_user.username}))
    else:
        return render(request, 'users/photos/add-photo.html', {
            'title': 'Añadir Foto',
            'form': form
        })

    return render(request, 'users/photos/list-photos.html', {
            'title': 'Listado de Fotos',
            'user': email_user
        })

@login_required(login_url="login")
@is_client
def deleteImage(request, username, id):
    try:
        usuario = User.objects.get(username=username)
        image = Image.objects.get(pk=id, user=usuario.email)
        image.delete()
        messages.success(request, "La imagen ha sido eliminada correctamente")
    except Image.DoesNotExist:
        messages.error(request, "La imagen no existe")
        return redirect(reverse('mis-fotos', kwargs={"username": usuario.username}))
    return redirect(reverse('mis-fotos', kwargs={"username": usuario.username}))

@login_required(login_url="login")
@is_client
def detailImage(request, username, id):
    try:
        usuario = User.objects.get(username=username)
        imagen = Image.objects.get(pk=id, user=usuario.email)
    except Image.DoesNotExist:
        messages.error(request, "La imagen no existe")
        return redirect(reverse('mis-fotos', kwargs={"username": usuario.username}))
    return render(request, 'users/photos/detail-photo.html', {
        'imagen': imagen,
        'title': 'Imagen en Detalle'
    })

@login_required(login_url="login")
@is_admin
def showGroups(request):
    groups = Group.objects.all()
    return render(request, 'groups/show-group.html', {
        'title': 'Grupos',
        'groups': groups

    })

@login_required(login_url="login")
@is_admin
def userGroups(request, id):
    grupo = Group.objects.get(pk=id)
    usuarios = User.objects.filter(grupo=id)

    return render(request, 'groups/group-users.html', {
        'title': f'{grupo.name}',
        'usuarios': usuarios

    })


@login_required(login_url="login")
@is_admin
def eraseGroup(request, id):
    try:
        group = Group.objects.get(pk=id)
        group.delete()
    except Group.DoesNotExist:
        messages.error(request, "El grupo no existe")
        return redirect('show-groups')
    messages.success(request, f"Grupo {group.name} eliminado correctamente!")
    return redirect('show-groups')




def passChangeView(request, username):
    user = get_object_or_404(User, username=username)
    form = PasswordChangeForm(user)
    if request.method=="POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, f"Contraseña del usuario {user.first_name}, {user.last_name} actualizada correctamente. ")
            return redirect(reverse('portal', kwargs={'username': request.session['username']}))
        else:
            return render(request, 'users/passwords/password_change_form.html', {
                'title': 'Cambio de contraseña',
                'form': form,
            })
    else:
        form = PasswordChangeForm(user)
    
    return render(request, 'users/passwords/password_change_form.html', {
        'title': 'Cambio de contraseña',
        'form': form,
    })





