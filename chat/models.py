from django.db import models
from user.models import User

class Chat(models.Model):
    emisor = models.ForeignKey(User, verbose_name="Emisor", on_delete=models.CASCADE, related_name="Usuario emisor+")
    receptor = models.ForeignKey(User, verbose_name="Receptor", on_delete=models.CASCADE, related_name="Usuario receptor+")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Fecha mensaje")
    content = models.CharField(verbose_name="Contenido", max_length=200)

    
    class Meta:
        verbose_name = "Chat"
        verbose_name_plural = "Chats"
