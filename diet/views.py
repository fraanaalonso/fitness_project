
from django.shortcuts import render, redirect, HttpResponseRedirect, reverse, HttpResponse, get_object_or_404
from .models import DietType as tipos, Aliment, Meal as comida, Diet, MealUser, AlimentUser
from user.models import User
from django.contrib import messages
from .forms import *
from django.core.paginator import Paginator
import datetime
from datetime import timedelta
from django.db.models import Max
from io import BytesIO
from django.template.loader import get_template
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
import tempfile
from .decorators import *
from django.contrib.auth.decorators import login_required

@login_required(login_url="login")
@has_perm
def mostrarTipos(request, username):
    if request.method == 'POST':
        try:
            getCalories = request.POST.get('oculto')
            login = request.POST.get('usuario')
            types = tipos.objects.all()
            cliente = User.objects.get(username=username)
        except:
            messages.error(request, 'Página no encontrada')
            return redirect('login')

        return render(request, 'tipos/tipos.html', {
            'title': 'Distribución',
            'tipos': types,
            'calorias': getCalories,
            'usuario': login,
            'cliente': cliente,

        })
    else:
        messages.error(request, 'Página no encontrada')
        return redirect('login')
@login_required(login_url="login")
@has_perm
def mostrarTiposAll(request):
    try:
        types = tipos.objects.all()
    except tipos.DoesNotExist:
        messages.error(request, "No hay tipos de dieta registrados")
        return redirect(reverse('portal', kwargs={'username': request.session['username']}))
    return render(request, 'tipos/tipos-all.html', {
        'title': 'Distribución',
        'tipos': types,

    })
@login_required(login_url="login")
@has_perm
def editType(request, id):
    try:
        tipo_dieta = tipos.objects.get(pk=id)
        form = typeDietForm(instance=tipo_dieta)

        if request.method == 'POST':
            form = typeDietForm(request.POST, instance=tipo_dieta)

            if form.is_valid:
                try:
                    form.save()
                    messages.success(request, f"El tipo de dieta {tipo_dieta.name} has sido modificada correctamente")
                    return redirect('tipos-dieta') 
                    
                except:
                    return render(request, 'tipos/edit-tipo.html', {
                            'title': 'Edición Tipo Dieta',
                            'tipo': tipo_dieta,
                            'form': form

                        })


        else:
            return render(request, 'tipos/edit-tipo.html', {
                'title': 'Edición Tipo Dieta',
                'tipo': tipo_dieta,
                'form': form

            })
    except tipos.DoesNotExist:
        messages.error(request, 'El tipo de dieta no existe')
        return redirect('tipos-dieta')
@login_required(login_url="login")
@has_perm
def eraseType(request, id):
    try:
        type_diet = tipos.objects.get(pk=id)
        type_diet.delete()
        messages.warning(request, f'El Tipo de dieta {type_diet.name} ha sido eliminada correctamente')
    except:
        messages.error(request, 'No se ha podido eliminar el tipo de dieta')
        return redirect('tipos-dieta')

    return redirect('tipos-dieta')

@login_required(login_url="login")
@has_perm
def detailTipos(request, id):
    try:
        id_tipos = tipos.objects.get(id=id)
    except:
        messages.error(request, 'El tipo de dieta no existe')
        return redirect('tipos-dieta')
    return render(request, 'tipos/detail-tipos.html', {
        'title': 'Tipos de Dieta',
        'detalle': id_tipos,

    })

@login_required(login_url="login")
@not_admin
@listDietC
@notPay
def listarDieta(request, email):
   
    cliente = get_object_or_404(User, pk=email)
    sesion = User.objects.get(username=request.session['username'])
    if sesion.email == cliente.email:
        dieta = Diet.objects.filter(created_by=cliente.is_trainer, visible=True, user=cliente.email)
    else:
        dieta = Diet.objects.filter(created_by=cliente.is_trainer, user=cliente.email)
    
    return render(request, 'dieta/dietas-user.html', {
        'title': 'Dietas usuario',
        'dietas': dieta,
        'cliente': cliente,
        
    })
    
        

 

