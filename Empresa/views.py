from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from Empresa.models import Empresa
from Empresa.forms import EmpresaForm
from Empresa.serializers import EmpresaSerializer
# Create your views here.
def index (request):
	"""Vista de la pagina principal de la aplicacion.
		En ella se listan las empresas que hay registradas
		Tambien da la opcion de registrar una nueva empresa
	"""
	lista_ultimas_empresas = Empresa.objects.all()
	context = {'lista_ultimas_empresas': lista_ultimas_empresas}
	return render(request, 'empresa/index.html', context)

def add_empresa(request):
	"""Vista de la funcionalidad de add_empresa.

		Recibiendo un objeto del tipo request, analiza si se trata de datos enviados mediante un formulario.
		Comprueba que dicho formulario es valido en relacion al modelo y en caso de ser valido, alamacena en
		la base de datos la nueva empresa, devolviendo el flujo al index de la aplicacion.

		En caso de que el formulario no sea valido o se procese con errores, se informa de lo que esta pasando.
	"""
	if request.method == 'POST':
		form = EmpresaForm(request.POST)
		if form.is_valid():
			form.save(commit=True)
			return index(request)
		else:
			print form.errors
	else:
		form = EmpresaForm()
	return render(request, 'empresa/add_empresa.html', {'form': form})





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
	elif request.method == 'POST':
		#elif request.method == 'PUT':
		data = JSONParser().parse(request)
		serializador = EmpresaSerializer(empresa, data=data)
		#serializador = Empresa.update(empresa, data=data)
		if serializador.is_valid():
			serializador.save()
			return JSONResponse(serializador.data,status=202)
		return JSONResponse(serializador.errors, status=400)
	elif request.method == 'DELETE':
		empresa.delete()
		return HttpResponse(status=204)
