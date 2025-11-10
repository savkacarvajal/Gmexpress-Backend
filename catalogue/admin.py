from django.contrib import admin
from django.utils.html import format_html
from .models import Categoria, Producto
from .forms import CategoriaForm, ProductoForm


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    """
    Administración de Categorías de Productos con interfaz mejorada
    """
    form = CategoriaForm
    list_display = ['nombre', 'descripcion_corta', 'estado_display', 'total_productos']
    list_filter = ['estado']
    search_fields = ['nombre', 'descripcion']
    ordering = ['nombre']
    
    fieldsets = (
        ('Información de la Categoría', {
            'fields': ('nombre', 'descripcion', 'estado')
        }),
    )
    
    def descripcion_corta(self, obj):
        """Muestra una descripción truncada"""
        if obj.descripcion:
            return obj.descripcion[:60] + '...' if len(obj.descripcion) > 60 else obj.descripcion
        return '-'
    descripcion_corta.short_description = 'Descripción'
    
    def estado_display(self, obj):
        """Muestra el estado con colores"""
        if obj.estado == '1':
            return format_html(
                '<span style="color: white; background-color: #28a745; padding: 3px 10px; border-radius: 3px;">●  Activo</span>'
            )
        return format_html(
            '<span style="color: white; background-color: #dc3545; padding: 3px 10px; border-radius: 3px;">●  Inactivo</span>'
        )
    estado_display.short_description = 'Estado'
    
    def total_productos(self, obj):
        """Muestra el total de productos en esta categoría"""
        count = Producto.objects.filter(categoria_id=obj).count()
        return format_html(
            '<span style="background-color: #e9ecef; padding: 3px 10px; border-radius: 3px; font-weight: bold;">{} productos</span>',
            count
        )
    total_productos.short_description = 'Total Productos'
    
    # Acciones personalizadas
    actions = ['activar_categorias', 'desactivar_categorias']
    
    def activar_categorias(self, request, queryset):
        """Activa las categorías seleccionadas"""
        updated = queryset.update(estado='1')
        self.message_user(request, f'{updated} categoría(s) activada(s) exitosamente.')
    activar_categorias.short_description = "✓ Activar categorías seleccionadas"
    
    def desactivar_categorias(self, request, queryset):
        """Desactiva las categorías seleccionadas"""
        updated = queryset.update(estado='0')
        self.message_user(request, f'{updated} categoría(s) desactivada(s) exitosamente.')
    desactivar_categorias.short_description = "✗ Desactivar categorías seleccionadas"
    
    # Configuración de la interfaz
    save_on_top = True
    list_per_page = 20


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    """
    Administración de Productos del Inventario con interfaz completa
    """
    form = ProductoForm
    list_display = ['nombre', 'imagen_preview', 'precio_display', 'stock_display', 'categoria_id', 'estado_badge']
    list_filter = ['categoria_id']
    search_fields = ['nombre', 'descripcion']
    ordering = ['nombre']
    readonly_fields = ['imagen_preview_large']
    
    fieldsets = (
        ('Información del Producto', {
            'fields': ('nombre', 'descripcion')
        }),
        ('Precios y Stock', {
            'fields': ('precio', 'stock'),
            'classes': ('wide',)
        }),
        ('Clasificación', {
            'fields': ('categoria_id',)
        }),
        ('Imagen', {
            'fields': ('imagen', 'imagen_preview_large')
        }),
    )
    
    def imagen_preview(self, obj):
        """Muestra una miniatura de la imagen en el listado"""
        if obj.imagen:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 5px;" />',
                obj.imagen.url
            )
        return format_html('<span style="color: #999;">Sin imagen</span>')
    imagen_preview.short_description = 'Imagen'
    
    def imagen_preview_large(self, obj):
        """Muestra una vista previa grande de la imagen en el formulario"""
        if obj.imagen:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 300px; object-fit: contain; border-radius: 8px; border: 1px solid #ddd;" />',
                obj.imagen.url
            )
        return format_html('<span style="color: #999;">Sin imagen</span>')
    imagen_preview_large.short_description = 'Vista Previa'
    
    def precio_display(self, obj):
        """Formatea el precio en pesos chilenos"""
        return format_html(
            '<span style="color: #28a745; font-weight: bold;">${:,}</span>',
            obj.precio
        )
    precio_display.short_description = 'Precio'
    precio_display.admin_order_field = 'precio'
    
    def stock_display(self, obj):
        """Muestra el stock con indicador de color"""
        if obj.stock == 0:
            color = '#dc3545'
            text = 'Agotado'
        elif obj.stock < 10:
            color = '#ffc107'
            text = f'{obj.stock} unidades'
        else:
            color = '#28a745'
            text = f'{obj.stock} unidades'
        
        return format_html(
            '<span style="color: white; background-color: {}; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color, text
        )
    stock_display.short_description = 'Stock'
    stock_display.admin_order_field = 'stock'
    
    def estado_badge(self, obj):
        """Muestra un badge del estado del producto basado en el stock"""
        if obj.stock == 0:
            return format_html(
                '<span style="color: white; background-color: #dc3545; padding: 3px 10px; border-radius: 3px;">⚠ Sin Stock</span>'
            )
        elif obj.stock < 10:
            return format_html(
                '<span style="color: #856404; background-color: #fff3cd; padding: 3px 10px; border-radius: 3px;">⚡ Stock Bajo</span>'
            )
        return format_html(
            '<span style="color: white; background-color: #28a745; padding: 3px 10px; border-radius: 3px;">✓ Disponible</span>'
        )
    estado_badge.short_description = 'Estado'
    
    # Acciones personalizadas
    actions = ['duplicar_productos', 'marcar_sin_stock', 'reabastecer_stock']
    
    def duplicar_productos(self, request, queryset):
        """Duplica los productos seleccionados"""
        count = 0
        for producto in queryset:
            producto.pk = None
            producto.nombre = f"{producto.nombre} (Copia)"
            producto.save()
            count += 1
        self.message_user(request, f'{count} producto(s) duplicado(s) exitosamente.')
    duplicar_productos.short_description = "⎘ Duplicar productos seleccionados"
    
    def marcar_sin_stock(self, request, queryset):
        """Marca los productos como sin stock"""
        updated = queryset.update(stock=0)
        self.message_user(request, f'{updated} producto(s) marcado(s) sin stock.')
    marcar_sin_stock.short_description = "⚠ Marcar sin stock"
    
    def reabastecer_stock(self, request, queryset):
        """Reabastece el stock de los productos seleccionados"""
        updated = 0
        for producto in queryset:
            producto.stock += 50
            producto.save()
            updated += 1
        self.message_user(request, f'{updated} producto(s) reabastecido(s) con +50 unidades.')
    reabastecer_stock.short_description = "📦 Reabastecer stock (+50)"
    
    # Configuración de la interfaz
    save_on_top = True
    list_per_page = 25