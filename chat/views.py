from django.shortcuts import render, redirect, reverse
from user.models import User, Record
from .models import Chat
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import *
# Create your views here.
@login_required(login_url="login")
@mixChat
def showUsers(request, username):

    try:
        sesion = User.objects.get(username=username)
        photos = {}
        
        if sesion.grupo.id == 1:
            client = User.objects.filter(grupo=3)
            
        elif sesion.grupo.id == 3:       
            client = User.objects.filter(is_trainer=sesion.email)
        
        if sesion.grupo.id == 3 or sesion.grupo.id == 1:
            for i in client:
                photo = Record.objects.get(userID=i.email)
                photos[i] = photo

        if sesion.grupo.id == 2:
            client = User.objects.get(email=sesion.is_trainer)
            photo = Record.objects.get(userID=client.email)
            photos[client] = photo

        return render(request, 'chat/index-users.html', {
            'title': 'Sala',
            'clients':photos,
            'sesion': sesion,
        })
    except: 
        messages.error(request, 'Espera a que te asignen un entrenador para hacer uso del chat')
        return redirect('login')


@login_required(login_url="login")
def showChat(request, usender, ureceiver):
    try:
        usender = request.session['username']
        emisor = User.objects.get(username=usender)
        receptor = User.objects.get(username=ureceiver)
        mensajes = []
        content = []
        photos = {}
        client = User.objects.filter(is_trainer=emisor.email)

        if emisor.grupo.id == 1:
            client = User.objects.filter(grupo=3)
            
        elif emisor.grupo.id == 3:       
            client = User.objects.filter(is_trainer=emisor.email)
        
        if emisor.grupo.id == 3 or emisor.grupo.id == 1:
            for i in client:
                photo = Record.objects.get(userID=i.email)
                photos[i] = photo

        if emisor.grupo.id == 2:
            client = User.objects.get(email=emisor.is_trainer)
            photo = Record.objects.get(userID=client.email)
            photos[client] = photo


        r_user = Record.objects.get(userID=receptor.email)
        e_user = Record.objects.get(userID=emisor.email)
        query1 = Chat.objects.filter((Q(emisor=emisor.email) & Q(receptor=receptor.email)) | (Q(emisor=receptor.email) & Q(receptor=emisor.email))).order_by('date')


        for j in query1:
            if str(j.emisor) == emisor.email:
                mensajes.append([j.date, j.content, '1'])
            else:
                mensajes.append([j.date, j.content, '2'])


        return render(request, 'chat/index-chat.html', {
            'title': 'Sala',
            'clients':photos,
            'receptor': receptor,
            'r_user': r_user,
            'e_user': e_user,
            'sesion':emisor,
            'mensajes': mensajes,
            'path': request.path,
        })
    except: 
        messages.error(request, 'Ha ocurrido un error con el Chat')
        return redirect('login')

@login_required(login_url="login")
def sendMessage(request, usender, ureceiver):
    try:
        sender = User.objects.get(username=usender)
        receiver = User.objects.get(username=ureceiver)
        sql = User.objects.raw(f"SELECT email from user_user where username='{usender}'")
        sql1 = User.objects.raw(f"SELECT email from user_user where username='{ureceiver}'")
        content_chat = request.POST['content-chat']
        if request.method == 'POST':
            chat = Chat.objects.create(emisor=sql[0], receptor=sql1[0], content=content_chat)
            chat.save()

            return redirect(reverse('index-chat', kwargs={'usender': sender.username, 'ureceiver': receiver.username}))
    except:
        messages.error(request, 'No se ha podido enviar el mensaje')
        return redirect(reverse('index-users', kwargs={'username': request.session['username']}))
    

