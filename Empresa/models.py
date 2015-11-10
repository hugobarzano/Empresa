from django.db import models

# Create your models here.



class Empresa(models.Model):
	"""Modelo para representar una empresa.
		Esta formado con el nombre de la empresa y su correo
	
	"""
	nombre = models.CharField (max_length=200)
	correo = models.CharField (max_length=200)
	
	
	def __unicode__(self):
		return self.nombre


class Valoracion(models.Model):
	"""Modelo para representar una valoracion acerca de una empresa.
		Esta formado por un comentario y una puntuacion
		Su clave externa es la empresa con la que esta relaccionada
	"""
	empresa = models.ForeignKey (Empresa)
	comentario = models.CharField (max_length=200)
	puntuacion = models.IntegerField (default=0)
	
	def __unicode__(self):
		return self.comentario
