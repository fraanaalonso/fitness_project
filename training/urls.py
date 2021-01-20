

"""

<!-- 

Author: Francisco López Alonso
Creation date: 02/11/2020 21:17
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
    path('detail_exercise/<int:id>', views.detailExercise, name="detail-exercise"),
    path('add_exercise/', views.addExercise, name="add-exercise"),
    path('edit_exercise/<int:id>', views.editExercise, name="edit-exercise"),
    path('delete_exercise/<int:id>', views.deleteExercise, name="delete-exercise"),
    path('show_exercises/', views.showExercises, name="show-exercises"),
    path('asigned_users/<str:username>', views.getUsuarios, name="asigned-users"),
    path('create_training/<str:username>', views.createTraining, name="create-training"),
    path('data_training/<str:username>/<int:id>', views.generarTrainingPlan, name="data-training"),
    path('add_exercise_training/<str:username>/<int:id>/<yyyy:date>/', views.addExerciseTraining, name="add-exercise-training"),
    path('list_training/<str:username>', views.listTraining, name="list-training"),
    path('delete-training/<str:username>/<int:id>', views.deleteTraining, name="delete-training"),
    path('edit-training/<int:id>', views.editTraining, name="edit-training"),
    path('show-day-training/<str:username>/<int:id>/<yyyy:date>/', views.showDayTraining, name="show-day-training"),
    path('show_training/<str:username>/<int:id>', views.showTableTraining, name="show-training"),
    path('delete_exercise_day/<str:username>/<int:id>/<int:training>/<yyyy:date>/', views.deleteExerciseDay, name="delete-exercise-day"),
    path('export_pdf/<str:username>/<int:id>', views.exportPDF, name="export-pdf"),
]