from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.test.client import RequestFactory

# Create your tests here.

from Empresa.models import Empresa,Valoracion
from Empresa.views import *


class EmpresaMethodTests(TestCase):
	"""
		Clase para Testear Empresa.
	"""

	def test_crea_empresa(self):
		"""
			Test para crear una Empresa
		"""
		emp = Empresa(nombre='etest',correo='ctest')
		emp.save()
		self.assertEqual(emp.nombre, 'etest')
		self.assertEqual(emp.correo, 'ctest')
        print("Empresa Creada Correctamente")

class ValoracionMethodTests(TestCase):

    def test_crea_valoracion(self):
        emp2 = Empresa(nombre='etest',correo='ctest')
        emp2.save()
        val = Valoracion(empresa=emp2,comentario='comentario de prueba',puntuacion=7)
        val.save()
        self.assertEqual(val.empresa,emp2)
        self.assertEqual(val.comentario, 'comentario de prueba')
        self.assertEqual(val.puntuacion, 7)
        print("Valoracion Creada Correctamente")


class RutasTests(APITestCase):
	"""
		Clase para testear las rutas de la applicacion
	"""
	def test_detalle_empresa(self):
		"""
			Test para consultar una unica empresa en detalle.
			Metodo get
		"""
		emp = Empresa(nombre='empresa1',correo='correo1')
		emp.save()
		response = self.client.get('/Empresa/1/')
		self.assertEqual(response.content,'{"nombre":"empresa1","correo":"correo1"}')
		print("Una unica Empresa consultada en detalle correctamente")

	def test_detalle_varias_empresas(self):
		"""
			Test para consultar varias empresas en detalle.
			Metodo get
		"""
		emp = Empresa(nombre='empresa1',correo='correo1')
		emp.save()
		emp2 = Empresa(nombre='empresa2',correo='correo2')
		emp2.save()
		response = self.client.get('/Empresas/')
		self.assertEqual(response.content,'[{"nombre":"empresa1","correo":"correo1"},{"nombre":"empresa2","correo":"correo2"}]')
		print("Varias Empresas consultadas en detalle correctamente")

	def test_crea_empresa(self):
		"""
			Test para crear una empresa
			Metodo post
		"""
		data={'nombre' : 'empresa_post', 'correo' : 'correo_post'}
		response=self.client.post('/Empresas/',data, format='json')
		self.assertEqual(response.status_code, 201)
		self.assertEqual(Empresa.objects.get().nombre,'empresa_post')
		print("REST: Empresa Creada correctamente")

	def test_actualiza_empresa(self):
		"""
			Test para actualizar una empresa
			Metodo post
		"""
		emp = Empresa(nombre='empresa1',correo='correo1')
		emp.save()
		data={'nombre' : 'empresa_update', 'correo' : 'correo_update'}
		response=self.client.post('/Empresa/1/',data, format='json')
		self.assertEqual(Empresa.objects.get().nombre, 'empresa_update')
		self.assertEqual(Empresa.objects.get().correo, 'correo_update')
		self.assertEqual(response.status_code, 202)
        print("REST: Empresa actualizada correctamente")

	def test_borra_empresa(self):
		"""
			Test para borrar una empresa
			Metodo delete
		"""
		emp = Empresa(nombre='empresa1',correo='correo1')
		emp.save()
		response=self.client.delete('/Empresa/1/',pk=emp.nombre)
		self.assertEqual(response.status_code, 204)
        print("REST: Empresa borrada correctamente")