@login_required(login_url="login")
@not_trainer
def editDietUser(request, id, email):
    login = User.objects.get(email=email)
    diet = Diet.objects.get(pk=id, user=email)

    if request.method == 'POST':
        form = FormDiet(request.POST, instance=diet)
        if form.is_valid():
            form.save()
            messages.success(
                request, f"Dieta de {login.username} actualizada correctamente")
            return redirect(reverse('listar-dieta', kwargs={'email': login.email}))
        else:
            return render(request, 'dieta/edit-dieta-user.html', {
                'title': f"Dieta de {login.first_name}",
                'form': form,
                'cliente': login.email,
                'diet': diet,
            })
    else:
        form = FormDiet(instance=diet)
        return render(request, 'dieta/edit-dieta-user.html', {
            'title': f"Dieta de {login.first_name}",
            'form': form,
            'cliente': login.email,
            'diet': diet,
        })

@login_required(login_url="login")
@not_admin
@notPay
def detailDiet(request, id, email):
    try:
        login = User.objects.get(email=email)
        dieta = Diet.objects.get(pk=id, user=email)
    except dieta.DoesNotExist:
        return redirect(reverse('listar-dieta', kwargs={'email': login.email}))

    return render(request, 'dieta/detail.html', {
        'dieta': dieta,
        'title': f'Dieta en detalle de {login.first_name}, {login.last_name}',
    
    })
@login_required(login_url="login")
@not_trainer
def deleteDietUser(request, id, email):
    try:
        dieta = Diet.objects.get(pk=id, user=email)
        dieta.delete()
        messages.success(request, f"Dieta {dieta.pk} eliminada correctamente")
        return redirect(reverse('listar-dieta', kwargs={'email': email}))
    except Diet.DoesNotExist:
        return redirect(reverse('listar-dieta', kwargs={'email': email}))

@login_required(login_url="login")
@not_trainer
def planning(request, username, id, calorias):

    tipe = tipos.objects.get(id=id)
    cliente = User.objects.get(username=username)
    tipes = tipos.objects.all()
    hc_user = round((int(tipe.hc_percentage)/100)*calorias, 2)
    pr_user = round((int(tipe.pr_percentage)/100)*calorias, 2)
    gr_user = round((int(tipe.gr_percentage)/100)*calorias, 2)

    if request.method == 'POST':
        
        user = request.POST.get('user')
        name = request.POST.get('name')
        id_usuario = User.objects.raw(f"SELECT email FROM user_user WHERE email='{user}'")
        sesion = User.objects.raw(f"SELECT email FROM user_user WHERE username='{request.session['username']}'")
        type_diet = request.POST.get('type_diet')
        calorias = request.POST.get('calorias')
        visible= request.POST.get('visible')
        id_dieta = tipos.objects.raw(
            f"SELECT id FROM diet_diettype WHERE id='{type_diet}'")
        diet = Diet.objects.create(
            user=id_usuario[0], type_diet=id_dieta[0], calorias=calorias, name=f"Dieta de {cliente.username}", calorias_hc=hc_user, calorias_pr=pr_user, calorias_gr=gr_user, fecha_inicio=date.today(), fecha_fin=date.today(), visible=visible, created_by=sesion[0])
        diet.save()
        messages.success(request, f"Dieta Guardada")
        return redirect(reverse('misUsuarios', kwargs={'username': request.session['username']}))
        
    else:
        return render(request, 'distribucion/distribucion.html', {
            'title': 'Distribución de Macronutrientes',
            'cliente': cliente,
            'tipe': tipe,
            'hc_user': hc_user,
            'pr_user': pr_user,
            'gr_user': gr_user,
            'tipos': tipes,
            'calorias': calorias,
        })

@login_required(login_url="login")
@has_perm
def add_type(request):

    try:
        if request.method == "POST":
            form_add_type = typeDietForm(request.POST)

            if form_add_type.is_valid():
                form_add_type.save()
                messages.success(request, f"El tipo de dieta ha sido creada correctamente")

                return redirect('tipos-dieta')
        else:
            form_add_type = typeDietForm()
    except: 
        messages.error(request, 'No se ha podido añadir la dieta')
        return redirect('tipos-dieta')
    return render(request, 'tipos/add_type.html', {
        'title': 'Añadir Tipo Dieta',
        'form_add_type': form_add_type

    })

@login_required(login_url="login")
@has_perm
def showAliments(request):
    all_aliments = Aliment.objects.all().order_by('name')
    paginator = Paginator(all_aliments, 10)

    page = request.GET.get('page')
    page_aliments = paginator.get_page(page)

    return render(request, 'aliments/list.html', {
        'title': 'Listado de Alimentos',
        'alimentos': page_aliments
    })

