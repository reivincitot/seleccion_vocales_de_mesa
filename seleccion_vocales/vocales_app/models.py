from django.db import models
from django.core.exceptions import ValidationError


# Create your models here.
class Votantes(models.Model):
    id_votante = models.BigAutoField(primary_key=True)
    cedula = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)
    edad = models.IntegerField(max_length=3)
    sexo = models.CharField(max_length=1)
    ha_sido_vocal = models.BooleanField(default=False)
    ultimo_ano_de_vocal = models.DateField(blank=True, null=True)
    latitud = models.DecimalField(max_digits=9, decimal_places=6)
    longitud = models.DecimalField(max_digits=9, decimal_places=6)
    presenta_discapacidad = models.BooleanField()

    def clean(self):
        # Verificar si ha_salido_vocal es True y fecha_seleccion está vacio
        if self.ha_sido_vocal and not self.ultimo_ano_de_vocal:
            raise ValidationError(
                "Fecha de selección es obligatoria para votantes que han sido vocales."
            )


class LocalDeVotacion(models.Model):
    id_local = models.AutoField(primary_key=True)
    nombre_del_local = models.CharField(max_length=255)
    cantidad_mesa = models.IntegerField(3)
    region = models.CharField(255)
    comuna = models.CharField(255)
    direccion = models.CharField(255)
    excepcion = models.BooleanField(default=False)
    motivo_exepcion = models.CharField(blank=True, null=True)
    latitud = models.DecimalField(max_digits=9, decimal_places=6)
    longitud = models.DecimalField(max_digits=9,decimal_places=6)

    def clean(self):
        # Verificar si hay excepción pero no se ha proporcionado el motivo
        if self.excepcion and not self.motivo_exepcion:
            raise ValidationError(
                "Se debe proporcionar el motivo de la excepción del local de votación."
            )


class MesaDeVotacion(models.Model):
    id_mesa = models.AutoField(primary_key=True)
    local_de_votacion = models.ForeignKey(LocalDeVotacion, on_delete=models.CASCADE)
    numero_de_la_mesa = models.IntegerField(max_length=6)
    vocales = models.ManyToManyField(Votantes, through="VocalesSeleccionados")


class VocalesSeleccionados(models.Model):
    vocal = models.ForeignKey(Votantes, on_delete=models.CASCADE)
    mesa_de_votacion = models.ForeignKey(MesaDeVotacion, on_delete=models.CASCADE)
    fecha_seleccion = models.DateField()
