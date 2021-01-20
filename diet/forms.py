from .models import Aliment, DietType, Meal, Diet, MealUser, AlimentUser
from django.forms import ModelForm
from django import forms
from django.core import validators
from django.core.validators import validate_email
import datetime
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from django.db.models import Max
from datetime import date
class editForm(ModelForm):
    name = forms.CharField(
        label="Nombre",
        max_length=40,
        required=True,

        validators=[
            validators.MinLengthValidator(2, 'El titulo es demasiado corto')
        ]
    )

    kcal_hundred_gr = forms.CharField(
        label="Kcal 100 Gramos",

        validators=[
            validators.MaxLengthValidator(
                6, 'Te has pasado, has puesto demasiado texto'),
            validators.MinValueValidator(str(1), "No puede ser 0"),
            validators.RegexValidator(
                regex="[0-9]", message="Debes introducir un número entero o decimal"),

        ]
    )

    gr_hc = forms.CharField(
        label="Gramos Hidratos de Carbono",

        validators=[
            validators.MaxLengthValidator(
                6, 'Te has pasado, has puesto demasiado texto'),
            validators.MinValueValidator(str(0), "No puede ser negativo"),
            validators.RegexValidator(
                regex="^[0-9]\d*(\.\d+)?$", message="Debes introducir un número entero o decimal"),
        ]
    )

    gr_pr = forms.CharField(
        label="Gramos Proteínas",

        validators=[
            validators.MaxLengthValidator(
                6, 'Te has pasado, has puesto demasiado texto'),
            validators.MinValueValidator(str(0), "No puede ser negativo"),
            validators.RegexValidator(
                regex="^[0-9]\d*(\.\d+)?$", message="Debes introducir un número entero o decimal"),
        ]
    )

    gr_lip = forms.CharField(
        label="Gramos Grasas",

        validators=[
            validators.MaxLengthValidator(
                6, 'Te has pasado, has puesto demasiado texto'),
            validators.MinValueValidator(str(0), "No puede ser negativo"),
            validators.RegexValidator(
                regex="^[0-9]\d*(\.\d+)?$", message="Debes introducir un número entero o decimal"),
        ]
    )

    class Meta:
        model = Aliment
        fields = ['name', 'kcal_hundred_gr', 'gr_hc', 'gr_pr', 'gr_lip']


class addForm(forms.ModelForm):

    name = forms.CharField(
        label="Nombre",
        max_length=40,
        required=True,

        validators=[
            validators.MinLengthValidator(2, 'El titulo es demasiado corto')

        ]
    )

    kcal = forms.CharField(
        label="Kcal 100 Gramos",

        validators=[
            validators.MaxLengthValidator(
                6, 'Te has pasado, has puesto demasiado texto'),
            validators.MinValueValidator(str(1), "No puede ser 0"),
            validators.RegexValidator(
                regex="[0-9]", message="Debes introducir un número entero o decimal"),

        ]
    )

    gr_hc = forms.CharField(
        label="Gramos Hidratos de Carbono",

        validators=[
            validators.MaxLengthValidator(
                6, 'Te has pasado, has puesto demasiado texto'),
            validators.MinValueValidator(str(0), "No puede ser negativo"),
            validators.RegexValidator(
                regex="^[0-9]\d*(\.\d+)?$", message="Debes introducir un número entero o decimal"),
        ]
    )

    gr_pr = forms.CharField(
        label="Gramos Proteínas",

        validators=[
            validators.MaxLengthValidator(
                6, 'Te has pasado, has puesto demasiado texto'),
            validators.MinValueValidator(str(0), "No puede ser negativo"),
            validators.RegexValidator(
                regex="^[0-9]\d*(\.\d+)?$", message="Debes introducir un número entero o decimal"),
        ]
    )

    gr_lip = forms.CharField(
        label="Gramos Grasas",

        validators=[
            validators.MaxLengthValidator(
                6, 'Te has pasado, has puesto demasiado texto'),
            validators.MinValueValidator(str(0), "No puede ser negativo"),
            validators.RegexValidator(
                regex="^[0-9]\d*(\.\d+)?$", message="Debes introducir un número entero o decimal"),
        ]
    )

    class Meta:
        model = Aliment
        fields = '__all__'


