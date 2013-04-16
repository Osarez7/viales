# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.contrib.admin import widgets
from triturados.apps.planta.models import Cliente, Producto, Planta, Obra, Pedido,ItemPedido, Despacho, Programacion

class ClienteForm(ModelForm):
    class Meta:
        model = Cliente

class ObraForm(forms.Form):
    nombre = forms.CharField(widget = forms.TextInput(), required=True)
    descripcion = forms.CharField(widget = forms.Textarea(), label="Descripción", required=True)
    categoria = forms.ModelChoiceField(queryset=Cliente.objects.all(), required=True, label="Cliente")

class ProgramacionForm(ModelForm):
    class Meta: 
        model = Programacion
        exclude = ('itemPedido')   

class PedidoForm(ModelForm):
    class Meta: 
        model = Pedido
#Campos que se mostraran
        fields = ('cliente','fechaPedido','fechaEntrea','consecutivo')
# exclude = ('usuario', 'disponible',) <- Datos que se excluirán. Sirve de la misma manera las dos formas



class ItemPedidoForm(ModelForm):
    class Meta: 
        model = ItemPedido
#Campos que se mostraran
        exclude = ('pedido') 


class  ConsecutivoItemForm(forms.Form):
         
         consecutivo  =  forms.IntegerField(widget = forms.HiddenInput(), required=True)


class  DespachoForm(forms.Form):
         remision = forms.CharField(widget = forms.TextInput(), required=True)
         cantidad =  forms.CharField(widget = forms.TextInput(), required=True)
         fecha =  forms.DateField()
         planta  =  forms.IntegerField(widget = forms.HiddenInput(), required=True)

class RangoFechaForm(forms.Form):
     fechaInicial = forms.DateField()
     fechaFinal = forms.DateField()

           



    

#Campos que se mostraran
        
