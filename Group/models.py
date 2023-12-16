from django.db import models


from django.db import models
from django.contrib.auth.models import User

class Group(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    administrador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='grupos_administrados')
    miembros = models.ManyToManyField(User, related_name='grupos_pertenecientes')

    def __str__(self):
        return self.nombre

from django.db import models
from django.contrib.auth.models import User
from .models import Group

class GroupInvitation(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_invitations', on_delete=models.CASCADE)
    nombre_de_usuario = models.CharField(max_length=150) 
    message = models.TextField(blank=True)
    accepted = models.BooleanField(default=False)



class JoinRequest(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='join_requests')
    sender = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Solicitud de {self.sender.username} para unirse a {self.group.nombre}"
