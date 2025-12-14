from rest_framework import serializers
from django.contrib.auth.models import User
from usuarios.models import TipoUsuario, Usuario
from catalogo.models import Servicio, Categoria as CategoriaWeb, Producto as ProductoWeb
from catalogue.models import Categoria, Producto
from ventas.models import Venta, DetalleVenta


# ==================== USUARIOS ====================
class TipoUsuarioSerializer(serializers.ModelSerializer):
    """Serializer para el modelo TipoUsuario"""
    
    class Meta:
        model = TipoUsuario
        fields = ['id', 'descripcion', 'estado', 'fecha_creacion']
        read_only_fields = ['id', 'fecha_creacion']


class UsuarioSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Usuario"""
    tipo_usuario_nombre = serializers.CharField(
        source='tipo_usuario.descripcion', 
        read_only=True
    )
    nombre_completo = serializers.SerializerMethodField()
    
    class Meta:
        model = Usuario
        fields = [
            'id', 'run', 'nombre', 'paterno', 'materno', 
            'correo', 'contrasenia', 'telefono', 'fecha_nacimiento',
            'fecha_registro', 'estado', 'tipo_usuario', 
            'tipo_usuario_nombre', 'nombre_completo'
        ]
        read_only_fields = ['id', 'fecha_registro']
        extra_kwargs = {
            'contrasenia': {'write_only': True}
        }
    
    def get_nombre_completo(self, obj):
        return obj.nombre_completo()
    
    def validate_run(self, value):
        """Validar formato de RUT chileno"""
        if not value:
            raise serializers.ValidationError("El RUT es obligatorio")
        return value
    
    def validate_correo(self, value):
        """Validar unicidad de correo"""
        if self.instance:
            # En caso de actualización, excluir el usuario actual
            if Usuario.objects.exclude(pk=self.instance.pk).filter(correo=value).exists():
                raise serializers.ValidationError("Este correo ya está registrado")
        else:
            # En caso de creación
            if Usuario.objects.filter(correo=value).exists():
                raise serializers.ValidationError("Este correo ya está registrado")
        return value


class UsuarioCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear usuarios (registro)"""
    
    class Meta:
        model = Usuario
        fields = [
            'run', 'nombre', 'paterno', 'materno', 
            'correo', 'contrasenia', 'telefono', 'fecha_nacimiento',
            'tipo_usuario'
        ]
        extra_kwargs = {
            'contrasenia': {'write_only': True}
        }


# ==================== CATÁLOGO WEB ====================
class ServicioSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Servicio"""
    
    class Meta:
        model = Servicio
        fields = ['id', 'nombre', 'imagen', 'servicio_tipo', 'descripcion', 'estado']
        read_only_fields = ['id']


class CategoriaWebSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Categoria del catálogo web"""
    
    class Meta:
        model = CategoriaWeb
        fields = ['id', 'nombre', 'descripcion', 'estado']
        read_only_fields = ['id']


class ProductoWebSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Producto del catálogo web"""
    categoria_nombre = serializers.CharField(
        source='categoria.nombre', 
        read_only=True
    )
    servicio_nombre = serializers.CharField(
        source='servicio.nombre', 
        read_only=True, 
        allow_null=True
    )
    
    class Meta:
        model = ProductoWeb
        fields = [
            'id', 'nombre', 'descripcion', 'precio', 'imagen',
            'categoria', 'categoria_nombre', 'servicio', 'servicio_nombre'
        ]
        read_only_fields = ['id']


# ==================== CATÁLOGO INTERNO ====================
class CategoriaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Categoria del catálogo interno"""
    
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion', 'estado']
        read_only_fields = ['id']


class ProductoSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Producto del catálogo interno"""
    categoria_nombre = serializers.CharField(
        source='categoria_id.nombre', 
        read_only=True
    )
    categoria_web_nombre = serializers.CharField(
        source='categoria_web_id.nombre', 
        read_only=True, 
        allow_null=True
    )
    servicio_nombre = serializers.CharField(
        source='servicio_id.nombre', 
        read_only=True, 
        allow_null=True
    )
    
    class Meta:
        model = Producto
        fields = [
            'id', 'nombre', 'descripcion', 'precio', 'stock', 'imagen',
            'categoria_id', 'categoria_nombre', 
            'categoria_web_id', 'categoria_web_nombre',
            'servicio_id', 'servicio_nombre'
        ]
        read_only_fields = ['id']
    
    def validate_precio(self, value):
        """Validar que el precio sea positivo"""
        if value <= 0:
            raise serializers.ValidationError("El precio debe ser mayor a 0")
        return value
    
    def validate_stock(self, value):
        """Validar que el stock sea positivo o cero"""
        if value < 0:
            raise serializers.ValidationError("El stock no puede ser negativo")
        return value


# ==================== VENTAS ====================
class DetalleVentaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo DetalleVenta"""
    producto_nombre = serializers.CharField(
        source='producto.nombre', 
        read_only=True
    )
    subtotal = serializers.SerializerMethodField()
    
    class Meta:
        model = DetalleVenta
        fields = [
            'id', 'venta', 'producto', 'producto_nombre',
            'precio_unitario', 'cantidad', 'subtotal'
        ]
        read_only_fields = ['id']
    
    def get_subtotal(self, obj):
        return obj.calcular_subtotal_producto()
    
    def validate_cantidad(self, value):
        """Validar que la cantidad sea positiva"""
        if value <= 0:
            raise serializers.ValidationError("La cantidad debe ser mayor a 0")
        return value
    
    def validate_precio_unitario(self, value):
        """Validar que el precio unitario sea positivo"""
        if value <= 0:
            raise serializers.ValidationError("El precio unitario debe ser mayor a 0")
        return value


class VentaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Venta"""
    usuario_nombre = serializers.CharField(
        source='usuario.nombre_completo', 
        read_only=True
    )
    detalles = DetalleVentaSerializer(many=True, read_only=True)
    
    class Meta:
        model = Venta
        fields = [
            'id', 'fecha_venta', 'estado', 'tipo_venta', 
            'monto_total', 'usuario', 'usuario_nombre', 'detalles'
        ]
        read_only_fields = ['id', 'fecha_venta']
    
    def validate_monto_total(self, value):
        """Validar que el monto total sea positivo"""
        if value <= 0:
            raise serializers.ValidationError("El monto total debe ser mayor a 0")
        return value


class DetalleVentaCreateSerializer(serializers.Serializer):
    """Serializer para crear detalles de venta sin venta_id"""
    producto = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all())
    precio_unitario = serializers.IntegerField(min_value=1)
    cantidad = serializers.IntegerField(min_value=1)


class VentaCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear ventas con detalles"""
    detalles = DetalleVentaCreateSerializer(many=True, write_only=True)
    
    class Meta:
        model = Venta
        fields = [
            'fecha_venta', 'estado', 'tipo_venta', 
            'monto_total', 'usuario', 'detalles'
        ]
    
    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')
        venta = Venta.objects.create(**validated_data)
        
        for detalle_data in detalles_data:
            DetalleVenta.objects.create(venta=venta, **detalle_data)
        
        return venta
