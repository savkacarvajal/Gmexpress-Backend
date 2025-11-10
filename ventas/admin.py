from django.contrib import admin
from .models import Venta, DetalleVenta
from .forms import VentaForm, DetalleVentaForm

class VentaAdmin(admin.ModelAdmin):
    form = VentaForm
    list_display = ['fecha_venta', 'usuario_id', 'total', 'estado']
    list_filter = ['estado', 'fecha_venta']
    search_fields = ['usuario_id__nombre']

class DetalleVentaAdmin(admin.ModelAdmin):
    form = DetalleVentaForm
    list_display = ['venta_id', 'producto_id', 'cantidad', 'subtotal']

admin.site.register(Venta, VentaAdmin)
admin.site.register(DetalleVenta, DetalleVentaAdmin)