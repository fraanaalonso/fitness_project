from django import forms
from django.core import validators
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm
from django.contrib.auth import get_user_model
from .models import User, Record, Image
from django.forms import ModelForm
from ckeditor.fields import RichTextFormField
import datetime
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, HTML
from django.contrib.auth.models import Group
from validate_email import validate_email
from localflavor.es.forms import ESIdentityCardNumberField
class registerForm(UserCreationForm):
    email = forms.EmailField(help_text='Required')
    password1 = forms.CharField(help_text='Required')
    password2 = forms.CharField(help_text='Required')
    
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['email', 'password']




class ImageForm(forms.ModelForm):
    description = forms.CharField(label="Descripcion", widget=forms.Textarea(), help_text="Required")
    image = forms.ImageField(
        label= "Foto",
        required="True",
        widget=forms.FileInput(),help_text="Required"

    )
    peso = forms.IntegerField(label="Peso", validators=[validators.RegexValidator(regex="[0-9]", message="Formato no válido")], help_text="Required")
    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('description', type='textarea', css_id='desc-id'),
            Field('image', type='image', css_id='img-id'),
            Field('peso', type='text', css_id='peso-id'),
            Submit('submit', 'Enviar'),
           
        )
    class Meta:
        model = Image
        fields = ['description', 'image', 'peso']
staff_choices = (
        ('1', 'Es Staff'),
        ('0', 'No es Staff')
    )

superuser_choices = (
        ('1', 'Es administrador'),
        ('0', 'No es administrador')
    )

active_choices = (
        ('1', 'Es activo'),
        ('0', 'No es activo')
    )

x = Group.objects.raw("SELECT * FROM auth_group")
group_choices = (
        (x[0].id, 'Administradores'),
        (x[1].id, 'Clientes'),
        (x[2].id, 'Entrenadores')
    )



class editUserForm(ModelForm):
    email = forms.CharField(label= "Email", help_text="Required",
    validators=[
        validators.EmailValidator(message="Formato de E-mail inválido")
    ],
    widget=forms.TextInput(attrs={'class': 'form_control', 'placeholder': 'i.e: abcd@dominio.com', 'readonly': 'readonly'})
    )
    username = forms.CharField(label="Login",help_text="required", max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}),
    validators=[
        
    ])
    is_trainer = forms.ModelChoiceField(label="Entrenador Asignado", required=False,  queryset=User.objects.filter(grupo=3))
    first_name = forms.CharField(label="Nombre",max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}), help_text="Required")
    last_name = forms.CharField(label="Apellidos",max_length=30,  widget=forms.TextInput(attrs={'class': 'form-control'}), help_text="Required")
    active =forms.ChoiceField(label="¿Está activo?", choices=active_choices, required=True, help_text="Required")
    staff = forms.ChoiceField(label="¿Es personal?", choices= staff_choices, required=True, help_text="Required")
    is_superuser = forms.ChoiceField(label="¿Es superusuario?", choices=superuser_choices, required=True, help_text="Required")
    grupo = forms.ChoiceField(label="Grupo de Usuario", choices=group_choices, required=True, help_text="Required")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Field('email', css_id="email"),
            
        )
    
    class Meta:
        model = User
        fields = ['email', 'username', 'is_trainer', 'first_name', 'last_name', 'active', 'staff', 'is_superuser']
        


class addUserForm(ModelForm):
    email = forms.CharField(label= "Email", help_text="Required",
    widget=forms.TextInput(attrs={'class': 'form_control', 'placeholder': 'i.e: abcd@dominio.com'})
    )
    username = forms.CharField(label="Login",help_text="Required", max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Required", validators=[validators.MinLengthValidator(limit_value=8, message='La contraseña no puede tener menos de 8 caracteres')])
    is_trainer = forms.ModelChoiceField(label="Entrenador Asignado",required=False, queryset=User.objects.filter(grupo=3))
    first_name = forms.CharField(label="Nombre",max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}), 
    help_text="Required", validators=[
            validators.RegexValidator(regex="[a-zA-Z]", message="No se admiten caracteres numéricos en el nombre")])
    last_name = forms.CharField(label="Apellidos",max_length=30,  widget=forms.TextInput(attrs={'class': 'form-control'}), 
    help_text="Required", validators=[validators.RegexValidator(regex="[a-zA-Z]", message="No se admiten caracteres numéricos en el nombre")])
    active =forms.ChoiceField(label="¿Está activo?", choices=active_choices, required=True, help_text="Required")
    staff = forms.ChoiceField(label="¿Es personal?", choices= staff_choices, required=True, help_text="Required")
    is_superuser = forms.ChoiceField(label="¿Es superusuario?", choices=superuser_choices, required=True, help_text="Required")
    grupo = forms.ChoiceField(label="Grupo de Usuario", choices=group_choices, required=True, help_text="Required")

    def clean(self):
        super(addUserForm, self).clean()
        
        email =self.cleaned_data.get('email')
        is_valid = validate_email(email)

        if not is_valid:
            self._errors['email'] = self.error_class(['El email no es válido'])
        return self.cleaned_data
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'is_trainer', 'first_name', 'last_name', 'active', 'staff', 'is_superuser', 'password']
        
