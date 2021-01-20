from .models import Training, Exercise, Practice
from django.forms import ModelForm
from django import forms
from django.core import validators
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, HTML, Div, Div
from datetime import date
category_exercise = (
    ('Calentamiento', 'Calentamiento'),
    ('Entrenamiento', 'Entrenamiento'),
    ('Estiramiento', 'Estiramiento'),
)

class exerciseForm(forms.ModelForm):
    name = forms.CharField(label = "Nombre", max_length=20, required=True,
    validators=[
        validators.MinLengthValidator(2, 'Título demasiado corto')
    ])
    description = forms.CharField(widget=forms.Textarea())
    categoria = forms.ChoiceField(label="Categoría", choices=category_exercise)
    image = forms.ImageField(label="Imagen (.jpg .png)", required=True)
    video = forms.FileField(label="Video (.mp4)", required=True)
    def __init__(self, *args, **kwargs):
        super(exerciseForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Field('name', css_id='name'),
            Field('description', css_id='description'),
            Field('categoria', css_id='categoria'),
            Field('image', type='file', css_id='image'),
            Field('video', type='file', css_id='video'),
            Submit('submit', 'Enviar'),
        )

    def clean(self):
        super(exerciseForm, self).clean()
        
        video =self.cleaned_data.get('video')

        if video:
            extension = video.name
            print(extension)
            if not extension.endswith('.mp4'):
                self._errors['video'] = self.error_class(['El archivo que ha enviado no es un video o tiene formato incorrecto'])
        return self.cleaned_data
        
    class Meta:
        model=Exercise
        fields=('name', 'description', 'image', 'video', 'categoria')



visible_options = (
    ('0', 'No'),
    ('1', 'Sí'),
)
class formTraining(forms.ModelForm):

    name = forms.CharField(label="Nombre", validators=[validators.MaxLengthValidator(50, 'Nombre demasiado largo'),
                            validators.MinLengthValidator(2, 'Nombre demasiado corto')])
    description = forms.CharField(label="Descripción", widget=forms.Textarea())
    fecha_inicio = forms.DateField(label="Fecha Inicio", widget=forms.SelectDateWidget())
    fecha_fin = forms.DateField(label="Fecha Fin",widget=forms.SelectDateWidget())
    visible = forms.ChoiceField(label="¿Visualizar Dieta?", choices=visible_options)
    class Meta:
        model = Training
        fields = ['name', 'description', 'fecha_inicio', 'fecha_fin', 'visible']


    def clean(self):
        super(formTraining, self).clean()
        
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
        super(formTraining, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Field('name', css_id="css-name"),
            Field('description', css_id="css-description"),
            Field('fecha_inicio', css_id="css-fecha-inicio"),
            Field('fecha_fin', css_id="css-fecha-fin"),
            Field('visible', css_id="css-visible"),
            Submit('submit', 'Enviar')
            
        )

lista = Exercise.objects.all().values_list('id', 'name')
class practiceForm(forms.ModelForm):
    ejercicio = forms.ChoiceField(choices=lista)
    comments = forms.CharField(label= "Comentario Adicionales", widget=forms.Textarea)
    
    class Meta:
        model=Practice
        fields = ['comments']
    