@login_required(login_url="login")
@has_perm
def eraseAliment(request, id):
    try:
        aliment = Aliment.objects.get(pk=id)
        aliment.delete()
        messages.warning(request, f'El alimento {aliment.name} ha sido eliminado')
    except Aliment.DoesNotExist:
        messages.warning(request, 'El alimento no existe')
        return redirect('aliments')
    except:
        messages.error(request, 'Ha ocurrido un error')
        return redirect('aliments')

    return redirect('aliments')

@login_required(login_url="login")
@has_perm
def editAliment(request, id):
    try:
        aliment = Aliment.objects.get(pk=id)
        form = editForm(instance=aliment)

        if request.method == 'POST':
            form = editForm(request.POST, instance=aliment)

            if form.is_valid:
                try:
                    aliment = form.save(commit=False)
                    aliment.save()
                    messages.success(request, f"Alimento {aliment.name} modificado correctamente")

                    return redirect('aliments')
                except:
                    return render(request, 'aliments/edit-aliment.html', {
                        'title': 'Edición Alimento',
                        'aliment': aliment,
                        'form': form

                    })

        else:
            return render(request, 'aliments/edit-aliment.html', {
                'title': 'Edición Alimento',
                'aliment': aliment,
                'form': form

            })
    except Aliment.DoesNotExist:
        messages.error(request, 'El alimento no existe')
        return redirect('aliments')
    except:
        messages.error(request, 'Ha ocurrido un error')
        return redirect('aliments')

@login_required(login_url="login")
@has_perm
def addAliment(request):
    try:
        if request.method == "POST":
            form = addForm(request.POST)

            if form.is_valid():
                x = form.save(commit=False)
                x.save()
                messages.success(
                    request, f"Alimento {x.name} creado correctamente")

                return redirect('aliments')
        else:
            form = addForm()
    except:
        messages.error(request, 'Ha ocurrido un error')
        return redirect('aliments')
    return render(request, 'aliments/add-aliment.html', {
        'title': 'Añadir Alimento',
        'form': form

    })

@login_required(login_url="login")
@has_perm
def showMeals(request):
    meals = comida.objects.all()

    paginator = Paginator(meals, 10)

    page = request.GET.get('page')
    page_meals = paginator.get_page(page)

    return render(request, 'meals/list.html', {
        'title': 'Lista de Comidas',
        'meals': page_meals
    })

@login_required(login_url="login")
@has_perm
def add_Meal(request):
    try:
        if request.method == 'POST':
            form = MealForm(request.POST)

            if form.is_valid():

                data = form.save(commit=False)
                data.save()

                messages.success(request, f"Comida añadida correctamente")

                return redirect('meals')

        else:
            form = MealForm()
    except:
        messages.error(request, 'Ha ocurrido en error')
        return redirect('meals')

    return render(request, 'meals/add-meal.html', {
        'title': 'Añadir Comida',
        'form': form
    })

@login_required(login_url="login")
@has_perm
def editMeal(request, id):
    try:
        meal = comida.objects.get(pk=id)
        form = MealForm(instance=meal)

        if request.method == 'POST':
            form = MealForm(request.POST, instance=meal)

            if form.is_valid:
                try:
                    meal = form.save(commit=False)
                    meal.save()
                    messages.success(request, f"La comida {meal.name} ha sido modificada correctamente")
                    return redirect('meals')
                except:
                    return render(request, 'meals/edit-meal.html', {
                        'title': 'Edición Comida',
                        'meal': meal,
                        'form': form

                    })

        else:
            return render(request, 'meals/edit-meal.html', {
                'title': 'Edición Comida',
                'meal': meal,
                'form': form

            })
    except comida.DoesNotExist:
        messages.error(request, 'La comida no existe')
        return redirect('meals')
        
@login_required(login_url="login")
@has_perm
def eraseMeal(request, id):
    try:
        meal = comida.objects.get(pk=id)
        meal.delete()
        messages.warning(request, f'La comida {meal.name} ha sido eliminada correctamente')
    except comida.DoesNotExist:
        messages.error(request, 'La comida no existe')
        return redirect('meals')

    return redirect('meals')

@login_required(login_url="login")
@has_perm
def showMeal(request, id):

    try:
        meal = comida.objects.get(pk=id)
    except comida.DoesNotExist:
        messages.error(request, 'La comida no existe')
        return redirect('meals')

    return render(request, 'meals/detail-meal.html', {
        'meal': meal,
        'title': 'Comida en Detalle'
    })
