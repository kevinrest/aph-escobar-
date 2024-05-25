from django.db import models

class residents(models.Model):
    identificacion = models.IntegerField(primary_key=45)
    nombre = models.CharField(max_length=60)
    apellido = models.CharField(max_length=80)
    edificio = models.CharField(max_length=10, blank=True, null=True)
    apartamento = models.CharField(max_length=10)
    cara = models.FileField(upload_to='archivos/')

    def __str__(self):
        return self.nombre