from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Record, Tariff


class UserAdmin(admin.ModelAdmin):
    list_display=('email',)  


admin.site.register(User, UserAdmin)
admin.site.register(Record)
admin.site.register(Tariff)