class typeDietForm(forms.ModelForm):
    name = forms.CharField(
        label="Nombre",
        max_length=40,
        required=True,
        help_text="Required",
        validators=[
            validators.MinLengthValidator(2, 'El titulo es demasiado corto')
        ]
    )

    description = forms.CharField(
        label="Descripcion",
        help_text="Required",
        validators=[
            validators.MinLengthValidator(
                3, 'La descripción es demasiado corta')


        ]
    )

    hc_percentage = forms.CharField(
        label="% Hidratos de Carbono",
        help_text="Required",
        validators=[
            validators.MaxLengthValidator(2, 'Porcentaje no realista'),
            validators.MinValueValidator(str(0), "No puede ser negativo"),
            validators.RegexValidator(
                regex="^[1-9]\d*(\.\d+)?$", message="Debes introducir un número entero o decimal"),

        ]
    )

    pr_percentage = forms.CharField(
        label="% Proteinas",
        help_text="Required",
        validators=[
            validators.MaxLengthValidator(2, 'Porcentaje no realista'),
            validators.MinValueValidator(str(0), "No puede ser negativo"),
            validators.RegexValidator(
                regex="^[1-9]\d*(\.\d+)?$", message="Debes introducir un número entero o decimal"),

        ]
    )

    gr_percentage = forms.CharField(
        label="% Lipidos",
        help_text="Required",
        validators=[
            validators.MaxLengthValidator(2, 'Porcentaje no realista'),
            validators.MinValueValidator(str(0), "No puede ser negativo"),
            validators.RegexValidator(
                regex="^[1-9]\d*(\.\d+)?$", message="Debes introducir un número entero o decimal"),

        ]
    )

    class Meta:
        model = DietType
        fields = '__all__'


class MealForm(forms.ModelForm):

    name = forms.CharField(help_text="Required", label="Nombre", validators=[
        validators.MinLengthValidator(1, message="Nombre demasiado corto")

    ])

    description = forms.CharField(widget=forms.Textarea())

    hc_gramos = forms.CharField(
        label="Gramos Hidratos de Carbono",

        validators=[
            validators.MaxLengthValidator(
                6, 'Te has pasado, has puesto demasiado texto'),
            validators.MinValueValidator(str(0), "No puede ser negativo"),
            validators.RegexValidator(
                regex="^[0-9]\d*(\.\d+)?$", message="Debes introducir un número entero"),
        ]
    )

    pr_gramos = forms.CharField(
        label="Gramos Proteínas",

        validators=[
            validators.MaxLengthValidator(
                6, 'Te has pasado, has puesto demasiado texto'),
            validators.MinValueValidator(str(0), "No puede ser negativo"),
            validators.RegexValidator(
                regex="^[0-9]\d*(\.\d+)?$", message="Debes introducir un número entero"),
        ]
    )

    gr_gramos = forms.CharField(
        label="Gramos Grasas",

        validators=[
            validators.MaxLengthValidator(
                6, 'Te has pasado, has puesto demasiado texto'),
            validators.MinValueValidator(str(0), "No puede ser negativo"),
            validators.RegexValidator(
                regex="^[0-9]\d*(\.\d+)?$", message="Debes introducir un número entero"),
        ]
    )

    class Meta:
        model = Meal
        fields = '__all__'




visible_options = (
    ('0', 'No'),
    ('1', 'Sí'),
)

