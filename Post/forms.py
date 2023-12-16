from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    contenido = forms.CharField(
        label='Contenido de la publicación',  # Cambia el texto de la etiqueta aquí
        widget=forms.Textarea(attrs={'rows': 10})


        
    )

    class Meta:
        model = Post
        fields = ['titulo','contenido', 'archivo_adjunto']  # Elimina 'archivo_adjunto' si no lo necesitas
    titulo = forms.CharField(
            label='Título',
     widget=forms.TextInput(attrs={'class': 'titulo', 'placeholder': '¿Qué titulo le pondras?'}),        )
    
    contenido = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'contenido', 'placeholder': ' Este sera el contenido de tu publicación'}),
    )

    archivo_adjunto = forms.FileField(
    label="Adjuntar archivo",
    widget=forms.ClearableFileInput(attrs={
        'class': 'archivo-adjunto', 
        'id': 'id_archivo_adjunto',
        'style': 'border: 3px solid purple;height:150px;background:url({% static "images/proyecto.png" %});background-size:cover;color:white'
    }),
)



# forms.py