@login_required(login_url="login")
@not_trainer
def ShowDays(request, id, email):
    try:
        dieta = get_object_or_404(Diet,user=email, pk=id)
        start_date = dieta.fecha_inicio
        end_date = dieta.fecha_fin

        if start_date > end_date: 
            messages.error(request, 'Rango de fechas erróneo')
            return redirect(reverse('listar-dieta', kwargs={'email': email}))
        else:
            delta = datetime.timedelta(days=1)
            fechas = []
            while start_date <= end_date:
                fechas.append(start_date)
                start_date+=delta
    except:
        messages.error(request, 'La petición no es posible')
        return redirect(reverse('portal', kwargs={'username': request.session['username']}))
        
        

    return render(request, 'dieta/show-days.html', {
        'title': 'Dias de la dieta',
        'fechas': fechas,
        'dieta': dieta,
        'size': len(fechas)
    })
    
@login_required(login_url="login")
@not_trainer
def fillDietUser(request, id, email, date):
    diet = get_object_or_404(Diet, pk=id, user=email)
    client = get_object_or_404(User, pk=email)
    try:
        formAlimentUser = AlimentUserForm()
        formMealUser = MealUserForm()
        if request.method == 'POST':
            formMealUser = MealUserForm(request.POST)
            meal_user = comida.objects.raw(f"SELECT id FROM diet_meal WHERE id='{request.POST['comidas-radio']}'")    
            meal_client = User.objects.raw(f"SELECT email FROM user_user WHERE email='{client.email}'")
            meal_diet_id = Diet.objects.raw(f"SELECT id FROM diet_diet WHERE user_id='{client.email}' and id='{diet.id}'")
            if formMealUser.is_valid():
                meal_diet = formMealUser.save(commit=False)
                maxNumberM = MealUser.objects.filter(diet=id, user=email, day=date).aggregate(Max('meal_number'))
                if maxNumberM['meal_number__max'] == None:
                    maxNumberM['meal_number__max'] = 0
                if meal_diet.meal_number >= maxNumberM['meal_number__max'] + 3:
                    messages.error(request, 'El número de comida está fuera de rango')
                    return redirect(reverse('fill-diet', kwargs={'id': diet.id, 'email': diet.user, 'date': date}))
                else:
                    meal_diet.meal = meal_user[0]
                    meal_diet.user = meal_client[0]
                    meal_diet.diet = meal_diet_id[0]
                    meal_diet.day = date
                    meal_diet.save()
                    messages.success(request, 'Comida añadida')
                    return redirect(reverse('fill-diet', kwargs={'id': diet.id, 'email': diet.user, 'date': date}))
            else:
                messages.error(request, "Error")
                comidas = comida.objects.filter().values_list('id', 'name')
                formAlimentUser = AlimentUserForm()
                formMealUser = MealUserForm()
                return render(request, 'dieta/fill-diet.html', {
                    'title': 'Rellenar Dieta',
                    'diet': diet,
                    'formA': formAlimentUser,
                    'formM': formMealUser,
                    'comidas': comidas,
                })
            
        else:
            alimentos = Aliment.objects.all()
            paginator = Paginator(alimentos, 10)
            page= request.GET.get('page')
            page_aliments = paginator.get_page(page)
            comidas = comida.objects.all()
            user_meals = comida.objects.raw(f"SELECT diet_meal.hc_gramos, diet_meal.gr_gramos, diet_meal.pr_gramos, diet_meal.id FROM diet_meal INNER join diet_mealuser on diet_mealuser.meal_id=diet_meal.id AND diet_mealuser.user_id='{client.email}' AND diet_mealuser.diet_id='{diet.pk}' AND diet_mealuser.day='{date}'")
            user_aliments = Aliment.objects.raw(f"SELECT * FROM diet_aliment INNER JOIN diet_alimentuser ON diet_aliment.id=diet_alimentuser.aliment_id and diet_alimentuser.user_id='{client.email}' and diet_alimentuser.diet_id='{diet.pk}' AND diet_alimentuser.day='{date}'")
            hidratos = 0 
            proteinas = 0 
            grasas = 0
            lista_macros = []
            for p in user_meals:
                hidratos = hidratos + int(p.hc_gramos)*4
                proteinas = proteinas + int(p.pr_gramos)*4
                grasas = grasas + int(p.gr_gramos)*9
            for a in user_aliments:
                hidratos = hidratos + (int(float(a.gr_hc)*4))/100*a.gramos
                proteinas = proteinas + (int(float(a.gr_pr)*4))/100*a.gramos
                grasas = grasas + (int(float(a.gr_lip)*4))/100*a.gramos
            lista_macros = [hidratos, proteinas, grasas]
            calorias_dieta = hidratos + proteinas + grasas
            
            return render(request, 'dieta/fill-diet.html', {
                'title': 'Rellenar Dieta',
                'diet': diet,
                'formA': formAlimentUser,
                'formM': formMealUser,
                'comidas': comidas,
                'alimentos': page_aliments,
                'cliente': client,
                'lista_macros':lista_macros,
                'calorias_dieta': calorias_dieta,
                'date': date
            })
    except:
        messages.error(request, 'Ha ocurrido un error')
        return redirect(reverse('show-days', kwargs={'id': diet.pk, 'email':client.email}))


