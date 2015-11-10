from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from Empresa.models import Empresa
from Empresa.serializers import EmpresaSerializer
# Create your views here.


class JSONResponse(HttpResponse):
	"""
	Un HttpResponse que renderiza su contenido a formato JSON.
	"""
	def __init__(self, data, **kwargs):
		content = JSONRenderer().render(data)
		kwargs['content_type'] = 'application/json'
		super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def Empresa_lista(request):
	"""
	Lista todas las empresas o crea una nueva
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


@csrf_exempt
def Empresa_detalle(request, pk):
	"""
	Recuperar, actualizar o borrar una empresa
	"""
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












