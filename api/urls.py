from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import (
    TipoUsuarioViewSet,
    UsuarioViewSet,
    ServicioViewSet,
    CategoriaWebViewSet,
    ProductoWebViewSet,
    CategoriaViewSet,
    ProductoViewSet,
    VentaViewSet,
    DetalleVentaViewSet,
    register_user,
    user_info,
)

# Crear el router y registrar los ViewSets
router = DefaultRouter()

# Usuarios
router.register(r'tipos-usuario', TipoUsuarioViewSet, basename='tipousuario')
router.register(r'usuarios', UsuarioViewSet, basename='usuario')

# Catálogo Web (público)
router.register(r'servicios', ServicioViewSet, basename='servicio')
router.register(r'categorias-web', CategoriaWebViewSet, basename='categoriaweb')
router.register(r'productos-web', ProductoWebViewSet, basename='productoweb')

# Catálogo Interno (protegido)
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'productos', ProductoViewSet, basename='producto')

# Ventas
router.register(r'ventas', VentaViewSet, basename='venta')
router.register(r'detalle-ventas', DetalleVentaViewSet, basename='detalleventa')

urlpatterns = [
    # Autenticación JWT
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('auth/register/', register_user, name='register'),
    path('auth/me/', user_info, name='user_info'),
    
    # Incluir todas las rutas del router
    path('', include(router.urls)),
]
