
from django.shortcuts import render, redirect, reverse, HttpResponseRedirect, HttpResponse, get_object_or_404
from .models import Exercise, Training, Practice
from .forms import exerciseForm, practiceForm, formTraining
from django.contrib import messages
from django.core.paginator import Paginator
from user.models import User, Record
import datetime
from datetime import date
from django.template.loader import get_template
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
import tempfile
from training.decorators import *
from diet.decorators import *
from django.contrib.auth.decorators import login_required


@login_required(login_url="login")
@has_perm
def addExercise(request):

    if request.method == 'POST':
        form = exerciseForm(request.POST, request.FILES)

        if form.is_valid():

            try:
                exercise = form.save()
                exercise.save()
                messages.success(request, "Ejercicio añadido")

                return redirect('show-exercises')
            except (Exception, e):
                messages.error(request, str(e))
        else:
             return render(request, 'exercises_crud/add-exercise.html', {
                'title': 'Añadir Ejercicio',
                'form': form
            })

    else:
        form = exerciseForm()
    
    return render(request, 'exercises_crud/add-exercise.html', {
        'title': 'Añadir Ejercicio',
        'form': form
    })


@login_required(login_url="login")
@has_perm
def deleteExercise(request, id):
    try:
        exercise = Exercise.objects.get(pk=id)
        exercise.delete()
        messages.success(request, "Ejericio eliminado correctamente")
    except Exercise.DoesNotExist:
        messages.error(request, "No existe el ejercicio")
        return redirect('show-exercises')
    except:
        messages.error(request, "Ha habido un problema")
        return redirect('show-exercises')

    return redirect('show-exercises')


@login_required(login_url="login")
@has_perm
def editExercise(request, id):
    try:
        exercise = get_object_or_404(Exercise, pk=id)
        form = exerciseForm(instance=exercise)

        if request.method == 'POST':
            form = exerciseForm(request.POST, request.FILES, instance=exercise)

            if form.is_valid():
                form.save()
                messages.success(request, "Ejercicio editado correctamente")
                return redirect('show-exercises')
            
            else:
                return render(request, 'exercises_crud/edit-exercise.html', {
                        'title': 'Editar Ejercicio',
                        'form': form,
                        'exercise': exercise
                    })
        else:
            return render(request, 'exercises_crud/edit-exercise.html', {
                'title': 'Editar Ejercicio',
                'form': form,
                'exercise': exercise
            })
    except Exercise.DoesNotExist:
        messages.success(request, "No existe el ejercicio")
        return redirect('show-exercises')
    except:
        messages.success(request, "Ha habido un problema")
        return redirect('show-exercises')




@login_required(login_url="login")
def detailExercise(request, id):
    try:
        exercise = Exercise.objects.get(pk=id)
    except Exercise.DoesNotExist:
        messages.error(request, "No existe este ejercicio")
        return redirect('show-exercises')
    return render(request, 'exercises_crud/detail-exercise.html', {
        'title': 'Ejercicio en detalle',
        'exercise': exercise,
    })

@login_required(login_url="login")
@has_perm
def showExercises(request):
    try:
        exercises = Exercise.objects.all()
        paginator = Paginator(exercises, 10)

        page = request.GET.get('page')
        page_exercises = paginator.get_page(page)
    except:
        messages.info(request, "Ha ocurrido un error")

    return render(request, 'exercises_crud/list.html', {
        'title': 'Listado de Ejercicios',
        'exercises': page_exercises
    })

@login_required(login_url="login")
@not_trainer
def getUsuarios(request, username):

    try:
        username = request.session['username']
        trainer = User.objects.get(username=username)
        users = User.objects.filter(is_trainer=trainer.email)
    except User.DoesNotExist:
        messages.error(request, "El usuario no existe")
        return redirect('login')
    except Exception:
        return redirect('login')

    return render(request, 'asigned_users.html', {
        'title': 'Usuarios asignados',
        'users': users,
        'usuario': trainer
    })

@login_required(login_url="login")
@not_trainer
def createTraining(request, username):
    client = User.objects.get(username=username)
    trainer = User.objects.get(pk=client.is_trainer)

    if request.method == 'POST':
        form = formTraining(request.POST)
        if form.is_valid():   
            x = form.save(commit=False)
            sql = User.objects.raw(f"SELECT email from user_user where email='{client.email}'") 
            sql1 = User.objects.raw(f"SELECT email from user_user where email='{client.is_trainer}'")    
            x.user = sql[0]
            x.created_by = sql1[0]
            x.save()
            messages.success(request, "Entrenamiento creado")
            return redirect(reverse('asigned-users', kwargs={'username': request.session['username']}))
        
        else:
            return render(request, 'create-training.html',  {
            'title': 'Crear Entrenamiento',
            'form': form,
            'client': client
        })
    else:
        form = formTraining()
        return render(request, 'create-training.html',  {
            'title': 'Crear Entrenamiento',
            'form': form,
            'client': client
        })

