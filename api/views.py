from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from usuarios.models import TipoUsuario, Usuario
from catalogo.models import Servicio, Categoria as CategoriaWeb, Producto as ProductoWeb
from catalogue.models import Categoria, Producto
from ventas.models import Venta, DetalleVenta

from .serializers import (
    TipoUsuarioSerializer,
    UsuarioSerializer,
    UsuarioCreateSerializer,
    ServicioSerializer,
    CategoriaWebSerializer,
    ProductoWebSerializer,
    CategoriaSerializer,
    ProductoSerializer,
    VentaSerializer,
    VentaCreateSerializer,
    DetalleVentaSerializer,
)


# ==================== PERMISOS PERSONALIZADOS ====================
class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    Permiso personalizado para permitir acceso de lectura a todos
    pero solo permitir escritura a usuarios autenticados
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated


# ==================== USUARIOS ====================
class TipoUsuarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD de TipoUsuario
    Requiere autenticación JWT
    """
    queryset = TipoUsuario.objects.all()
    serializer_class = TipoUsuarioSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['estado']
    search_fields = ['descripcion']
    ordering_fields = ['id', 'descripcion', 'fecha_creacion']
    ordering = ['-fecha_creacion']


class UsuarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD de Usuario
    Requiere autenticación JWT
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['estado', 'tipo_usuario']
    search_fields = ['run', 'nombre', 'paterno', 'materno', 'correo']
    ordering_fields = ['id', 'nombre', 'fecha_registro']
    ordering = ['-fecha_registro']


# ==================== CATÁLOGO WEB ====================
class ServicioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD de Servicio
    GET: Público
    POST/PUT/PATCH/DELETE: Requiere autenticación JWT
    """
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['estado', 'servicio_tipo']
    search_fields = ['nombre', 'descripcion', 'servicio_tipo']
    ordering_fields = ['id', 'nombre']
    ordering = ['id']


class CategoriaWebViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD de Categoria Web
    GET: Público
    POST/PUT/PATCH/DELETE: Requiere autenticación JWT
    """
    queryset = CategoriaWeb.objects.all()
    serializer_class = CategoriaWebSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['estado']
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['id', 'nombre']
    ordering = ['id']


class ProductoWebViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD de Producto Web (catálogo público)
    GET: Público
    POST/PUT/PATCH/DELETE: Requiere autenticación JWT
    """
    queryset = ProductoWeb.objects.all()
    serializer_class = ProductoWebSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categoria', 'servicio']
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['id', 'nombre', 'precio']
    ordering = ['id']


# ==================== CATÁLOGO INTERNO ====================
class CategoriaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD de Categoria (catálogo interno)
    Requiere autenticación JWT
    """
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['estado']
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['id', 'nombre']
    ordering = ['id']


class ProductoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD de Producto (catálogo interno)
    Requiere autenticación JWT
    """
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categoria_id', 'categoria_web_id', 'servicio_id']
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['id', 'nombre', 'precio', 'stock']
    ordering = ['id']


# ==================== VENTAS ====================
class VentaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD de Venta
    Requiere autenticación JWT
    """
    queryset = Venta.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['estado', 'tipo_venta', 'usuario']
    search_fields = ['usuario__nombre', 'usuario__correo']
    ordering_fields = ['id', 'fecha_venta', 'monto_total']
    ordering = ['-fecha_venta']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return VentaCreateSerializer
        return VentaSerializer


class DetalleVentaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD de DetalleVenta
    Requiere autenticación JWT
    """
    queryset = DetalleVenta.objects.all()
    serializer_class = DetalleVentaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['venta', 'producto']
    search_fields = ['producto__nombre']
    ordering_fields = ['id', 'cantidad', 'precio_unitario']
    ordering = ['id']


# ==================== AUTENTICACIÓN Y REGISTRO ====================
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Endpoint para registro de nuevos usuarios
    POST /api/auth/register/
    """
    serializer = UsuarioCreateSerializer(data=request.data)
    if serializer.is_valid():
        usuario = serializer.save()
        return Response({
            'message': 'Usuario registrado exitosamente',
            'usuario': {
                'id': usuario.id,
                'nombre': usuario.nombre_completo(),
                'correo': usuario.correo
            }
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    """
    Endpoint para obtener información del usuario autenticado
    GET /api/auth/me/
    """
    # El usuario autenticado viene en request.user
    # Necesitamos buscar el Usuario del modelo personalizado
    try:
        # Buscar por correo o username si el usuario está en el sistema de auth de Django
        usuario = Usuario.objects.filter(correo=request.user.email).first()
        if not usuario:
            return Response({
                'error': 'Usuario no encontrado en el sistema'
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UsuarioSerializer(usuario)
        return Response(serializer.data)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
