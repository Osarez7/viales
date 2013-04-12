# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from triturados.apps.planta.models import Producto
from django.contrib.auth.decorators import login_required
from triturados.apps.planta.forms import PedidoForm, DespachoForm
from django.http import HttpResponseRedirect

def home(request):
    ctx = {}
    return render_to_response('home/index.html', ctx ,context_instance = RequestContext(request))


def nuevoPedido(request):
    form = PedidoForm
    if request.method == "POST":
        form = PedidoForm(request.POST)
        if form.is_valid():
            fechaPedido = form.cleaned_data['fechaPedido']
            fechaEntrea = form.cleaned_data['fechaEntrea']
            cliente = form.cleaned_data['cliente'].id
            consecutivo = form.cleaned_data['consecutivo']
             
            p = Pedido()
            p.fechaPedido = fechaPedido
            p.fechaEntrea = fechaEntrea
            p.cliente_id = cliente 
            p.consecutivo = consecutivo
            p.save()
            return HttpResponseRedirect('/')
    despachoForm = DespachoForm
    ctx = {'form':form,'formulario':despachoForm}
    return render_to_response('pedido/nuevo.html', ctx ,context_instance = RequestContext(request))