@login_required(login_url="login")
@not_trainer
def fillDietUserAliment(request, id, email, date):
    diet = get_object_or_404(Diet, pk=id, user=email)
    client = get_object_or_404(User, pk=email)
    try:
        if request.method == 'POST':
            formAlimentUser = AlimentUserForm(request.POST)
            aliment_user = Aliment.objects.raw(f"SELECT id FROM diet_aliment WHERE id='{request.POST['alimentos-radio']}'")
            aliment_diet_id = Diet.objects.raw(f"SELECT id FROM diet_diet WHERE user_id='{client.email}' and id='{diet.id}'")
            aliment_client = User.objects.raw(f"SELECT email FROM user_user WHERE email='{client.email}'")

            if formAlimentUser.is_valid():
                aliment_diet = formAlimentUser.save(commit=False)
                maxNumberA = AlimentUser.objects.filter(diet=id, user=email, day=date).aggregate(Max('meal_number'))
                if maxNumberA['meal_number__max'] == None:
                    maxNumberA['meal_number__max'] = 0
                if aliment_diet.meal_number >= maxNumberA['meal_number__max'] + 3:
                    messages.error(request, 'El número de comida está fuera de rango')
                    return redirect(reverse('fill-diet', kwargs={'id': diet.id, 'email': diet.user, 'date': date}))
                else:
                    aliment_diet.aliment = aliment_user[0]
                    aliment_diet.user = aliment_client[0]
                    aliment_diet.diet = aliment_diet_id[0]
                    aliment_diet.day = date
                    aliment_diet.save()
                    messages.success(request, 'Alimento añadido')
                    return redirect(reverse('fill-diet', kwargs={'id': diet.id, 'email': diet.user, 'date': date}))
            else:
                messages.error(request, "Formato erróneo en campo Numero de Comida")
                formAlimentUser = AlimentUserForm()
                formMealUser = MealUserForm()
                alimentos = Aliment.objects.all()
                paginator = Paginator(alimentos, 10)
                page= request.GET.get('page')
                page_aliments = paginator.get_page(page)
                comidas = comida.objects.all()
                user_meals = comida.objects.raw(f"SELECT diet_meal.hc_gramos, diet_meal.gr_gramos, diet_meal.pr_gramos, diet_meal.id FROM diet_meal INNER join diet_mealuser on diet_mealuser.meal_id=diet_meal.id AND diet_mealuser.user_id='{client.email}' AND diet_mealuser.diet_id='{diet.pk}' AND diet_mealuser.day='{date}'")
                user_aliments = Aliment.objects.raw(f"SELECT * FROM diet_aliment INNER JOIN diet_alimentuser ON diet_aliment.id=diet_alimentuser.aliment_id and diet_alimentuser.user_id='{client.email}' and diet_alimentuser.diet_id='{diet.pk}' AND diet_alimentuser.day='{date}'")
                hidratos = 0 
                proteinas = 0 
                grasas = 0
                lista_macros = []
                for p in user_meals:
                    hidratos = hidratos + int(p.hc_gramos)*4
                    proteinas = proteinas + int(p.pr_gramos)*4
                    grasas = grasas + int(p.gr_gramos)*9
                for a in user_aliments:
                    hidratos = hidratos + (int(float(a.gr_hc)*4))/100*a.gramos
                    proteinas = proteinas + (int(float(a.gr_pr)*4))/100*a.gramos
                    grasas = grasas + (int(float(a.gr_lip)*4))/100*a.gramos
                lista_macros = [hidratos, proteinas, grasas]
                calorias_dieta = hidratos + proteinas + grasas
                return render(request, 'dieta/fill-diet.html', {
                        'title': 'Rellenar Dieta',
                        'diet': diet,
                        'formA': formAlimentUser,
                        'formM': formMealUser,
                        'comidas': comidas,
                        'alimentos': page_aliments,
                        'cliente': client,
                        'lista_macros':lista_macros,
                        'calorias_dieta': calorias_dieta,
                        'date': date
                    })
    except:
        messages.error(request, 'Ha ocurrido un error')
        return redirect(reverse('show-days', kwargs={'id': diet.pk, 'email':client.email}))

