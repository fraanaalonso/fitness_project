
"""

<!-- 

Author: Francisco López Alonso
Creation date: 02/10/2020 18:39
Last Update -

-->

"""

from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path('pago/<int:id>/<str:email>', views.view_pago, name="pago"),
    path('complete/', views.complete, name="complete"),
    path('thanks/<str:username>/<int:id_tarifa>', views.thanks, name='thanks'),
]