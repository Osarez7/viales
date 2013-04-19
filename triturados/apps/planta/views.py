# -*- coding: utf-8 -*-
import datetime
import json
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext # For CSRF
from triturados.apps.planta.models import Producto, Despacho, Planta, Pedido, ItemPedido, Programacion
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
                programacion = form.save(commit=False
                programacion.save()
            return HttpResponseRedirect('/indexProgramacion/%i' % formulario.cleaned_data['consecutivo']) # Redirect to a 'success' page   
    else:
        programacion_formset = ProgramacionFormSet(initial=[{'itemPedido':id_item_pedido]})
        item_pedido =  ItemPedido.objects.get(pk=id_item_pedido)

    # For CSRF protection
    # See http://docs.djangoproject.com/en/dev/ref/contrib/csrf/ 
    c = {
         'item_pedido' : item_pedido,
         'programacion_formset': programacion_formset
        }
    c.update(csrf(request))

    return render_to_response('programacion/programarItem.html', c)




def indexDespachos(request,id_planta):
    #fecha=datetime.date.today(),
    #planta  = Despacho.objects.get(id=id_planta)
    request.user
    lstProgramacion = Programacion.objects.filter(planta_id=id_planta)
    despachos = Despacho.objects.filter(id__in=lstProgramacion).order_by('-id').select_related()
    ctx = {'despachos':despachos,'id_planta':id_planta}
  
    return render_to_response('admin_planta/despacho/despachoIndex.html', ctx ,context_instance = RequestContext(request))

def nuevoDespacho(request,id_programacion):

    
    class RequiredFormSet(BaseFormSet):
        def __init__(self, *args, **kwargs):
            super(RequiredFormSet, self).__init__(*args, **kwargs)
            for form in self.forms:
                form.empty_permitted = False
    DespachoFormSet = formset_factory(DespachoForm, max_num=10, formset=RequiredFormSet)
    if request.method == 'POST': # If the form has been submitted...
        
        formulario = ConsecutivoItemForm(request.POST)
        despacho_formset =  DespachoFormSet(request.POST, request.FILES)

        if  despacho_formset.is_valid() and formulario.is_valid():
            
            for form in despacho_formset.forms:
                despacho = form.save(commit=False)
                despacho.programacion_id = formulario.cleaned_data['consecutivo']
                despacho.save()
            return HttpResponseRedirect('/despachos/%i' % formulario.cleaned_data['consecutivo']) # Redirect to a 'success' page
        else:
            
    else:
        
        consecutivo_form = ConsecutivoItemForm(initial={'consecutivo': id_programacion})
        despacho_formset = DespachoFormSet ()

    # For CSRF protection
    # See http://docs.djangoproject.com/en/dev/ref/contrib/csrf/ 
    c = {'consecutivo_form': consecutivo_form,
         'despacho_formset': despacho_formset,
         'programacion' : programacion
        }
    c.update(csrf(request))

    return render_to_response('admin_planta/despacho/nuevoDespacho.html', c)
 



def indexProgramacion(request,id_item_pedido):
    item_pedido =  ItemPedido.objects.get(pk=id_item_pedido)
    lstProgramacion = Programacion.objects.filter(itemPedido_id=id_item_pedido).order_by('-id')
    ctx = {'item_pedido':item_pedido,'lstProgramacion':lstProgramacion}
  
    return render_to_response('programacion/indexProgramacionItem.html', ctx ,context_instance = RequestContext(request))


def indexProgramacionPlanta(request,id_planta):
   
    planta = Planta.objects.get(pk=id_planta)
    lstProgramacion = Programacion.objects.select_related().filter(planta_id=id_planta)
   # lstProgramacion = Programacion.objects.raw('select planta_programacion.*, planta_itempedido.* from planta_programacion inner join planta_itempedido on planta_programacion.itempedido_id = planta_itempedido.id where planta_programacion.planta_id = %s' % id_planta)
    ctx = {'lstProgramacion':lstProgramacion,'id_planta':id_planta, 'planta': planta } 
    return render_to_response('programacion/indexProgramacionPlanta.html', ctx ,context_instance = RequestContext(request))


def nuevoPedido(request):
    form = PedidoForm
    if request.method == "POST":
        form = PedidoForm(request.POST)
        if form.is_valid():
            fechaPedido = form.cleaned_data['fechaPedido']
            fechaEntrega = form.cleaned_data['fechaEntrega']
            cliente = form.cleaned_data['cliente'].id
            consecutivo = form.cleaned_data['consecutivo']
            items  = json.loads(form.cleaned_data['items']) 

            p = Pedido()
            p.fechaPedido = fechaPedido
            p.fechaEntrega = fechaEntrega
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
            return HttpResponseRedirect('/pedidos') # Redirect to a 'success' pa
            
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
