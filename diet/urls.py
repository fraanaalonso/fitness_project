

"""

<!-- 

Author: Francisco López Alonso
Creation date: 18/10/2020 14:29
Last Update -

-->

"""

from django.urls import path, register_converter
from django.conf import settings
from . import views
from datetime import datetime
import datetime
class DateConverter:
    regex = '\d{4}-\d{2}-\d{2}'

    def to_python(self, value):
        return datetime.datetime.strptime(value, '%Y-%m-%d').date()

    def to_url(self, value):
        return str(value)

register_converter(DateConverter, 'yyyy')


urlpatterns = [
    path('tipos_dieta/<str:username>', views.mostrarTipos, name="tipos-dieta"),
    path('tipos_dieta/', views.mostrarTiposAll, name="tipos-dieta"),
    path('detail_tipos/<int:id>', views.detailTipos, name="detail-tipos"),
    path('planning_diet/<str:username>/<int:id>/<int:calorias>',
         views.planning, name="planning"),
    path('add_type/', views.add_type, name="add-type"),
    path('aliments/', views.showAliments, name="aliments"),
    path('aliments-edit/<int:id>', views.editAliment, name="edit-aliment"),
    path('aliments-erase/<int:id>', views.eraseAliment, name="erase-aliment"),
    path('aliments-add/', views.addAliment, name="aliments-add"),
    path('type-edit/<int:id>', views.editType, name="edit-type"),
    path('type-erase/<int:id>', views.eraseType, name="erase-type"),
    path('meals/', views.showMeals, name="meals"),
    path('meal-edit/<int:id>', views.editMeal, name="edit-meal"),
    path('meal-erase/<int:id>', views.eraseMeal, name="erase-meal"),
    path('meal-show/<int:id>', views.showMeal, name="show-meal"),
    path('meal-add/', views.add_Meal, name="add-meal"),
    path('listar_dieta/<str:email>', views.listarDieta, name="listar-dieta"),
    path('edit_diet_user/<int:id>/<str:email>',
         views.editDietUser, name="edit-diet-user"),
    path('detail_diet/<int:id>/<str:email>',
         views.detailDiet, name="detail-diet"),
    path("erase_diet_user/<int:id>/<str:email>",
         views.deleteDietUser, name="erase-diet-user"),
    path("fill_diet/<int:id>/<str:email>/<yyyy:date>/", views.fillDietUser, name="fill-diet"),
    path("fill_diet_aliment/<int:id>/<str:email>/<yyyy:date>/", views.fillDietUserAliment, name="fill-diet-aliment"),
    path("show_days/<int:id>/<str:email>", views.ShowDays, name="show-days"),
    path('diet_day/<int:id>/<str:email>/<yyyy:date>/', views.listDietDay, name="list-diet-day"),
    path('diet_complete/<int:id>/<str:email>', views.listCompleteDiet, name="list-complete"),
    path('diet_pdf/<int:id>', views.export_pdf, name="diet-pdf"),
    path('erase_meal_diet/<int:id>/', views.erase_meal_diet, name="erase-meal-diet"),
    path('erase_aliment_diet/<int:id>/', views.erase_aliment_diet, name="erase-aliment-diet"),
    path('edit_meal_diet/<int:id>/', views.edit_meal_diet, name="edit-meal-diet"),
    path('edit_aliment_diet/<int:id>/', views.edit_aliment_diet, name="edit-aliment-diet"),
]