@login_required(login_url="login")
@not_admin
@notPay
def listCompleteDiet(request, id, email):
    try:
        user = get_object_or_404(User, pk=email)
        dieta = get_object_or_404(Diet, pk=id)
        delta = datetime.timedelta(days=1)
        fechas = []
        list_meals = []
        dictionary1 = {}
        dictionary2 = {}
        max_meal = 0
        meals = []

        while dieta.fecha_inicio <= dieta.fecha_fin:
            fechas.append(dieta.fecha_inicio)
            dieta.fecha_inicio+=delta
        
        for fecha in fechas:
            maxNumberA = AlimentUser.objects.filter(diet=id, user=email, day=fecha).aggregate(Max('meal_number'))
            maxNumberM = MealUser.objects.filter(diet=id, user=email, day=fecha).aggregate(Max('meal_number'))
            meal_diet = comida.objects.raw(f"SELECT day, diet_meal.name, comments, meal_number, diet_mealuser.id, 1 id FROM diet_mealuser INNER JOIN diet_meal ON diet_meal.id=diet_mealuser.meal_id INNER JOIN diet_diet on diet_diet.id=diet_mealuser.diet_id AND diet_mealuser.user_id='{user.email}' AND diet_mealuser.diet_id='{dieta.id}' AND day='{fecha}'")
            aliments_diet = Aliment.objects.raw(f"SELECT day, diet_aliment.name, comments, gramos, meal_number, diet_alimentuser.id, 1 id FROM diet_alimentuser INNER JOIN diet_aliment ON diet_aliment.id=diet_alimentuser.aliment_id INNER JOIN diet_diet on diet_diet.id=diet_alimentuser.diet_id AND diet_alimentuser.user_id='{user.email}' AND diet_alimentuser.diet_id='{dieta.id}' AND day='{fecha}'")
            
            for i in meal_diet:
                list_meals.append([i.name, '-', i.comments, i.meal_number, i.id])
            for j in aliments_diet:
                list_meals.append([j.name, j.gramos, j.comments, j.meal_number, j.id])
            
            if maxNumberA['meal_number__max'] == None:
                maxNumberA['meal_number__max'] = 0
            if maxNumberM['meal_number__max'] == None:
                maxNumberM['meal_number__max'] = 0
            
            if maxNumberA['meal_number__max'] > maxNumberM['meal_number__max']:
                max_meal = maxNumberA['meal_number__max']
            else:
                max_meal = maxNumberM['meal_number__max']
            for number in range(1, max_meal + 1):
                for y in list_meals:
                    if y[3] == number:
                        meals.append(y)
                dictionary1[number] = meals
                meals = []
            dictionary2[fecha]=dictionary1
            list_meals = []
            dictionary1 = {}
            dict_copy = {**dictionary2}
            for k, v in dict_copy.items():
                if not v:
                    del dictionary2[k]
    except:
        messages.error(request, 'La página solicita no está disponible') 
        return redirect('login')

    return render(request, 'dieta/full-diet.html', {
        'title': 'Dieta Completa',
        'dict': dictionary2,
        'cliente': user,
        'dieta': dieta
    })

