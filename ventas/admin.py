from django.contrib import admin
from django.utils.html import format_html
from .models import Venta, DetalleVenta
from .forms import VentaForm, DetalleVentaForm


class DetalleVentaInline(admin.TabularInline):
    """
    Inline para mostrar detalles de venta dentro de la venta
    """
    model = DetalleVenta
    form = DetalleVentaForm
    extra = 1
    fields = ['producto_id', 'cantidad', 'precio_unitario', 'subtotal_display']
    readonly_fields = ['subtotal_display']
    
    def subtotal_display(self, obj):
        """Muestra el subtotal calculado"""
        if obj.cantidad and obj.precio_unitario:
            subtotal = obj.cantidad * obj.precio_unitario
            return format_html(
                '<span style="color: #28a745; font-weight: bold;">${:,}</span>',
                subtotal
            )
        return '-'
    subtotal_display.short_description = 'Subtotal'


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    """
    Administración de Ventas con vista detallada y estadísticas
    """
    form = VentaForm
    list_display = ['id', 'fecha_venta', 'usuario_id', 'tipo_venta_display', 'monto_total_display', 'estado_display']
    list_filter = ['tipo_venta', 'estado', 'fecha_venta']
    search_fields = ['usuario_id__nombre', 'usuario_id__run']
    ordering = ['-fecha_venta']
    date_hierarchy = 'fecha_venta'
    inlines = [DetalleVentaInline]
    
    fieldsets = (
        ('Información de la Venta', {
            'fields': ('fecha_venta', 'usuario_id', 'tipo_venta')
        }),
        ('Montos', {
            'fields': ('monto_total',),
            'classes': ('wide',)
        }),
        ('Estado', {
            'fields': ('estado',)
        }),
    )
    
    def tipo_venta_display(self, obj):
        """Muestra el tipo de venta formateado"""
        tipos = {
            'p': ('Producto', '#17a2b8'),
            's': ('Servicio', '#6f42c1'),
        }
        tipo_info = tipos.get(obj.tipo_venta, ('Desconocido', '#6c757d'))
        return format_html(
            '<span style="color: white; background-color: {}; padding: 3px 10px; border-radius: 3px;">{}</span>',
            tipo_info[1], tipo_info[0]
        )
    tipo_venta_display.short_description = 'Tipo'
    tipo_venta_display.admin_order_field = 'tipo_venta'
    
    def monto_total_display(self, obj):
        """Formatea el monto total en pesos chilenos"""
        return format_html(
            '<span style="color: #28a745; font-weight: bold; font-size: 14px;">${:,}</span>',
            obj.monto_total
        )
    monto_total_display.short_description = 'Monto Total'
    monto_total_display.admin_order_field = 'monto_total'
    
    def estado_display(self, obj):
        """Muestra el estado con colores según el valor"""
        estados = {
            '1': ('Pendiente', '#ffc107'),
            '2': ('En Proceso', '#17a2b8'),
            '3': ('Completado', '#28a745'),
            '4': ('Cancelado', '#dc3545'),
            '5': ('Devuelto', '#6c757d'),
        }
        estado_info = estados.get(obj.estado, ('Desconocido', '#6c757d'))
        return format_html(
            '<span style="color: white; background-color: {}; padding: 3px 10px; border-radius: 3px;">●  {}</span>',
            estado_info[1], estado_info[0]
        )
    estado_display.short_description = 'Estado'
    estado_display.admin_order_field = 'estado'
    
    # Acciones personalizadas
    actions = ['marcar_completado', 'marcar_en_proceso', 'marcar_cancelado']
    
    def marcar_completado(self, request, queryset):
        """Marca las ventas como completadas"""
        updated = queryset.update(estado='3')
        self.message_user(request, f'{updated} venta(s) marcada(s) como completadas.')
    marcar_completado.short_description = "✓ Marcar como completado"
    
    def marcar_en_proceso(self, request, queryset):
        """Marca las ventas como en proceso"""
        updated = queryset.update(estado='2')
        self.message_user(request, f'{updated} venta(s) marcada(s) como en proceso.')
    marcar_en_proceso.short_description = "⟳ Marcar como en proceso"
    
    def marcar_cancelado(self, request, queryset):
        """Marca las ventas como canceladas"""
        updated = queryset.update(estado='4')
        self.message_user(request, f'{updated} venta(s) marcada(s) como canceladas.')
    marcar_cancelado.short_description = "✗ Marcar como cancelado"
    
    # Configuración de la interfaz
    save_on_top = True
    list_per_page = 25


@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
    """
    Administración de Detalles de Venta
    """
    form = DetalleVentaForm
    list_display = ['venta_id', 'producto_id', 'cantidad', 'precio_unitario_display', 'subtotal_display']
    list_filter = ['venta_id__fecha_venta']
    search_fields = ['producto_id__nombre', 'venta_id__id']
    ordering = ['-venta_id__fecha_venta']
    
    fieldsets = (
        ('Venta', {
            'fields': ('venta_id',)
        }),
        ('Producto', {
            'fields': ('producto_id', 'cantidad')
        }),
        ('Precios', {
            'fields': ('precio_unitario',)
        }),
    )
    
    def precio_unitario_display(self, obj):
        """Formatea el precio unitario"""
        return format_html(
            '<span style="color: #28a745; font-weight: bold;">${:,}</span>',
            obj.precio_unitario
        )
    precio_unitario_display.short_description = 'Precio Unit.'
    precio_unitario_display.admin_order_field = 'precio_unitario'
    
    def subtotal_display(self, obj):
        """Calcula y muestra el subtotal"""
        subtotal = obj.cantidad * obj.precio_unitario
        return format_html(
            '<span style="color: #28a745; font-weight: bold; font-size: 14px;">${:,}</span>',
            subtotal
        )
    subtotal_display.short_description = 'Subtotal'
    
    # Configuración de la interfaz
    save_on_top = True
    list_per_page = 50