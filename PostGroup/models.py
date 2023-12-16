from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from Group.models import Group

class PostGroup(models.Model):
    grupo = models.ForeignKey(Group, on_delete=models.CASCADE)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255, default="")  # Agrega un valor predeterminado
    contenido = models.TextField()
    archivo_adjunto = models.FileField(upload_to='uploads/', blank=True, null=True)
    nombre_archivo = models.CharField(max_length=255, default="Nombre de archivo por defecto")
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    total_calificaciones = models.IntegerField(default=0)
    
    def get_class_name(self):
        return self.__class__.__name__
    
    def get_group_name(self):
            return self.grupo.nombre

class Calificacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(PostGroup, on_delete=models.CASCADE)
    calificacion = models.IntegerField()


class CommentGroup(models.Model):
    post = models.ForeignKey(PostGroup, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.username} - {self.post.titulo}'
