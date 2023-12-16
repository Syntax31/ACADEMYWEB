# models.py

from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255)
    contenido = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    archivo_adjunto = models.FileField(upload_to='archivos/', blank=True, null=True)
    nombre_archivo = models.CharField(max_length=255, blank=True, null=True)
    
    # Nueva relación con los comentarios
    comentarios = models.ManyToManyField('Comment', blank=True, related_name='post_comments')

    def __str__(self):
        return self.titulo
    
    def get_class_name(self):
        return self.__class__.__name__


# models.py

from django.db import models
from django.contrib.auth.models import User

class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.username} - {self.post.titulo}'

