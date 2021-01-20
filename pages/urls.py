
"""

<!-- 

Author: Francisco López Alonso
Creation date: 24/09/2020 11:46
Last Update -

-->

"""

from django.urls import path

from . import views

urlpatterns = [
    path('pagina/<str:slug>', views.page, name='page')
]