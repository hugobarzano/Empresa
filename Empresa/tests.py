from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

# Create your tests here.

from Empresa.models import Empresa,Valoracion
from Empresa.views import *


class EmpresaMethodTests(TestCase):

	def test_crea_empresa(self):
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

	def test_detalle_empresa(self):
		emp = Empresa(nombre='empresa1',correo='correo1')
		emp.save()
		response = self.client.get('/Empresa/1/')
		self.assertEqual(response.content,'{"nombre":"empresa1","correo":"correo1"}')
		print("Una unica Empresa consultada en detalle correctamente")

	def test_detalle_varias_empresas(self):
		emp = Empresa(nombre='empresa1',correo='correo1')
		emp.save()
		emp2 = Empresa(nombre='empresa2',correo='correo2')
		emp2.save()
		response = self.client.get('/Empresas/')
		self.assertEqual(response.content,'[{"nombre":"empresa1","correo":"correo1"},{"nombre":"empresa2","correo":"correo2"}]')
		print("Varias Empresas consultadas en detalle correctamente")
