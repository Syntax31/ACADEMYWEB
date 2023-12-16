from django import forms
from Post.models import Comment



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={'class': 'form-control', 'rows': 3,'placeholder':'Contenido de tu comentario'}),
        }
