from django import forms
from Empresa.models import Empresa

class EmpresaForm(forms.ModelForm):
    nombre = forms.CharField(max_length=200, help_text="Nombre Empresa")
    correo = forms.CharField(max_length=200, help_text="correo Empresa")

    class Meta:
        model = Empresa
        fields = ('nombre','correo')
