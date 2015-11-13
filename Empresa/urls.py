from django.conf.urls import url
from Empresa import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add_empresa/$', views.add_empresa, name='add_empresa'),
    url(r'^Empresas/$', views.Empresa_lista),
    url(r'^Empresa/(?P<pk>[0-9]+)/$', views.Empresa_detalle),
]
