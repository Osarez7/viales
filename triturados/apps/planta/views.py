# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from triturados.apps.planta.models import Producto, Despacho, Planta
from django.contrib.auth.decorators import login_required
from triturados.apps.planta.forms import PedidoForm, DespachoForm
from django.http import HttpResponseRedirect
import datetime
import json

def home(request):
    ctx = {}
    return render_to_response('home/index.html', ctx ,context_instance = RequestContext(request))

def index(request):
    ctx = {}
    return render_to_response('home/index-privado.html', ctx ,context_instance = RequestContext(request))

def indexDespachos(request,id_planta):
    #fecha=datetime.date.today(),
    #planta  = Despacho.objects.get(id=id_planta)
    request.user
    despachos = Despacho.objects.filter(planta_id=id_planta).order_by('-id');
    ctx = {'despachos':despachos,'id_planta':id_planta}
  
    return render_to_response('admin_planta/despachoIndex.html', ctx ,context_instance = RequestContext(request))

def nuevoDespacho(request,id_planta):
    formulario = DespachoForm(initial={'planta':id_planta})
    if request.method == "POST":
        formulario = DespachoForm(request.POST)
        if formulario.is_valid():
            
            d = Despacho()
            d.planta_id = formulario.cleaned_data['planta']
            d.cantidad = formulario.cleaned_data['cantidad']
            d.fecha = formulario.cleaned_data['fecha']
            d.remision= formulario.cleaned_data['remision']
            d.save()
            return HttpResponseRedirect('/%s/despachos' % id_planta)
   
    ctx = {'formulario':formulario, 'id_planta':id_planta}
    return render_to_response('admin_planta/despacho/nuevoDespacho.html', ctx ,context_instance = RequestContext(request))




def indexProgramacion(request):
  
    despachos = Programacion.objects.all().order_by('-id');
    ctx = {'despachos':despachos,}
  
    return render_to_response('admin_planta/despacho/despachoIndex.html', ctx ,context_instance = RequestContext(request))


def indexProgramacionPlanta(request,id_planta):
   
    programacion = Programacion.objects.filter(planta_id=id_planta).order_by('-id');
    ctx = {'programacion':programacion,'id_planta':id_planta}
  
    return render_to_response('admin_planta/despacho/despachoIndex.html', ctx ,context_instance = RequestContext(request))


def nuevoPedido(request):
    form = PedidoForm
    if request.method == "POST":
        form = PedidoForm(request.POST)
        if form.is_valid():
            fechaPedido = form.cleaned_data['fechaPedido']
            fechaEntrea = form.cleaned_data['fechaEntrea']
            cliente = form.cleaned_data['cliente'].id
            consecutivo = form.cleaned_data['consecutivo']
            items  = json.loads(form.cleaned_data['items']) 

            p = Pedido()
            p.fechaPedido = fechaPedido
            p.fechaEntrea = fechaEntrea
            p.cliente_id = cliente 
            p.consecutivo = consecutivo
            p.save()
            nuevosItems(items , p.id )
            return HttpResponseRedirect('/pedidos')  
    ctx = {'formulario':form}
    return render_to_response('facturacion/pedido/nuevoPedido.html', ctx ,context_instance = RequestContext(request))

def nuevosItems(items , pedido_id ):
   
    itemObj

    for item in items:
        itemObj = Item()
        itemObj.pruducto_id = item.producto 
        itemObj.obra_id = item.obra
        itemObj.pedido_id = pedido_id
        itemObj.pruducto_id = item.cantidad
        itemObj.save()