Country_choices =( 
    ("ES", "España"), 
    ("PO", "Portugal"), 
    ("AL", "Alemania"), 
    ("CO", "Colombia"), 
    ("IT", "Italia"), 
    ("Otro", "Otro")
) 

somatotipe_choices = (
        ('EC', 'Ectomorfo'),
        ('ME', 'Mesomorfo'),
        ('EN', 'Endomorfo')
    )
  
gender_choices = (
        ('Hombre', 'Masculino'),
        ('Mujer', 'Femenino')
    )

today = datetime.date.today()
year = today.year
class editFicha(ModelForm):
    dni = ESIdentityCardNumberField(only_nif=True, help_text="Required")
    phone = forms.CharField(
        label="Teléfono Móvil",
        validators=[
            validators.RegexValidator(regex="^(\d{4})?(-)?\d{3}(-)?\d{3}(-)?\d{3}$", message="No es un número de teléfono válido")
        ],
        widget=forms.TextInput(attrs={'class': 'form-control'}), help_text="Required"
    )
    photo = forms.ImageField(help_text="Required")

    date = forms.DateField(
        label="Fecha de Nacimiento",
        validators=[
            validators.RegexValidator(regex="([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))", message="Formato de fecha inválido"),

        ],
        widget=forms.SelectDateWidget(attrs={'placeholder': 'AAAA-MM-DD', 'class': 'form-control'}, years=range(1940, year)), help_text="Required"
    
    )
    country = forms.ChoiceField(
        label="País",
        choices=Country_choices,
        widget=forms.Select(attrs={'class': 'country_form', 'placeholder': 'País'}), help_text="Required"
    )

    weight = forms.IntegerField(
        label="Peso (kg)",
        validators=[
            validators.RegexValidator("[0-9]", message="Formato erróneo en el peso"),
            validators.MaxValueValidator(limit_value=250, message="Valor de peso no realista"),
            validators.MinValueValidator(limit_value=20, message="Valor de peso no realista"),

        ],
        widget=forms.TextInput(attrs={'class': 'form_control', 'placeholder': 'Peso'}), help_text="Required"
    )

    height = forms.IntegerField(
        label = "Altura (cm)",
        validators=[
            validators.RegexValidator("[0-9]", message="Formato de altura no realista"),
            validators.MaxValueValidator(limit_value=250, message="Valor de altura no realista"),
            validators.MinValueValidator(limit_value=20, message="Valor de altura no realista"),
        ],
        widget=forms.NumberInput(attrs={'class': 'form_control', 'placeholder': 'Altura'}), help_text="Required"


    )

    somatotipe=forms.ChoiceField(
        label="Somatotipo",
        choices=somatotipe_choices,
        widget=forms.Select(attrs={'class': 'form_control'}), help_text="Required"
    )

    gender=forms.ChoiceField(
        label="Género",
        choices=gender_choices, help_text="Required"
    )

    timing = forms.CharField(label="Horarios", widget=forms.Textarea, help_text="Required")
    meals = forms.CharField(label="Comidas",widget=forms.Textarea, help_text="Required")
    sports = forms.CharField(label="Deportes",widget=forms.Textarea, help_text="Required")
    comments = forms.CharField(label="Comentarios Adicionales",widget=forms.Textarea, help_text="Required")
    patologies = forms.CharField(label="Patologías",widget=forms.Textarea, help_text="Required")
   

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
    
    class Meta:
        model = Record
        fields = ['dni', 'phone', 'photo', 'date', 'country', 'weight', 'height', 'somatotipe', 'gender', 'timing','meals', 'patologies', 'sports', 'comments']





class UserRecopilacionForm(forms.ModelForm):

    username = forms.CharField(label="Login",help_text="Required", max_length=20)
    first_name = forms.CharField(label="Nombre",max_length=30,  
    validators=[validators.RegexValidator("[a-zA-Z]", message="El nombre no puede tener formato numérico")], help_text="Required")
    last_name = forms.CharField(label="Apellidos",max_length=30, validators = [validators.RegexValidator("[a-zA-Z]", message="El apellido no puede tener formato numérico")], help_text="Required")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']


