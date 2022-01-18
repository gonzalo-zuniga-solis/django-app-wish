from ssl import create_default_context
from django.db import models

# Create your models here.
class User(models.Model):
    
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=200, unique=True, null=True)
    password = models.CharField(max_length=100)
    confirm_password = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    # deseos = listado de deseos de un usuario
    # preferencias  = listado de deseos cumplidos

    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['name']
        
    def __str__(self):
        return f"{self.name}"

class Deseo(models.Model):
    item = models.CharField(max_length=200) 
    usuario = models.ForeignKey(User, related_name='deseos', on_delete=models.CASCADE)
    comsumidores = models.ManyToManyField(User, related_name="preferencias")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
