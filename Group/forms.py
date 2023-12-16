from django import forms
from .models import Group,GroupInvitation

class GroupCreationForm(forms.ModelForm):
    nombre = forms.CharField(
        label='Nombre del Grupo',
        max_length=100,
        widget=forms.TextInput(attrs={
            'style': 'border: 2px solid purple; width: 100%; padding: 5px;border-radius:15px;background-color:black;color:white',
            'placeholder': 'Nombre del Grupo que crearas'
        })
    )
    descripcion = forms.CharField(
        label='Descripción',
        widget=forms.Textarea(attrs={
            'style': 'border: 2px solid purple; width: 100%; padding: 5px;background-color:black;color:white',
            'rows': 3,
            'placeholder': 'Una breve descripción del Grupo'
        })
    )

    class Meta:
        model = Group
        fields = ['nombre', 'descripcion']

    def __init__(self, *args, **kwargs):
        super(GroupCreationForm, self).__init__(*args, **kwargs)
      

from django import forms


from django import forms

class GroupInvitationForm(forms.ModelForm):
    nombre_de_usuario = forms.CharField(
        label='Nombre de Usuario',
        max_length=100,
        widget=forms.TextInput(attrs={
            'style': 'background-color:black;color:white;border: 2px solid purple; width: 100%; padding: 5px; border-radius: 15px;',
            'placeholder': 'Nombre de Usuario'
        })
    )
    message = forms.CharField(
        label='Mensaje',
        widget=forms.Textarea(attrs={
            'style': 'border: 2px solid purple; width: 100%; padding: 5px;background-color:black;color:white',
            'rows': 3,
            'placeholder': 'Escribe un mensaje'
        })
    )

    class Meta:
        model = GroupInvitation
        fields = ['nombre_de_usuario', 'message']

class EditGroupForm(forms.ModelForm):
    descripcion = forms.CharField(
        label='Descripción',
        widget=forms.Textarea(attrs={
            'style': 'border: 2px solid purple; width: 100%; padding: 5px;background-color:black;color:white',
            'rows': 3,
            'placeholder': 'Una breve descripción del Grupo'
        })
    )
    class Meta:
        model = Group
        fields = ['descripcion']