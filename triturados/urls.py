from django.conf.urls import patterns, include, url
import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^static/(?P<path>.*)$','django.views.static.serve', {'document_root': settings.STATIC_ROOT}), 
    url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),
    url(r'^$', 'triturados.apps.planta.views.home', name='home'),
    url(r'^privado/', 'triturados.apps.planta.views.index', name='index'),
    url(r'^despacho/nuevo/(?P<id_programacion>.*)', 'triturados.apps.planta.views.nuevoDespacho', name='nuevo_despacho'),
    url(r'^(?P<id_planta>.*)/despachos/', 'triturados.apps.planta.views.indexDespachos', name='index_despachos'),
    url(r'^pedido/nuevo', 'triturados.apps.planta.views.ingresoPedido', name='nuevo_pedido'),
    url(r'^pedido/detalle/(?P<id_pedido>.*)$', 'triturados.apps.planta.views.verDetallePedido', name='detalle_pedido'),  
    url(r'^pedidos/', 'triturados.apps.planta.views.indexPedidos', name='index_pedidos'),
     url(r'^despachos/(?P<id_planta>.*)$', 'triturados.apps.planta.views.indexDespachos', name='index_despachos'),



    url(r'^indexProgramacion/(?P<id_item_pedido>.*)$', 'triturados.apps.planta.views.indexProgramacion', name='index_programacion'),
    url(r'^programar/(?P<id_item_pedido>.*)$', 'triturados.apps.planta.views.programarItemPedido', name='programar_item'),  
    url(r'^programacion/(?P<id_pedido>.*)$/agendar', 'triturados.apps.planta.views.indexProgramacion', name='index_programacion'),
    url(r'^programacion/planta/(?P<id_planta>.*)$', 'triturados.apps.planta.views.indexProgramacionPlanta', name='programacion_planta'),
    

    url(r'^bitacora/nuevo/registro', 'triturados.apps.planta.views.registroBitacora', name='registro_bitacora'),
    url(r'^bitacora/nuevo/registro', 'triturados.apps.planta.views.indexBitacora', name='index_bitacora'),

    # url(r'^triturados/', include('triturados.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)
