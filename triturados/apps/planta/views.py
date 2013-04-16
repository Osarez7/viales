# -*- coding: utf-8 -*-
import datetime
import json
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext # For CSRF
from triturados.apps.planta.models import Producto, Despacho, Planta, Pedido, ItemPedido
from django.contrib.auth.decorators import login_required
from triturados.apps.planta.forms import PedidoForm, DespachoForm, ItemPedidoForm, ProgramacionForm, ConsecutivoItemForm
from django.http import HttpResponseRedirect


from django.core.context_processors import csrf 
from django.forms.formsets import formset_factory, BaseFormSet
from django.http import HttpResponse, HttpResponseRedirect


def home(request):
    ctx = {}
    return render_to_response('home/index.html', ctx ,context_instance = RequestContext(request))

def index(request):
    ctx = {}
    return render_to_response('home/index-privado.html', ctx ,context_instance = RequestContext(request))

def indexBitacora(request):
    ctx = {}
    return render_to_response('home/index-privado.html', ctx ,context_instance = RequestContext(request))

def registroBitacora(request):
    ctx = {}
    return render_to_response('home/index-privado.html', ctx ,context_instance = RequestContext(request))

def programarItemPedido(request,id_item_pedido):
    # This class is used to make empty formset forms required
    # See http://stackoverflow.com/questions/2406537/django-formsets-make-first-required/4951032#4951032
    


    class RequiredFormSet(BaseFormSet):
        def __init__(self, *args, **kwargs):
            super(RequiredFormSet, self).__init__(*args, **kwargs)
            for form in self.forms:
                form.empty_permitted = False  
    ProgramacionFormSet = formset_factory(ProgramacionForm, max_num=10, formset=RequiredFormSet)
    if request.method == 'POST': # If the form has been submitted...
        programacion_formset = ProgramacionFormSet(request.POST, request.FILES)
        formulario = ConsecutivoItemForm(request.POST)

        if programacion_formset.is_valid() and formulario.is_valid():
            for form in programacion_formset.forms:
                programacion = form.save(commit=False)
    
                programacion.itemPedido_id = formulario.cleaned_data['consecutivo']
                programacion.save()
            return HttpResponseRedirect('/pedidos') # Redirect to a 'success' page
        else:
            return render_to_response('pedido/nuevoPedido.html')    
    else:
        programacion_formset = ProgramacionFormSet()

    # For CSRF protection
    # See http://docs.djangoproject.com/en/dev/ref/contrib/csrf/ 
    c = {
         'programacion_formset': programacion_formset,
         'consecutivo_item_form': ConsecutivoItemForm(initial={'consecutivo':id_item_pedido})       }
    c.update(csrf(request))

    return render_to_response('programacion/programarItem.html', c)




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


def indexPedidos(request):
    lstPedidos = Pedido.objects.all().order_by('-fechaPedido');
    ctx = {'lstPedidos': lstPedidos}
    return render_to_response('pedido/indexPedido.html', ctx ,context_instance = RequestContext(request))




def ingresoPedido(request):
    # This class is used to make empty formset forms required
    # See http://stackoverflow.com/questions/2406537/django-formsets-make-first-required/4951032#4951032
    class RequiredFormSet(BaseFormSet):
        def __init__(self, *args, **kwargs):
            super(RequiredFormSet, self).__init__(*args, **kwargs)
            for form in self.forms:
                form.empty_permitted = False
    ItemPedidoFormSet = formset_factory(ItemPedidoForm, max_num=10, formset=RequiredFormSet)
    if request.method == 'POST': # If the form has been submitted...
        pedido_form = PedidoForm(request.POST) # A form bound to the POST data
        # Create a formset from the submitted data
        item_pedido_formset = ItemPedidoFormSet(request.POST, request.FILES)

        if pedido_form.is_valid() and item_pedido_formset.is_valid():
            pedido = pedido_form.save()
            for form in item_pedido_formset.forms:
                pedido_item = form.save(commit=False)
                pedido_item.pedido = pedido
                pedido_item.save()
            return HttpResponseRedirect('/pedidos') # Redirect to a 'success' page
        else:
            return render_to_response('pedido/nuevoPedido.html')    
    else:
        pedido_form = PedidoForm()
        item_pedido_formset = ItemPedidoFormSet()

    # For CSRF protection
    # See http://docs.djangoproject.com/en/dev/ref/contrib/csrf/ 
    c = {'pedido_form':  pedido_form,
         'item_pedido_formset': item_pedido_formset
        }
    c.update(csrf(request))

    return render_to_response('pedido/nuevoPedido.html', c)

def verDetallePedido(request,id_pedido):
    pedido = Pedido.objects.filter(pk=id_pedido);
    lstItemsPedido = ItemPedido.objects.filter(pedido=pedido);
    ctx = {'lstItemsPedido': lstItemsPedido, 'pedido':pedido}
    return render_to_response('pedido/detallePedido.html', ctx ,context_instance = RequestContext(request))
