

"""

<!-- 

Author: Francisco López Alonso
Creation date: 22/10/2020 14:29
Last Update -

-->

"""

from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path('index_chat/<str:usender>/<str:ureceiver>', views.showChat, name="index-chat"),
    path('index_users/<str:username>', views.showUsers, name="index-users"),  
    path('send_message/<str:usender>/<str:ureceiver>', views.sendMessage, name="send-message"),
]