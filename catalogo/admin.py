from django.contrib import admin
from django.utils.html import format_html
from .models import Categoria, Producto, Servicio
from .forms import ServicioForm, ProductoWebForm, CategoriaWebForm


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    """
    Administración de Servicios con interfaz mejorada y vista previa de imágenes
    """
    form = ServicioForm
    list_display = ['nombre', 'imagen_preview', 'servicio_tipo', 'descripcion_corta', 'estado_display']
    list_filter = ['estado']
    search_fields = ['nombre', 'servicio_tipo', 'descripcion']
    ordering = ['nombre']
    
    fieldsets = (
        ('Información del Servicio', {
            'fields': ('nombre', 'servicio_tipo', 'descripcion')
        }),
        ('Imagen', {
            'fields': ('imagen',)
        }),
        ('Estado', {
            'fields': ('estado',),
            'classes': ('collapse',)
        }),
    )
    
    def imagen_preview(self, obj):
        """Muestra una miniatura de la imagen"""
        if obj.imagen:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 5px;" />',
                obj.imagen.url
            )
        return format_html('<span style="color: #999;">Sin imagen</span>')
    imagen_preview.short_description = 'Imagen'
    
    def descripcion_corta(self, obj):
        """Muestra una descripción truncada"""
        if obj.descripcion:
            return obj.descripcion[:50] + '...' if len(obj.descripcion) > 50 else obj.descripcion
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
    
    # Acciones personalizadas
    actions = ['activar_servicios', 'desactivar_servicios']
    
    def activar_servicios(self, request, queryset):
        """Activa los servicios seleccionados"""
        updated = queryset.update(estado='1')
        self.message_user(request, f'{updated} servicio(s) activado(s) exitosamente.')
    activar_servicios.short_description = "✓ Activar servicios seleccionados"
    
    def desactivar_servicios(self, request, queryset):
        """Desactiva los servicios seleccionados"""
        updated = queryset.update(estado='0')
        self.message_user(request, f'{updated} servicio(s) desactivado(s) exitosamente.')
    desactivar_servicios.short_description = "✗ Desactivar servicios seleccionados"
    
    # Configuración de la interfaz
    save_on_top = True
    list_per_page = 20


@admin.register(Categoria)
class CategoriaWebAdmin(admin.ModelAdmin):
    """
    Administración de Categorías del Catálogo Web
    """
    form = CategoriaWebForm
    list_display = ['nombre', 'descripcion_corta', 'estado_display']
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
    
    # Acciones personalizadas
    actions = ['activar_categorias', 'desactivar_categorias']
    
    def activar_categorias(self, request, queryset):
        updated = queryset.update(estado='1')
        self.message_user(request, f'{updated} categoría(s) activada(s) exitosamente.')
    activar_categorias.short_description = "✓ Activar categorías seleccionadas"
    
    def desactivar_categorias(self, request, queryset):
        updated = queryset.update(estado='0')
        self.message_user(request, f'{updated} categoría(s) desactivada(s) exitosamente.')
    desactivar_categorias.short_description = "✗ Desactivar categorías seleccionadas"
    
    save_on_top = True
    list_per_page = 20


@admin.register(Producto)
class ProductoWebAdmin(admin.ModelAdmin):
    """
    Administración de Productos del Catálogo Web
    """
    form = ProductoWebForm
    list_display = ['nombre', 'imagen_preview', 'precio_display', 'categoria', 'servicio']
    list_filter = ['categoria', 'servicio']
    search_fields = ['nombre', 'descripcion']
    ordering = ['nombre']
    
    fieldsets = (
        ('Información del Producto', {
            'fields': ('nombre', 'descripcion', 'precio')
        }),
        ('Clasificación', {
            'fields': ('categoria', 'servicio')
        }),
        ('Imagen', {
            'fields': ('imagen',)
        }),
    )
    
    def imagen_preview(self, obj):
        """Muestra una miniatura de la imagen"""
        if obj.imagen:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 5px;" />',
                obj.imagen.url
            )
        return format_html('<span style="color: #999;">Sin imagen</span>')
    imagen_preview.short_description = 'Imagen'
    
    def precio_display(self, obj):
        """Formatea el precio en pesos chilenos"""
        return format_html(
            '<span style="color: #28a745; font-weight: bold;">${:,}</span>',
            obj.precio
        )
    precio_display.short_description = 'Precio'
    precio_display.admin_order_field = 'precio'
    
    # Acciones personalizadas
    actions = ['duplicar_productos']
    
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
    
    save_on_top = True
    list_per_page = 25
