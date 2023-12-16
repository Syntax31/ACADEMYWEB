from django import forms
from .models import PostGroup

class PostGroupForm(forms.ModelForm):
    titulo = forms.CharField(
        label='Título',
        widget=forms.TextInput(attrs={'class': 'titulo', 'placeholder': 'Ejemplo de título'})
    )
    
    contenido = forms.CharField(
        label='Contenido de la publicación',
        widget=forms.Textarea(attrs={'class': 'contenido', 'placeholder': 'Contenido de la publicación'})
    )

    archivo_adjunto = forms.FileField(
        label="Adjuntar archivo",
        widget=forms.ClearableFileInput(attrs={'class': 'archivo-adjunto', 'id': 'id_archivo_adjunto'})
    )

    class Meta:
        model = PostGroup
        fields = ['titulo', 'contenido', 'archivo_adjunto']



class CalificacionForm(forms.Form):
    calificacion = forms.IntegerField(min_value=1, max_value=5)
    
    