@login_required(login_url="login")
@not_trainer
def listDietDay(request, id, email, date):
    dieta = get_object_or_404(Diet,pk=id, user=email)
    user = get_object_or_404(User,pk=email)
    meal_day = comida.objects.raw(f"SELECT day, diet_meal.name, comments, meal_number, 1 id FROM diet_mealuser INNER JOIN diet_meal ON diet_meal.id=diet_mealuser.meal_id INNER JOIN diet_diet on diet_diet.id=diet_mealuser.diet_id AND diet_mealuser.user_id='{user.email}' AND diet_mealuser.diet_id='{dieta.id}' AND day='{date}'")
    aliments_day = Aliment.objects.raw(f"SELECT day, diet_aliment.name, comments, gramos, meal_number, 1 id FROM diet_alimentuser INNER JOIN diet_aliment ON diet_aliment.id=diet_alimentuser.aliment_id INNER JOIN diet_diet on diet_diet.id=diet_alimentuser.diet_id AND diet_alimentuser.user_id='{user.email}' AND diet_alimentuser.diet_id='{dieta.id}' AND day='{date}'")
    maxNumberA = AlimentUser.objects.filter(diet=id, user=email, day=date).aggregate(Max('meal_number'))
    maxNumberM = MealUser.objects.filter(diet=id, user=email, day=date).aggregate(Max('meal_number'))
    list_meals = []
    dictionary = {}
    comidas = []
    max_meal = 0

    if maxNumberA['meal_number__max'] == None:
            maxNumberA['meal_number__max'] = 0
    if maxNumberM['meal_number__max'] == None:
        maxNumberM['meal_number__max'] = 0
        
    if maxNumberA['meal_number__max'] > maxNumberM['meal_number__max']:
        max_meal = maxNumberA['meal_number__max']
    else:
        max_meal = maxNumberM['meal_number__max']

    #Lista de listas con las comidas
    for i in meal_day:
        list_meals.append([i.name, 'No procede', i.comments, i.meal_number])
    #lista de listas con los alimentos
    for j in aliments_day:
        list_meals.append([j.name, j.gramos, j.comments, j.meal_number])
    
    for number_meal in range(1, max_meal+1):
        for x in list_meals:
            if x[3] == number_meal:
                comidas.append(x)
        dictionary[number_meal] = comidas
        comidas = []
    return render(request, 'dieta/show-meal-day.html', {
        'date': date,
        'diet': dieta,
        'dict': dictionary


    })
@login_required(login_url="login")
@not_trainer
def erase_meal_diet(request, id):
    try:
        meal = get_object_or_404(MealUser, pk=id)
        meal.delete()
        messages.success(request, f"Día {meal.day}: Alimento de la comida {meal.meal_number} eliminado correctamente")
    except:
        messages.error(request, 'Petición no permitida')
        return redirect('login')
    return redirect(reverse('list-complete', kwargs={'id': meal.diet.id, 'email': meal.user}))

@login_required(login_url="login")
@not_trainer
def erase_aliment_diet(request, id):
    try:
        aliment = get_object_or_404(AlimentUser, pk=id)
        aliment.delete()
        messages.success(request, f"Día {aliment.day}: Alimento de la comida {aliment.meal_number} eliminado correctamente")
    except:
        messages.error(request, 'Petición no permitida')
        return redirect('login')
    return redirect(reverse('list-complete', kwargs={'id': aliment.diet.id, 'email': aliment.user}))
@login_required(login_url="login")
@not_trainer
def edit_meal_diet(request, id):

    meal = get_object_or_404(MealUser, pk=id)
    if request.method == 'POST':
        form = FormEditMealUser(request.POST, instance=meal)
        
        if form.is_valid():
            toret = form.save(commit=False)
            maxNumberM = MealUser.objects.filter(diet=meal.diet, user=meal.user, day=meal.day).aggregate(Max('meal_number'))
            if maxNumberM['meal_number__max'] == None:
                maxNumberM['meal_number__max'] = 0
            if toret.meal_number >= maxNumberM['meal_number__max'] + 2:
                messages.warning(request, 'El número de comida está fuera de rango')
                return render(request, 'dieta/edit-diet-meal.html', {
                'title': 'Editar Comida',
                'form': form,
                'meal': meal
            })
            else:
                toret.user = meal.user
                toret.diet = meal.diet
                toret.save()
                messages.success(request, f'Día {meal.day}: Alimento en comida {meal.meal_number} modificado correctamente')
                return redirect(reverse('list-complete', kwargs={'id': meal.diet.id, 'email': meal.user}))
        else:
            form = FormEditMealUser(instance=meal)
            return render(request, 'dieta/edit-diet-meal.html', {
                'title': 'Editar Comida',
                'form': form,
                'meal': meal
            })

    else:
        form = FormEditMealUser(instance=meal)
        return render(request, 'dieta/edit-diet-meal.html', {
            'title': 'Editar Comida',
            'form': form,
            'meal': meal
        })
