from django import forms
from PostGroup.models import CommentGroup

class CommentGroupForm(forms.ModelForm):
    class Meta:
        model = CommentGroup
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Contenido de tu comentario'}),
        }