@login_required(login_url="login")
@not_trainer
def editTraining(request, id):
    training = get_object_or_404(Training, pk = id)
    user = User.objects.get(email=training.user)
    if request.method == 'POST':
        form = formTraining(request.POST, instance=training)
        if form.is_valid():  
            x = form.save(commit=False)
            sql = User.objects.raw(f"SELECT email from user_user where email='{training.user}'")    
            x.user = sql[0] 
            x.save()
            messages.success(request, "Entrenamiento modificado correctamente")
            return redirect(reverse('list-training', kwargs={'username': user.username}))     
        else:
            form = formTraining(instance=training)
            return render(request, 'edit-training.html',  {
            'title': 'Editar Entrenamiento',
            'form': form,
            'training': training,
            'client': user,
        })
    else:
        form = formTraining(instance=training)
        return render(request, 'edit-training.html',  {
            'title': 'Editar Entrenamiento',
            'form': form,
            'training': training,
            'client': user,
        })

@login_required(login_url="login")
@not_admin
@listT
@notPay
def listTraining(request, username):
    username = get_object_or_404(User, username=username)
    sesion = get_object_or_404(User, username=request.session['username'])
    if sesion.email == username.email:
        entrenamiento = Training.objects.filter(created_by=username.is_trainer, visible=True, user=username.email)
    else:
        entrenamiento = Training.objects.filter(created_by=username.is_trainer, user=username.email)
    return render(request, 'list-trainings.html', {
        'title': f"Entrenamientos de {username.first_name}, {username.last_name}",
        'entrenos': entrenamiento,
        'sesion': sesion,
        'trainer': username.is_trainer,
        'usuario': username
    })
@login_required(login_url="login")
@not_trainer
def generarTrainingPlan(request, username, id):
    client = get_object_or_404(User, username=username)
    ficha = get_object_or_404(Record, userID=client.email)
    training = get_object_or_404(Training, pk=id)
    try:
        delta = datetime.timedelta(days=1)
        dias = []

        while training.fecha_inicio <= training.fecha_fin:
            dias.append(training.fecha_inicio)
            training.fecha_inicio+=delta
    except:
        messages.error(request, 'Ha habido un error')
        return redirect(reverse('list-training', kwargs={'username': client.username}))


     
    return render(request, 'data-training.html', {
        'title': 'Solicitud Datos Entrenamiento',
        'ficha': ficha,
        'client': client,
        'fechas': dias,
        'entreno':training,
    })


@login_required(login_url="login")
@not_trainer
def addExerciseTraining(request, username, id, date):
    client = get_object_or_404(User, username=username)
    training = get_object_or_404(Training, pk=id)
    ejercicios = Exercise.objects.all()
    try:
        if request.method == 'POST':
            form_practice=practiceForm(request.POST)
            if form_practice.is_valid():
                practica = form_practice.save(commit=False)
                sql = User.objects.raw(f"select email, 1 id from user_user where email='{client.email}'")
                sql1 = Training.objects.raw(f"select id, 1 id from training_training where user_id='{client.email}' and id='{training.id}'")
                sql2 = Exercise.objects.raw(f"select id from training_exercise where id='{request.POST['ejercicio']}'")
                practica.user = sql[0]
                practica.training_id = sql1[0]
                practica.day = date
                training.exercise.add(request.POST['ejercicio'])
                practica.exercise = sql2[0]

                reps = request.POST['reps-input']
                stop = request.POST['stop-input']
                print(stop)
                practica.reps = reps
                practica.stop = stop
                cont = 0
                for i in reps:
                    if i == '-':
                        cont+=1
                practica.series = cont
                practica.save()
                messages.success(request, "Ejercicio añadido correctamente")
                return redirect(reverse('data-training', kwargs={'username': username, 'id': training.id}))
            else:
                
                return render(request, 'add-exercise-training.html', {
                'form': form_practice,
                'client': client,
                'entreno': training,
                'fecha': date,
                'ejercicios': ejercicios,
                'title': f'Añadir Ejercicio a {training.name}'

            })
        else:
            form_practice=practiceForm()
            return render(request, 'add-exercise-training.html', {
                'form': form_practice,
                'client': client,
                'entreno': training,
                'fecha': date,
                'ejercicios': ejercicios,
                'title': f'Añadir Ejercicio a {training.name}'

            })
    except:
        messages.error(request, 'Ha habido un problema para ñadir el ejercicio')
        return redirect(reverse('data-training', kwargs={'username':client.username, 'id': training.pk}))

