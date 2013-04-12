from django.contrib import admin
from triturados.apps.planta.models import Producto,Cliente, Obra, Planta, Pedido, ClienteProducto, ItemPedido, Programacion, Maquina, Vehiculo, Despacho, Anticipo

admin.site.register(Producto)
admin.site.register(Cliente)
admin.site.register(Obra)
admin.site.register(Planta)
admin.site.register(Pedido)
admin.site.register(ClienteProducto)
admin.site.register(ItemPedido)
admin.site.register(Programacion)
admin.site.register(Maquina)
admin.site.register(Vehiculo)
admin.site.register(Despacho)
admin.site.register(Anticipo)