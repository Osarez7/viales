# -*- coding: utf-8 -*-
from django.db import models
#Se importa los usuarios para usarlo en Producto
from django.contrib.auth.models import User

#Se crea el modelo de categoría
class Producto(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    referencia = models.CharField(max_length=100, unique=True)
    desc    = models.CharField(max_length=200, unique=True)
    def __unicode__(self):
        return self.nombre 

class Cliente(models.Model):
    nombre = models.CharField(max_length=50)
    telefono = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    precioTransporte = models.BigIntegerField()
    def __unicode__(self):  
        return self.nombre


class Obra(models.Model):
#usuario = models.ForeignKey(User)
    nombre = models.CharField(max_length=100, unique=True)
    cliente = models.ForeignKey(Cliente)
    descripcion = models.TextField()

    def __unicode__(self):
        return self.nombre

class Planta(models.Model):
    nombre     = models.CharField(max_length=100, unique=True)
    ubicacion  = models.CharField(max_length=200)
    producto   = models.ManyToManyField(Producto)
    jefe       = models.OneToOneField(User)
    def __unicode__(self):
        return self. nombre 
      
class Pedido(models.Model):

    cliente      = models.ForeignKey(Cliente)
    fechaPedido  = models.DateField()
    fechaEntrega = models.DateField()
    consecutivo  = models.CharField(max_length=100, unique=True)
    pendiente    = models.BooleanField(default=True)

    def __unicode__(self):
        return self.consecutivo



class ClienteProducto(models.Model): 
    cliente = models.ForeignKey(Cliente)
    producto = models.ForeignKey(Producto)
    precio = models.BigIntegerField()
    def __unicode__(self):
        return self.cliente


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido) 
    obra = models.ForeignKey(Obra)
    producto = models.ForeignKey(Producto)
    cantidad = models.IntegerField()
    def __unicode__(self):
        return '%s de pedido %s ' % (self.producto,self.pedido ) 

class Programacion(models.Model):
    itemPedido = models.ForeignKey(ItemPedido) 
    planta = models.ForeignKey(Planta) 
    cantidad = models.IntegerField()
    fecha = models.DateField()

class Maquina(models.Model):
    nombre = models.CharField(max_length=100, unique=True)  
    valor = models.IntegerField()
    planta = models.ForeignKey(Planta)
    def __unicode__(self):
        return self.nombre   
    
class Vehiculo(models.Model):
    idVehiculo   =  models.OneToOneField(Maquina)
    placa     =  models.CharField(max_length=20, unique=True)
    capacidad = models.IntegerField()
    modelo    =  models.CharField(max_length=20, unique=True)
    def __unicode__(self):
        return self.placa 

class Despacho(models.Model):
    programacion = models.ForeignKey(Programacion) 
    vehiculo = models.ForeignKey(Vehiculo)
    cantidad = models.IntegerField()
    fecha =  models.DateField()
    remision = models.CharField(max_length=100, unique=True)
    def __unicode__(self):
        return self.remision

class Anticipo(models.Model):
    despacho = models.ForeignKey(Despacho) 
    valor = models.IntegerField()
    concepto = models.CharField(max_length=100, unique=True)
    
               