@login_required(login_url="login")
@not_trainer
def deleteTraining(request, username, id):
    usuario = get_object_or_404(User, username=username)
    entreno = get_object_or_404(Training, pk=id, user=usuario.email)
    try:
        entreno.delete()
        messages.success(request, "El entrenamiento ha sido eliminado correctamente")
        return redirect(reverse('list-training', kwargs={'username': username}))
    except:
        messages.warning(request, "No se puede borrar el entrenamiento")
        return redirect(reverse('asigned-users', kwargs={'username': trainer.username}))

@login_required(login_url="login") 
@not_trainer  
def showDayTraining(request, username, id, date):
    usuario = get_object_or_404(User, username=username)
    training = get_object_or_404(Training, pk=id)
    exercises = Practice.objects.filter(user=usuario.email, training_id=training.pk, day=date)
    lista = []
    dictionary = {}
    cont = 0
    for i in exercises:
        cont+=1
        lista.append([i.exercise, i.series, i.stop, i.reps, i.comments, cont, i.id])

    dictionary[date]= lista

    return render(request, 'table/table-training-day.html', {
        'title': f'Entrenamiento día {date}',
        'dictionary': dictionary,
        'client': usuario,
        'entreno': training
    })

@login_required(login_url="login")
@not_admin
@notPay
def showTableTraining(request, username, id):
    client = get_object_or_404(User, username=username)
    training = get_object_or_404(Training, user=client.email, pk=id)
    fechas = []
    delta = datetime.timedelta(days=1)
    dictionary = {}
    lista = []
    count = 0
    while training.fecha_inicio <= training.fecha_fin:
        fechas.append(training.fecha_inicio)
        training.fecha_inicio+=delta

    
    for fecha in fechas:
        data = Practice.objects.filter(user=client.email, training_id=training.pk, day=fecha)
        for i in data:
            count+=1
            lista.append([i.exercise, i.series, i.stop, i.reps, i.comments, count])
    
        dictionary[fecha] = lista
        lista = []
        count = 0

    dict_copy = {**dictionary}
    for k, v in dict_copy.items():
        if not v:
            del dictionary[k]  

    return render(request, 'table/full-training.html', {
        'title': f'Tabla Entrenamiento de {client.first_name}',
        'dictionary': dictionary,
        'client': client,
        'entreno': training
    })



@login_required(login_url="login")
@not_trainer
def deleteExerciseDay(request, username, id, training, date):
    cliente =get_object_or_404(User, username=username)
    pk_training = get_object_or_404(Training, pk = training)
    ejercicio = get_object_or_404(Practice, user=cliente.email, pk=id)
    try:
        ejercicio.delete()
        return redirect(reverse('show-day-training', kwargs={'username': cliente.username, 'id': pk_training.pk, 'date': date}))
    except:
        messages.error(request, 'Ha habido un problema.')
        return redirect(reverse('show-day-training', kwargs={'username': cliente.username, 'id': pk_training.pk, 'date': date}))

@login_required(login_url="login")
@not_admin
@notPay
def exportPDF(request, username, id):
    client = get_object_or_404(User, username=username)
    training = get_object_or_404(Training, user=client.email, pk=id)
    fechas = []
    delta = datetime.timedelta(days=1)
    dictionary = {}
    lista = []
    count = 0
    try:
        while training.fecha_inicio <= training.fecha_fin:
            fechas.append(training.fecha_inicio)
            training.fecha_inicio+=delta

        
        for fecha in fechas:
            data = Practice.objects.filter(user=client.email, training_id=training.pk, day=fecha)
            for i in data:
                count+=1
                lista.append([i.exercise, i.series, i.stop, i.reps, i.comments, count])
        
            dictionary[fecha] = lista
            lista = []
            count = 0
        dict_copy = {**dictionary}
        for k, v in dict_copy.items():
            if not v:
                del dictionary[k]
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=Training' + "_" + str(client.first_name) + "_" + str(client.last_name) + str(training.pk) + '.pdf'
        html_string = render_to_string('table/export-pdf.html',{
            'dictionary': dictionary,
            'client': client,
            'entreno': training
        })

        html = HTML(string=html_string)
        result = html.write_pdf()

        with tempfile.NamedTemporaryFile(delete=False) as output:
            output.write(result)
            output.close()
            output = open(output.name, 'rb')
            response.write(output.read())
    except:
        messages.error(request, 'No se ha podido exportar el entrenamiento a PDF')
        return redirect(reverse('portal', kwargs={'username': request.session['username']}))

    

    return response