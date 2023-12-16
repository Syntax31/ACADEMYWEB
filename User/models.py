from django.db import models
from django.contrib.auth.models import User
import json
from Group.models import Group
# MODELO USUARIO, ID SE GENERA SOLA POR DJANGO
# IMPORTAMOS USER DE DJANGO

class UserProfile(models.Model):
    email = models.EmailField(unique=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    intereses = models.TextField()
    preferencias = models.TextField(default='')
    nivel_de_dominio = models.TextField(max_length=50)
    grupos = models.ManyToManyField(Group, related_name='miembross', blank=True)

    def __str__(self):
        return self.user.username

    def __str__(self):
        return self.email



