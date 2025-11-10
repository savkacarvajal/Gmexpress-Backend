from django.contrib import admin
from django.utils.html import format_html
from .models import TipoUsuario, Usuario
from .forms import UsuarioForm, TipoUsuarioForm

@admin.register(TipoUsuario)
class TipoUsuarioAdmin(admin.ModelAdmin):
    """
    Administración de Tipos de Usuario con interfaz mejorada
    """
    form = TipoUsuarioForm
    list_display = ['descripcion', 'estado_display', 'fecha_creacion']
    list_filter = ['estado', 'fecha_creacion']
    search_fields = ['descripcion']
    ordering = ['descripcion']
    
    fieldsets = (
        ('Información del Tipo de Usuario', {
            'fields': ('descripcion', 'estado')
        }),
    )
    
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
    
    # Configuración de la interfaz
    save_on_top = True
    list_per_page = 20


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    """
    Administración de Usuarios con interfaz completa y acciones personalizadas
    """
    form = UsuarioForm
    list_display = ['run', 'nombre_completo', 'correo', 'tipo_usuario_id', 'fecha_nacimiento', 'estado_display']
    list_filter = ['tipo_usuario_id', 'fecha_nacimiento', 'fecha_creacion']
    search_fields = ['run', 'nombre', 'paterno', 'materno', 'correo']
    ordering = ['-fecha_creacion']
    date_hierarchy = 'fecha_creacion'
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('run', 'nombre', 'paterno', 'materno')
        }),
        ('Información de Contacto', {
            'fields': ('direccion', 'telefono', 'correo')
        }),
        ('Datos Adicionales', {
            'fields': ('fecha_nacimiento', 'tipo_usuario_id')
        }),
        ('Estado', {
            'fields': ('estado',),
            'classes': ('collapse',)
        }),
    )
    
    def nombre_completo(self, obj):
        """Muestra el nombre completo del usuario"""
        return f"{obj.nombre} {obj.paterno} {obj.materno or ''}"
    nombre_completo.short_description = 'Nombre Completo'
    nombre_completo.admin_order_field = 'nombre'
    
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
    actions = ['activar_usuarios', 'desactivar_usuarios']
    
    def activar_usuarios(self, request, queryset):
        """Activa los usuarios seleccionados"""
        updated = queryset.update(estado='1')
        self.message_user(request, f'{updated} usuario(s) activado(s) exitosamente.')
    activar_usuarios.short_description = "✓ Activar usuarios seleccionados"
    
    def desactivar_usuarios(self, request, queryset):
        """Desactiva los usuarios seleccionados"""
        updated = queryset.update(estado='0')
        self.message_user(request, f'{updated} usuario(s) desactivado(s) exitosamente.')
    desactivar_usuarios.short_description = "✗ Desactivar usuarios seleccionados"
    
    # Configuración de la interfaz
    save_on_top = True
    list_per_page = 25