@login_required(login_url="login")
@not_trainer
def edit_aliment_diet(request, id):
    meal = get_object_or_404(AlimentUser, pk=id)
    if request.method == 'POST':
        form = FormEditAlimentUser(request.POST, instance=meal)

        if form.is_valid():
            toret = form.save(commit=False)
            maxNumberM = AlimentUser.objects.filter(diet=meal.diet, user=meal.user, day=meal.day).aggregate(Max('meal_number'))
            if maxNumberM['meal_number__max'] == None:
                maxNumberM['meal_number__max'] = 0
            if toret.meal_number >= maxNumberM['meal_number__max'] + 2:
                form = FormEditAlimentUser(instance=meal)
                messages.warning(request, 'El número de comida está fuera de rango')
                return render(request, 'dieta/edit-diet-aliment.html', {
                'title': 'Editar Comida',
                'form': form,
                'meal': meal
            })
            else:
                toret.user = meal.user
                toret.diet = meal.diet
                toret.save()
                messages.success(request, f'Día {meal.day}: Alimento en comida {meal.meal_number} modificado correctamente')
                return redirect(reverse('list-complete', kwargs={'id': meal.diet.id, 'email': meal.user}))
        else:
            form = FormEditAlimentUser(instance=meal)
            return render(request, 'dieta/edit-diet-aliment.html', {
                'title': 'Editar Comida',
                'form': form,
                'meal': meal
            })

    else:
        form = FormEditAlimentUser(instance=meal)
        return render(request, 'dieta/edit-diet-aliment.html', {
            'title': 'Editar Comida',
            'form': form,
            'meal': meal
        })
@login_required(login_url="login")
@not_admin
@notPay
def export_pdf(request, id):
    dieta = get_object_or_404(Diet, pk=id)
    client = get_object_or_404(User, email=dieta.user)
    try:
        delta = datetime.timedelta(days=1)
        fechas = []
        list_meals = []
        dictionary1 = {}
        dictionary2 = {}
        max_meal = 0
        meals = []

        while dieta.fecha_inicio <= dieta.fecha_fin:
            fechas.append(dieta.fecha_inicio)
            dieta.fecha_inicio+=delta
        
        for fecha in fechas:
            maxNumberA = AlimentUser.objects.filter(diet=id, user=dieta.user, day=fecha).aggregate(Max('meal_number'))
            maxNumberM = MealUser.objects.filter(diet=id, user=dieta.user, day=fecha).aggregate(Max('meal_number'))
            meal_diet = comida.objects.raw(f"SELECT day, diet_meal.name, comments, meal_number, diet_mealuser.id, 1 id FROM diet_mealuser INNER JOIN diet_meal ON diet_meal.id=diet_mealuser.meal_id INNER JOIN diet_diet on diet_diet.id=diet_mealuser.diet_id AND diet_mealuser.user_id='{dieta.user}' AND diet_mealuser.diet_id='{dieta.id}' AND day='{fecha}'")
            aliments_diet = Aliment.objects.raw(f"SELECT day, diet_aliment.name, comments, gramos, meal_number, diet_alimentuser.id, 1 id FROM diet_alimentuser INNER JOIN diet_aliment ON diet_aliment.id=diet_alimentuser.aliment_id INNER JOIN diet_diet on diet_diet.id=diet_alimentuser.diet_id AND diet_alimentuser.user_id='{dieta.user}' AND diet_alimentuser.diet_id='{dieta.id}' AND day='{fecha}'")
            
            for i in meal_diet:
                list_meals.append([i.name, '-', i.comments, i.meal_number, i.id])
            for j in aliments_diet:
                list_meals.append([j.name, j.gramos, j.comments, j.meal_number, j.id])
            
            if maxNumberA['meal_number__max'] == None:
                maxNumberA['meal_number__max'] = 0
            if maxNumberM['meal_number__max'] == None:
                maxNumberM['meal_number__max'] = 0
            
            if maxNumberA['meal_number__max'] > maxNumberM['meal_number__max']:
                max_meal = maxNumberA['meal_number__max']
            else:
                max_meal = maxNumberM['meal_number__max']
            for number in range(1, max_meal + 1):
                for y in list_meals:
                    if y[3] == number:
                        meals.append(y)
                dictionary1[number] = meals
                meals = []
            dictionary2[fecha]=dictionary1
            list_meals = []
            dictionary1 = {}
        
        dict_copy = {**dictionary2}
        for k, v in dict_copy.items():
            if not v:
                del dictionary2[k]

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=Diet' + "_" + str(client.first_name) + "_" + str(client.last_name) + str(dieta.pk) + '.pdf'
        html_string = render_to_string('dieta/export-pdf.html',{
            'dict': dictionary2,
            'client': client,
        })

        html = HTML(string=html_string)
        result = html.write_pdf()

        with tempfile.NamedTemporaryFile(delete=False) as output:
            output.write(result)
            output.close()
            output = open(output.name, 'rb')
            response.write(output.read())
    except:
        messages.error(request, 'No se ha podido exportar la dieta a pdf')
        return redirect(reverse('listar-dieta', kwargs={'email': client.email}))
    

    return response