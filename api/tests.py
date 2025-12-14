from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from usuarios.models import TipoUsuario, Usuario
from catalogo.models import Servicio, Categoria as CategoriaWeb, Producto as ProductoWeb
from catalogue.models import Categoria, Producto
from ventas.models import Venta, DetalleVenta
from datetime import date, timedelta


class JWTAuthenticationTestCase(TestCase):
    """Tests para autenticación JWT"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
    
    def test_obtain_jwt_token(self):
        """Test: Obtener tokens JWT con credenciales válidas"""
        response = self.client.post('/api/auth/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_obtain_jwt_token_invalid_credentials(self):
        """Test: Rechazar credenciales inválidas"""
        response = self.client.post('/api/auth/login/', {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_refresh_jwt_token(self):
        """Test: Renovar access token con refresh token"""
        # Obtener tokens
        login_response = self.client.post('/api/auth/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        refresh_token = login_response.data['refresh']
        
        # Renovar access token
        response = self.client.post('/api/auth/refresh/', {
            'refresh': refresh_token
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
    
    def test_verify_jwt_token(self):
        """Test: Verificar validez de un token"""
        # Obtener token
        login_response = self.client.post('/api/auth/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        access_token = login_response.data['access']
        
        # Verificar token
        response = self.client.post('/api/auth/verify/', {
            'token': access_token
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ServicioAPITestCase(TestCase):
    """Tests para el endpoint de Servicios (público)"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='admin',
            password='admin123'
        )
        self.servicio = Servicio.objects.create(
            nombre='Catering Corporativo',
            servicio_tipo='catering-corporativo',
            descripcion='Servicio de catering para empresas',
            estado='1'
        )
    
    def test_list_servicios_public(self):
        """Test: Listar servicios sin autenticación (público)"""
        response = self.client.get('/api/servicios/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
    
    def test_retrieve_servicio_public(self):
        """Test: Obtener detalle de servicio sin autenticación"""
        response = self.client.get(f'/api/servicios/{self.servicio.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], 'Catering Corporativo')
    
    def test_create_servicio_without_auth(self):
        """Test: No permitir crear servicio sin autenticación"""
        response = self.client.post('/api/servicios/', {
            'nombre': 'Nuevo Servicio',
            'servicio_tipo': 'nuevo-servicio',
            'descripcion': 'Descripción',
            'estado': '1'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_servicio_with_auth(self):
        """Test: Crear servicio con autenticación"""
        # Obtener token
        login_response = self.client.post('/api/auth/login/', {
            'username': 'admin',
            'password': 'admin123'
        })
        token = login_response.data['access']
        
        # Crear servicio con token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post('/api/servicios/', {
            'nombre': 'Nuevo Servicio',
            'servicio_tipo': 'nuevo-servicio',
            'descripcion': 'Descripción',
            'estado': '1'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_filter_servicios_by_estado(self):
        """Test: Filtrar servicios por estado"""
        Servicio.objects.create(
            nombre='Servicio Inactivo',
            servicio_tipo='inactivo',
            estado='0'
        )
        response = self.client.get('/api/servicios/?estado=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)


class UsuarioAPITestCase(TestCase):
    """Tests para el endpoint de Usuarios (protegido)"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='admin',
            password='admin123'
        )
        self.tipo_usuario = TipoUsuario.objects.create(
            descripcion='Cliente',
            estado='1'
        )
    
    def test_list_usuarios_without_auth(self):
        """Test: No permitir listar usuarios sin autenticación"""
        response = self.client.get('/api/usuarios/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_list_usuarios_with_auth(self):
        """Test: Listar usuarios con autenticación"""
        # Obtener token
        login_response = self.client.post('/api/auth/login/', {
            'username': 'admin',
            'password': 'admin123'
        })
        token = login_response.data['access']
        
        # Listar usuarios
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get('/api/usuarios/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_usuario_with_auth(self):
        """Test: Crear usuario con autenticación"""
        # Obtener token
        login_response = self.client.post('/api/auth/login/', {
            'username': 'admin',
            'password': 'admin123'
        })
        token = login_response.data['access']
        
        # Crear usuario
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post('/api/usuarios/', {
            'run': '12345678-9',
            'nombre': 'Juan',
            'paterno': 'Pérez',
            'materno': 'González',
            'correo': 'juan@example.com',
            'contrasenia': 'Password123!',
            'telefono': '+56912345678',
            'fecha_nacimiento': '1990-01-01',
            'tipo_usuario': self.tipo_usuario.id,
            'estado': '1'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ProductoWebAPITestCase(TestCase):
    """Tests para el endpoint de Productos Web (público para GET)"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='admin',
            password='admin123'
        )
        self.servicio = Servicio.objects.create(
            nombre='Catering',
            servicio_tipo='catering',
            estado='1'
        )
        self.categoria = CategoriaWeb.objects.create(
            nombre='Almuerzos',
            descripcion='Almuerzos ejecutivos',
            estado='1'
        )
        self.producto = ProductoWeb.objects.create(
            nombre='Almuerzo Ejecutivo',
            descripcion='Almuerzo completo',
            precio=5000,
            categoria=self.categoria,
            servicio=self.servicio
        )
    
    def test_list_productos_web_public(self):
        """Test: Listar productos web sin autenticación"""
        response = self.client.get('/api/productos-web/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
    
    def test_filter_productos_by_servicio(self):
        """Test: Filtrar productos por servicio"""
        response = self.client.get(f'/api/productos-web/?servicio={self.servicio.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
    
    def test_create_producto_web_without_auth(self):
        """Test: No permitir crear producto sin autenticación"""
        response = self.client.post('/api/productos-web/', {
            'nombre': 'Nuevo Producto',
            'descripcion': 'Descripción',
            'precio': 3000,
            'categoria': self.categoria.id,
            'servicio': self.servicio.id
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class VentaAPITestCase(TestCase):
    """Tests para el endpoint de Ventas (protegido)"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='admin',
            password='admin123'
        )
        self.tipo_usuario = TipoUsuario.objects.create(
            descripcion='Cliente',
            estado='1'
        )
        self.usuario = Usuario.objects.create(
            run='12345678-9',
            nombre='Juan',
            paterno='Pérez',
            materno='González',
            correo='juan@example.com',
            contrasenia='Password123!',
            telefono='+56912345678',
            fecha_nacimiento='1990-01-01',
            tipo_usuario=self.tipo_usuario,
            estado='1'
        )
        self.categoria = Categoria.objects.create(
            nombre='Almuerzos',
            descripcion='Almuerzos',
            estado='1'
        )
        self.producto = Producto.objects.create(
            nombre='Almuerzo',
            descripcion='Almuerzo completo',
            precio=5000,
            stock=10,
            categoria_id=self.categoria
        )
    
    def test_list_ventas_without_auth(self):
        """Test: No permitir listar ventas sin autenticación"""
        response = self.client.get('/api/ventas/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_list_ventas_with_auth(self):
        """Test: Listar ventas con autenticación"""
        # Obtener token
        login_response = self.client.post('/api/auth/login/', {
            'username': 'admin',
            'password': 'admin123'
        })
        token = login_response.data['access']
        
        # Listar ventas
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get('/api/ventas/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_venta_with_auth(self):
        """Test: Crear venta con autenticación"""
        # Obtener token
        login_response = self.client.post('/api/auth/login/', {
            'username': 'admin',
            'password': 'admin123'
        })
        token = login_response.data['access']
        
        # Crear venta
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post('/api/ventas/', {
            'fecha_venta': date.today().isoformat(),
            'estado': '1',
            'tipo_venta': 'p',
            'monto_total': 5000,
            'usuario': self.usuario.id,
            'detalles': [
                {
                    'producto': self.producto.id,
                    'precio_unitario': 5000,
                    'cantidad': 1
                }
            ]
        }, format='json')
        self.assertEqual(
            response.status_code, 
            status.HTTP_201_CREATED,
            f"Failed to create venta: {response.data}"
        )


class PaginationTestCase(TestCase):
    """Tests para paginación de la API"""
    
    def setUp(self):
        self.client = APIClient()
        # Crear múltiples servicios para probar paginación
        for i in range(15):
            Servicio.objects.create(
                nombre=f'Servicio {i}',
                servicio_tipo=f'servicio-{i}',
                estado='1'
            )
    
    def test_pagination_default_page_size(self):
        """Test: Verificar paginación con tamaño de página por defecto (10)"""
        response = self.client.get('/api/servicios/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 15)
        self.assertEqual(len(response.data['results']), 10)
        self.assertIsNotNone(response.data['next'])
    
    def test_pagination_second_page(self):
        """Test: Obtener segunda página de resultados"""
        response = self.client.get('/api/servicios/?page=2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)
        self.assertIsNone(response.data['next'])
        self.assertIsNotNone(response.data['previous'])
