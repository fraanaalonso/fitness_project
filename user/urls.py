
"""

<!-- 

Author: Francisco López Alonso
Creation date: 23/09/2020 18:39
Last Update -

-->

"""

from django.urls import path
from django.conf import settings
from . import views
from fitness_project import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('registro/', views.registerApp, name="register"),
    path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name="activate"),
    path('login/', views.LoginApp, name='login'),
    path('logout/', views.logoutApp, name="logout"),
    path('reset_password/', views.reset_password, name="password_reset"), #form para poner el email
    path('reset_password/done/', views.pasword_done, name="password-done"), #form con instrucciones sobre el link enviado
    path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', views.password_reset_complete, name='password_reset_complete'),
    path('user_erase/<str:email>', views.eraseUser, name="user-erase"),
    path('user_edit/<str:email>', views.editUser, name="user-edit"),
    path('portal/<str:username>', views.portal, name='portal'),
    path('show-Users/', views.showUsers, name="show-users"),
    path('recopilacion/<str:email>', views.recopilacion, name="recopilacion"),
    path('seleccionaPago/<str:email>', views.seleccionarTarifa, name="tarifas"),
    path('misUsuarios/<str:username>', views.getUsuarios, name="misUsuarios"),
    path('detalle/<str:email>', views.userDetail, name="detalle"),
    path('calculate/<str:username>', views.calculate, name="calculate"),
    path('misFotos/<str:username>', views.misFotos, name="mis-fotos"),
    path('add_Photo/<str:username>', views.upload_image, name="add-photo"),
    path('delete_img/<str:username>/<int:id>', views.deleteImage, name="delete-image"),
    path('detail_img/<str:username>/<int:id>', views.detailImage, name="detail-image"),
    path('groups/', views.showGroups, name="show-groups"),
    path('user_groups/<int:id>', views.userGroups, name="user-groups"),
    path('erase_group/<int:id>', views.eraseGroup, name="erase-group"),
    path('reset_password/<str:username>', views.passChangeView, name="reset-password"),
    path('user_add/', views.addUser, name="user-add"),


]

#Conf para cargar ficheros creando una ruta para ellos
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    