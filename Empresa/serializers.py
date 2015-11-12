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
		#instance.nombre = validated_data.nombre
		#instance.correo = validated_data.correo
		instance.save()
		return instance