class FormDiet(forms.ModelForm):

    calorias = forms.CharField(label="Calorias",
                               validators=[validators.RegexValidator(
                                   regex="[0-9]", message="Formato incorrecto"), ]
                               )
    name = forms.CharField(label="Nombre", validators=[validators.MaxLengthValidator(limit_value=20, message="Nombre demasiado largo"),
                                                       validators.MinLengthValidator(limit_value=2, message="Nombre demasiado corto")])
    description =  forms.CharField(label="Descripción", widget=forms.Textarea, empty_value=True)
    fecha_inicio = forms.DateField(
        label="Fecha Inicio",
        widget=forms.SelectDateWidget())
    fecha_fin = forms.DateField(
        label="Fecha Fin",
        widget=forms.SelectDateWidget())

    visible = forms.ChoiceField(label="¿Visualizar Dieta?", choices=visible_options)
    
    
    
    class Meta:
        model = Diet
        fields = ['name', 'description', 'calorias', 'fecha_inicio', 'fecha_fin', 'visible']     

    
    def clean(self):
        super(FormDiet, self).clean()
        
        fecha_inicio =self.cleaned_data.get('fecha_inicio')
        fecha_fin = self.cleaned_data.get('fecha_fin')
        delta = fecha_fin-fecha_inicio
        if fecha_inicio >= fecha_fin:
            self._errors['fecha_inicio'] = self.error_class([''])
            self._errors['fecha_fin'] = self.error_class(['Rango de fechas erróneo'])
        if delta.days > 14:
            self._errors['fecha_inicio'] = self.error_class([''])
            self._errors['fecha_fin'] = self.error_class(['Rango de fechas demasiado grande'])

        if fecha_inicio < date.today():
            self._errors['fecha_inicio'] = self.error_class(['La fecha de inicio corresponde a una fecha ya pasada'])
        
        if fecha_fin < date.today():
            self._errors['fecha_fin'] = self.error_class(['La fecha de fin corresponde a una fecha ya pasada'])
        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super(FormDiet, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Field('name', css_id="name"),
            Field('calorias', css_id="calorias"),
            Field('description', css_id="description"),
            Field('fecha_inicio', css_id="fechaI"),
            Field('fecha_fin', css_id="fechaF"),
            Field('visible', css_id="visible"),
            Submit('submit', 'Enviar')
            
        )
        self.render_required_fields = True

today = datetime.date.today()
year = today.year



class MealUserForm(forms.ModelForm):
    meal_number = forms.IntegerField(label="Numero de Comida", 
    validators=[validators.RegexValidator(regex="[0-9]", message="Formato erróneo"),
    ])
    comments =  forms.CharField(label="Comentarios Adicionales", widget=forms.Textarea)

    class Meta:
        model = MealUser
        fields = ['comments', 'meal_number']

class AlimentUserForm(forms.ModelForm):
    meal_number = forms.IntegerField(label="Numero de Comida", 
    validators=[validators.RegexValidator(regex="[0-9]", message="Formato erróneo"),
    ])
    gramos = forms.CharField(
        validators=[validators.RegexValidator(regex="[0-9]", message="Formato inválido"),]
    )
    comments =  forms.CharField(label="Comentarios Adicionales", widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

    class Meta:
        model = AlimentUser
        fields = ['gramos', 'comments', 'meal_number']


class FormEditMealUser(forms.ModelForm):
    meal_number = forms.IntegerField(label="Numero de Comida", 
    validators=[validators.RegexValidator(regex="[0-9]", message="Formato erróneo"),
    ])
    comments =  forms.CharField(label="Comentarios Adicionales", widget=forms.Textarea)
    def __init__(self, *args, **kwargs):
        super(FormEditMealUser, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Field('meal', css_id="meal-name"),
            Field('comments', css_id="comments"),
            Field('day', css_id="day", readonly='readonly'),
            Field('meal_number', css_id="meal-number"),
            Submit('submit', 'Enviar')
            
        )


    class Meta:
        model = MealUser
        fields = ['meal', 'day', 'comments', 'meal_number']

class FormEditAlimentUser(forms.ModelForm):
    meal_number = forms.IntegerField(label="Numero de Comida", 
    validators=[validators.RegexValidator(regex="[0-9]", message="Formato erróneo"),
    ])
    gramos = forms.CharField(
        validators=[validators.RegexValidator(regex="[0-9]", message="Formato inválido"),]
    )
    comments =  forms.CharField(label="Comentarios Adicionales", widget=forms.Textarea)
    def __init__(self, *args, **kwargs):
        super(FormEditAlimentUser, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Field('aliment', css_id="meal-name"),
            Field('gramos', css_id="gramos"),
            Field('comments', css_id="comments"),
            Field('day', css_id="day", readonly='readonly'),
            Field('meal_number', css_id="meal-number"),
            Submit('submit', 'Enviar')
            
        )
    
    class Meta:
        model = AlimentUser
        fields = ['aliment', 'day', 'comments', 'gramos', 'meal_number']