class PasswordChangeForm(PasswordChangeForm):
    class Meta:
        fields = ['email', ]

class PasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Field('email', css_id='email', css_name="email"),
            Submit('submit', 'Enviar', css_class="button-reset-pass"),
            HTML('<a class="btn btn-danger" href="{% url "login" %}">Volver</a>')
        )
        self.render_required_fields = True
    class Meta:
        fields = ['email', ]

class PasswordCorfirmForm(forms.Form):
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput(),
        validators=[validators.MinLengthValidator(limit_value=8, message="Contraseña demasiado corta. Mínimo 8 carcateres"),
        ], help_text="Mínimo 8 caracteres")
    password_confirm = forms.CharField(label="Contraseña (confirmación)", widget=forms.PasswordInput(), validators=[validators.MinLengthValidator(limit_value=8, message="Contraseña demasiado corta. Mínimo 8 carcateres"),
        ], help_text="Mínimo 8 caracteres")
    def __init__(self, *args, **kwargs):
        super(PasswordCorfirmForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Field('password', data_name="password-name", id="password-field1", css_class="passwordfields"),
            Field('password_confirm', data_name="password-name-confirm", id="password-field2", css_class="passwordfields"),
            Submit('submit', 'Enviar'),
            HTML('<a class="btn btn-danger" href="{% url "login" %}">Volver</a>'),
            HTML('<input type="hidden" name="uidb64" value="{{uidb64}}"/>'),
            HTML('<input type="hidden" name="token" value="{{token}}"/>'),
            
        )
    class Meta:
        fields = ['password1', 'password2' ]


class editFicha2(ModelForm):
    dni = ESIdentityCardNumberField(only_nif=True)
    phone = forms.CharField(
        label="Teléfono Móvil",
        validators=[
            validators.RegexValidator(regex="^(\d{4})?(-)?\d{3}(-)?\d{3}(-)?\d{3}$", message="No es un número de teléfono válido")
        ],
        widget=forms.TextInput(attrs={'class': 'form-control'}), help_text="Required"
    )
    photo = forms.ImageField(help_text="Required")

    date = forms.DateField(
        label="Fecha de Nacimiento",
        validators=[
            validators.RegexValidator(regex="([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))", message="Formato de fecha inválido"),

        ],
        widget=forms.SelectDateWidget(attrs={'placeholder': 'AAAA-MM-DD', 'class': 'form-control'}, years=range(1940, year)), help_text="Required"
    
    )
    country = forms.ChoiceField(
        label="País",
        choices=Country_choices,
        widget=forms.Select(attrs={'class': 'country_form', 'placeholder': 'País'}), help_text="Required"
    )

    weight = forms.IntegerField(
        label="Peso (kg)",
        validators=[
            validators.RegexValidator("[0-9]", message="Formato erróneo en el peso"),
            validators.MaxValueValidator(limit_value=250, message="Valor de peso no realista"),
            validators.MinValueValidator(limit_value=20, message="Valor de peso no realista"),

        ],
        widget=forms.TextInput(attrs={'class': 'form_control', 'placeholder': 'Peso'}), help_text="Required"
    )

    height = forms.IntegerField(
        label = "Altura (cm)",
        validators=[
            validators.RegexValidator("[0-9]", message="Formato de altura no realista"),
            validators.MaxValueValidator(limit_value=250, message="Valor de altura no realista"),
            validators.MinValueValidator(limit_value=20, message="Valor de altura no realista"),
        ],
        widget=forms.NumberInput(attrs={'class': 'form_control', 'placeholder': 'Altura'}), help_text="Required"


    )

    somatotipe=forms.ChoiceField(
        label="Somatotipo",
        choices=somatotipe_choices,
        widget=forms.Select(attrs={'class': 'form_control'}), help_text="Required"
    )

    gender=forms.ChoiceField(
        label="Género",
        choices=gender_choices, help_text="Required"
    )

    timing = forms.CharField(label="Horarios", widget=forms.Textarea, help_text="Required")
    meals = forms.CharField(label="Comidas",widget=forms.Textarea, help_text="Required")
    sports = forms.CharField(label="Deportes",widget=forms.Textarea, help_text="Required")
    comments = forms.CharField(label="Comentarios Adicionales",widget=forms.Textarea, help_text="Required")
    patologies = forms.CharField(label="Patologías",widget=forms.Textarea, help_text="Required")
    
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
    
    class Meta:
        model = Record
        fields = ['dni', 'phone', 'photo', 'date', 'country', 'weight', 'height', 'somatotipe', 'gender', 'timing','meals', 'patologies', 'sports', 'comments', 'plan']
