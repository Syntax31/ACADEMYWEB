from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from User.models import UserProfile
from django import forms
from django.contrib.auth import password_validation


from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        fields = ['preferencias']

        widgets = {
            'preferencias': forms.TextInput(attrs={'style': 'border: 3px solid purple;height:150px;background-color:black;color:white'}),
        }
        intereses = forms.MultipleChoiceField(
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
    )
    
        
    def clean_dominion(self):
        dominion = self.cleaned_data.get('dominion')
        if dominion < 1 or dominion > 10:
            raise forms.ValidationError("El nivel de dominio debe estar entre 1 y 10.")
        return dominion
        

from django import forms

class SearchGroupForm(forms.Form):
    nombre = forms.CharField(max_length=255, required=False)
    
    from django import forms
from django.contrib.auth.models import User

class SearchUserForm(forms.Form):
    nombre_usuario = forms.CharField(max_length=100, required=False)

from django import forms
from django.contrib.auth.models import User



from django import forms
from django.contrib.auth.models import User

class SearchUserProfileForm(forms.Form):
    nombre_usuario = forms.CharField(max_length=100, required=False)




import re



from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django import forms

class InterestDominionForm(forms.Form):
    interest = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly' }))
    dominion = forms.IntegerField()
    is_checked = forms.BooleanField(required=False)

class CustomUserCreationForm(forms.Form):
    username = forms.CharField(
        label="Nombre de usuario único",
        strip=False,
        help_text="",
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9 ]*',
                message="Ingrese un nombre de usuario válido.",
                code="invalid_username"
            )
        ],
        error_messages={
            'required': 'Este campo es obligatorio.',
        }
    )

    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        error_messages={
            'required': 'Este campo es obligatorio.',
            'invalid': 'Ingrese una dirección de correo electrónico válida.',
        }
    )

    password1 = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text="",
        error_messages={
            'required': 'Este campo es obligatorio.',
        }
    )

    password2 = forms.CharField(
        label="Confirmar Contraseña",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text="",
        error_messages={
            'required': 'Este campo es obligatorio.',
        }
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Este nombre de usuario ya está registrado.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este correo electrónico ya está registrado.")
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if password1 and username and email and (username in password1 or email in password1):
            raise ValidationError("La contraseña es demasiado similar al nombre de usuario o al correo electrónico.")

        # Validación personalizada para la contraseña
        if not re.match(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=!]).{8,}$', password1):
            raise ValidationError(
                "La contraseña debe tener al menos 8 caracteres y contener al menos una mayúscula, un número y un carácter especial (@, #, $, %, ^, &, +, =, !)."
            )

        return password1


    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            raise ValidationError("Las contraseñas no coinciden. Por favor, ingrese las mismas contraseñas en ambos campos.")
        
        

    def save(self):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password1']

        user = User.objects.create_user(username=username, email=email, password=password)
        return user
class BuscarGrupoForm(forms.Form):
    buscar_grupo = forms.CharField(label='Buscar Grupo', required=False, max_length=255)
