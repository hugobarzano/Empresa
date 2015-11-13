#Pasos a seguir para crear una aplicacion con variables REST utilizando djangorestframework 

##Crear entorno de pruebas
	virtualenv EntornoPruebas
	source EntornoPruebas/bin/activate

##Intalar dependencias

	pip install django
	pip install djangorestframework 

##Crear el proyecto

	django-admin.py startproject EjerciciosIV

###Crear aplicación

	python manage.py startapp Empresa

##Añadir restFramewokr y aplicación al proyecto en settings.py

	INSTALLED_APPS = (
	    'django.contrib.admin',
	    'django.contrib.auth',
	    'django.contrib.contenttypes',
	    'django.contrib.sessions',
	    'django.contrib.messages',
	    'django.contrib.staticfiles',
	    'rest_framework',
	    'Empresa',
	)

##Añadir la url de la aplicacion a las urls del proyecto

	urlpatterns = [
	    url(r'^admin/', include(admin.site.urls)),
	    url(r'^', include('Empresa.urls')),
	]

##Creacion de los modelos con los que vamos a trabajar en models.py
	
	from django.db import models

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

##Migracion y modelado de la base de datos

	python manage.py makemigrations snippets
	python manage.py migrate

##Crear clases para serializar las intancias de empresa en formato Json

	from rest_framework import serializers
	from Empresa.models import Empresa


	class EmpresaSerializer(serializers.Serializer):
		nombre = serializers.CharField(max_length=200)
		correo = serializers.CharField(max_length=200)

		def create(self, validated_data):
			"""
			Crea y vevuelve una nueva instancia de Empresa
			"""
			return Empresa.objects.create(**validated_data)

		def update(self, instance, validated_data):
			"""
			Actualiza y devuelve una instancia de Empresa, teniendo en cuenta los datos validados
			"""
			instance.nombre = validated_data.get('nombre', instance.nombre)
			instance.correo = validated_data.get('correo', instance.correo)
			instance.save()
			return instance
##Crear contenido

El siguiente paso es crear instancias de Empresa con las que podemos trabajar. Esto puede hacerse desde linea de comandos o desde el 
panel de administrador que facilita Django. En la siguiente captura se muestra como seria desde linea de comandos y tambien compruebo que la serialización funciona:

![serializar](https://www.dropbox.com/s/9m9ay7jqapdmu7t/serializar.png?dl=1)


#Crear vistas regulares para Django con la clase serializadora

Los primero es crear una subclase HttpResponse que pueda renderizar cualquier dato a formato Json 

	class JSONResponse(HttpResponse):
		def __init__(self, data, **kwargs):
			content = JSONRenderer().render(data)
			kwargs['content_type'] = 'application/json'
			super(JSONResponse, self).__init__(content, **kwargs)


Ahora vamos a crear las funcionalidades principales de nuestra API que serán, listar empresas o crearlas.

	def Empresa_lista(request):
	    """
	    Lista todos los nombres de empresas o crea una nueva
	    """
	    if request.method == 'GET':
		empresas = Empresa.objects.all()
		serializador = EmpresaSerializer(empresas, many=True)
		return JSONResponse(serializador.data)

	    elif request.method == 'POST':
		data = JSONParser().parse(request)
		serializador = EmpresaSerializer(data=data)
		if serializador.is_valid():
			serializador.save()
			return JSONResponse(serializador.data, status=201)
		return JSONResponse(serializador.errors, status=400)

y ya que estamos podemos añadir mas funcionalidades para  recuperar, actualizar o borrar una empresa

	def Empresa_detalle(request, pk):

		try:
			empresa = Empresa.objects.get(pk=pk)
		except Empresa.DoesNotExist:
			return HttpResponse(status=404)

		if request.method == 'GET':
			serializador = EmpresaSerializer(empresa)
			return JSONResponse(serializador.data)
		elif request.method == 'PUT':
			data = JSONParser().parse(request)
			serializador = EmpresaSerializer(empresa, data=data)
			if serializador.is_valid():
				serializador.save()
				return JSONResponse(serializador.data)
			return JSONResponse(serializador.errors, status=400)
		elif request.method == 'DELETE':
			empresa.delete()
			return HttpResponse(status=204)



##Añadir estas vistas, a las rutas de la aplicación

Para ello creamos el fichero urls.py en el directorio de la aplicación y añadimos lo siguiente:

	from django.conf.urls import url
	from Empresa import views

	urlpatterns = [
	    url(r'^Empresa/$', views.Empresa_lista),
	    url(r'^Empresa/(?P<pk>[0-9]+)/$', views.Empresa_detalle),
	]

##comprobar que esta funcionando

Llegados a este punto, podemos hacer una prueba sobre las vistas, para ello ponemos en marcha el servidor:

	python manage.py runserver

Y mediante un navegador o mediante curl, podemos comprobar que efectivamente las peticiones son 
renderizadas a formato Json

![Serializar_2](https://www.dropbox.com/s/go7igqx2nds6ve2/serializar2.png?dl=1)








