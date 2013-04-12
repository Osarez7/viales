# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.contrib.admin import widgets
from triturados.apps.planta.models import Cliente, Producto, Planta, Obra, Pedido, Despacho

class ClienteForm(ModelForm):
    class Meta:
        model = Cliente


class ObraForm(forms.Form):
    nombre = forms.CharField(widget = forms.TextInput(), required=True)
    descripcion = forms.CharField(widget = forms.Textarea(), label="Descripción", required=True)
    categoria = forms.ModelChoiceField(queryset=Cliente.objects.all(), required=True, label="Cliente")

class ProgramacionForm(forms.Form):
     nombre = forms.CharField(widget = forms.TextInput(), required=True)
     descripcion = forms.CharField(widget = forms.Textarea(), label="Descripción", required=True)
      

class PedidoForm(ModelForm):
    class Meta: 
        model = Pedido
#Campos que se mostraran
        fields = ('cliente','fechaPedido','fechaEntrea','consecutivo')
# exclude = ('usuario', 'disponible',) <- Datos que se excluirán. Sirve de la misma manera las dos formas

class  DespachoForm(forms.Form):
    nombre = forms.CharField(widget = forms.TextInput(), required=True)
    fecha = forms.DateField(widget = widgets.AdminDateWidget, required=True)
    
#Campos que se mostraran
        
