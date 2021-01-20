
"""

<!-- 

Author: Francisco López Alonso
Creation date: 23/09/2020 18:39
Last Update -

-->

"""

from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('inicio/', views.index, name="inicio"),
]