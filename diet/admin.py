from django.contrib import admin
from .models import DietType, Diet, Aliment, Meal
# Register your models here.

admin.site.register(Diet)
admin.site.register(DietType)
admin.site.register(Aliment)
admin.site.register(Meal)