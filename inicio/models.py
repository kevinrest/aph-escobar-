from django.db import models

class User(models.Model):
    id = models.IntegerField(primary_key=20)
    nombre = models.CharField(max_length=45)
    contraseña = models.CharField(max_length=30)
    
    def __str__(self):
        return self.nombre