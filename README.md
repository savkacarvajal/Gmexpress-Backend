

<div align="center">
   <img src="static/images/gm express.png" alt="GM Express Logo" width="180"/>
   <h1>🚀 GM Express - Sistema de Gestión Completo</h1>
   <b>Sistema Django completo para la gestión de servicios de alimentación y eventos de <span style="color:#388e3c">GM Express</span>.</b>
   <br/>
   <i>Aplicación web funcional con CRUD completo, autenticación, validaciones de negocio y panel administrativo.</i>
</div>

---

## 📋 **DESCRIPCIÓN DEL PROYECTO**

GM-Express es una aplicación web desarrollada en Django 5.2.7 que proporciona un sistema integral de gestión para una empresa chilena de servicios de alimentación y catering. 

### **Características Principales:**
- ✅ **API RESTful con JWT**: API completa con autenticación JWT (tokens de 60 min)
- ✅ **Sistema de Autenticación**: Login/Logout con protección de vistas
- ✅ **CRUD Completo**: Operaciones Create, Read, Update, Delete para todas las entidades
- ✅ **Endpoints Públicos y Protegidos**: Control granular de permisos
- ✅ **Validaciones de Negocio**: 
  - RUT chileno válido
  - Fechas en el pasado (no permitir fechas futuras)
  - Stock disponible antes de ventas
  - Duplicados de registros
  - Precios y cantidades positivas
- ✅ **Formularios con Validación**: Todos los formularios incluyen validaciones de formato y negocio
- ✅ **Panel Administrativo**: Dashboard con estadísticas y gestión completa
- ✅ **Sitio Web Responsive**: Catálogo público con Bootstrap 5
- ✅ **Base de Datos Poblada**: 50+ registros de prueba
- ✅ **Tests Completos**: 20 tests unitarios para la API

---

## 🗂️ **ESTRUCTURA DEL PROYECTO**

```text
GM-Express/
│
├── 📁 APLICACIONES (5 Apps Django)
│   ├── api/               # 🔌 API RESTful con JWT
│   │   ├── serializers.py # Serializers para todos los modelos
│   │   ├── views.py       # ViewSets con permisos
│   │   ├── urls.py        # Rutas de la API
│   │   └── tests.py       # 20 tests unitarios
│   │
│   ├── usuarios/           # 👥 Gestión de usuarios y tipos
│   │   ├── models.py       # Usuario, TipoUsuario
│   │   ├── forms.py        # Formularios con validaciones
│   │   └── views.py        # CRUD completo
│   │
│   ├── catalogue/          # 📋 Catálogo de productos internos
│   │   ├── models.py       # Producto, Categoria (inventario)
│   │   ├── forms.py        # Validación stock, precios
│   │   └── views.py        # CRUD productos/categorías
│   │
│   ├── ventas/            # 💰 Sistema de ventas
│   │   ├── models.py       # Venta, DetalleVenta
│   │   ├── forms.py        # Validación fechas, montos, stock
│   │   └── views.py        # CRUD ventas y detalles
│   │
│   └── catalogo/          # 🌐 Catálogo web público
│       ├── models.py       # Servicio, Producto (web)
│       ├── forms.py        # Formularios servicios
│       └── views.py        # Vistas públicas + CRUD
│
├── 📁 CONFIGURACIÓN
│   ├── gmexpress/         # ⚙️ Configuración principal
│   │   ├── settings.py    # Base de datos, apps, zona horaria Chile
│   │   └── urls.py        # Todas las rutas (públicas y CRUD)
│   │
│   ├── templates/         # 🎨 Plantillas HTML
│   │   ├── templateEmpresa/    # Inicio, login, dashboard, info
│   │   ├── templateCatalogo/   # Catálogo público
│   │   ├── templateUsuarios/   # CRUD usuarios
│   │   ├── templateCatalogue/  # CRUD productos
│   │   └── templateVentas/     # CRUD ventas
│   │
│   └── static/           # 🖼️ CSS, imágenes y recursos
│
├── 📁 BASE DE DATOS
│   ├── db.sqlite3        # 🗄️ Base de datos SQLite (activa)
│   └── migrate_to_mysql.sh # 🔄 Script migración MySQL opcional
│
└── 📁 DOCUMENTACIÓN
    ├── README.md         # 📖 Este archivo
    ├── requirements.txt  # 📦 Dependencias del proyecto
    └── manage.py         # 🛠️ Script gestión Django
```

---

## 🚀 **INSTALACIÓN Y EJECUCIÓN**

### **📋 Requisitos Previos:**
- Python 3.11 o superior
- pip (gestor de paquetes de Python)
- Git (para clonar el repositorio)

### **⚙️ Pasos de Instalación:**

#### **1. Clonar el Repositorio:**
```bash
git clone https://github.com/PandaAkiraNakai/GM-Express.git
cd GM-Express
```

#### **2. Crear y Activar Entorno Virtual:**

**En Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**En Windows (CMD):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**En Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### **3. Instalar Dependencias:**
```bash
pip install -r requirements.txt
```

El archivo `requirements.txt` contiene:
- Django==5.2.7
- pymysql==1.1.1
- asgiref==3.8.1
- sqlparse==0.5.2

#### **4. Aplicar Migraciones:**
```bash
python manage.py migrate
```

Este comando crea/actualiza todas las tablas en la base de datos SQLite.

#### **5. (Opcional) Poblar Base de Datos:**

La base de datos ya viene poblada con datos de prueba. Si necesitas repoblarla:

```bash
python poblar_servicios.py
```

#### **6. Iniciar el Servidor:**
```bash
python manage.py runserver
```

El servidor se iniciará en: **http://127.0.0.1:8000/**

---

## 🔐 **CREDENCIALES DE ACCESO**

### **Administrador Django (Admin Panel):**
- **URL**: http://127.0.0.1:8000/admin/
- **Usuario**: `admin`
- **Contraseña**: `admin123`

### **Acceso al Dashboard:**
- **URL**: http://127.0.0.1:8000/login/
- **Usuario**: `admin`
- **Contraseña**: `admin123`

---

## 🌐 **ESTRUCTURA DE URLS Y FUNCIONALIDADES**

### **📍 Rutas Públicas (sin autenticación):**
- **Inicio**: http://127.0.0.1:8000/
- **Catálogo**: http://127.0.0.1:8000/catalogo/
- **Productos**: http://127.0.0.1:8000/catalogo/catering-corporativo/
- **Nosotros**: http://127.0.0.1:8000/nosotros/
- **Login**: http://127.0.0.1:8000/login/

### **🔒 Rutas Protegidas (requieren login):**

#### **Dashboard:**
- http://127.0.0.1:8000/dashboard/

#### **CRUD Usuarios:**
- Lista: http://127.0.0.1:8000/usuarios/
- Crear: http://127.0.0.1:8000/usuarios/crear/
- Editar: http://127.0.0.1:8000/usuarios/{id}/editar/
- Eliminar: http://127.0.0.1:8000/usuarios/{id}/eliminar/
- Detalle: http://127.0.0.1:8000/usuarios/{id}/

#### **CRUD Tipos de Usuario:**
- Lista: http://127.0.0.1:8000/tipos-usuario/
- Crear: http://127.0.0.1:8000/tipos-usuario/crear/
- Editar: http://127.0.0.1:8000/tipos-usuario/{id}/editar/
- Eliminar: http://127.0.0.1:8000/tipos-usuario/{id}/eliminar/

#### **CRUD Categorías:**
- Lista: http://127.0.0.1:8000/categorias/
- Crear: http://127.0.0.1:8000/categorias/crear/
- Editar: http://127.0.0.1:8000/categorias/{id}/editar/
- Eliminar: http://127.0.0.1:8000/categorias/{id}/eliminar/

#### **CRUD Productos:**
- Lista: http://127.0.0.1:8000/productos/
- Crear: http://127.0.0.1:8000/productos/crear/
- Editar: http://127.0.0.1:8000/productos/{id}/editar/
- Eliminar: http://127.0.0.1:8000/productos/{id}/eliminar/
- Detalle: http://127.0.0.1:8000/productos/{id}/

#### **CRUD Ventas:**
- Lista: http://127.0.0.1:8000/ventas/
- Crear: http://127.0.0.1:8000/ventas/crear/
- Editar: http://127.0.0.1:8000/ventas/{id}/editar/
- Eliminar: http://127.0.0.1:8000/ventas/{id}/eliminar/
- Detalle: http://127.0.0.1:8000/ventas/{id}/
- Agregar Producto: http://127.0.0.1:8000/ventas/{id}/agregar-producto/

#### **CRUD Servicios:**
- Lista: http://127.0.0.1:8000/servicios/
- Crear: http://127.0.0.1:8000/servicios/crear/
- Editar: http://127.0.0.1:8000/servicios/{id}/editar/
- Eliminar: http://127.0.0.1:8000/servicios/{id}/eliminar/

---

## ✅ **VALIDACIONES IMPLEMENTADAS**

### **Validaciones de Formato:**
- ✅ RUT chileno con dígito verificador válido
- ✅ Correos electrónicos únicos
- ✅ Teléfonos en formato chileno
- ✅ Contraseñas seguras (9+ caracteres, mayúscula, símbolo)
- ✅ Slug de servicios en minúsculas con guiones

### **Validaciones de Negocio:**
- ✅ **Fechas en el pasado**: No permitir ventas o nacimientos futuros
- ✅ **Stock disponible**: Verificar antes de vender
- ✅ **Duplicados**: Evitar nombres/RUTs/correos duplicados
- ✅ **Valores positivos**: Precios, cantidades, montos > 0
- ✅ **Edad mínima**: Usuarios deben tener 18+ años
- ✅ **Relaciones protegidas**: No eliminar si hay registros dependientes

---

## 📊 **DATOS DE PRUEBA**

La base de datos incluye:
- **10+ Usuarios** con datos chilenos reales
- **3 Tipos de Usuario**: Administrador, Cliente, Empleado
- **4 Categorías**: Almuerzos, Bebidas, Repostería, Snacks
- **31 Productos** con precios y stock
- **6 Servicios**: Catering, Eventos, Delivery, etc.
- **Múltiples Ventas** con detalles

---

## 🛠️ **COMANDOS ÚTILES**

### **Gestión de Base de Datos:**
```bash
# Crear migraciones después de cambios en models.py
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario (si necesitas otro)
python manage.py createsuperuser
```

### **Comandos Personalizados:**
```bash
# Verificar servicios activos
python manage.py crear_servicios

# Actualizar imágenes de productos
python manage.py actualizar_imagenes
```

### **Servidor de Desarrollo:**
```bash
# Iniciar servidor
python manage.py runserver

# Iniciar en otro puerto
python manage.py runserver 8080

# Iniciar accesible desde red local
python manage.py runserver 0.0.0.0:8000
```

---

## 🔧 **CONFIGURACIÓN DE BASE DE DATOS**

### **SQLite (Actual - Desarrollo):**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### **MySQL (Opcional - Comentado en settings.py):**
Requiere XAMPP con MariaDB 10.5+
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'gmexpress',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

---

## 📱 **TECNOLOGÍAS UTILIZADAS**

- **Backend**: Django 5.2.7 (Python)
- **Base de Datos**: SQLite (desarrollo), MySQL compatible
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Autenticación**: Django Auth
- **Localización**: Español chileno (es-cl)
- **Zona Horaria**: America/Santiago

---

## 📝 **NOTAS IMPORTANTES**

### **Para Desarrollo:**
- `DEBUG = True` - Solo para desarrollo
- `SECRET_KEY` es insegura - cambiar en producción
- Imágenes se referencian como rutas de texto en `static/images/`

### **Para Producción:**
- Cambiar `DEBUG = False`
- Generar nueva `SECRET_KEY` segura
- Configurar `ALLOWED_HOSTS`
- Usar base de datos MySQL/PostgreSQL
- Ejecutar `python manage.py collectstatic`
- Configurar servidor web (Nginx/Apache) con Gunicorn

### **Para Despliegue en AWS:**
1. Instalar dependencias: `pip install -r requirements.txt`
2. Configurar variables de entorno para credenciales DB
3. Aplicar migraciones: `python manage.py migrate`
4. Recopilar archivos estáticos: `python manage.py collectstatic`
5. Configurar Nginx/Apache como proxy inverso
6. Usar Gunicorn como servidor WSGI

---

## 🎯 **CUMPLIMIENTO DE REQUISITOS**

### **✅ Requisitos Funcionales:**
- [x] Implementación de todos los formularios (excepto transaccionales)
- [x] Validaciones de formato (RUT, email, teléfono, etc.)
- [x] Validaciones de negocio (fechas pasadas, duplicados, stock)
- [x] Sistema de autenticación (login/logout)
- [x] Acceso protegido a vistas sensibles (@login_required)
- [x] CRUD completo para todas las entidades

### **✅ Requisitos Técnicos:**
- [x] Configuración de base de datos en settings.py
- [x] Archivo requirements.txt incluido
- [x] README.md con instrucciones completas
- [x] Credenciales de prueba documentadas
- [x] Proyecto ejecutable con `python manage.py runserver`
- [x] Código limpio, documentado y estructurado

---

## 👨‍💻 **AUTOR**

**Proyecto**: GM-Express
**Repositorio**: https://github.com/PandaAkiraNakai/GM-Express
**Curso**: Programación Back End
**Institución**: INACAP
**Fecha**: Noviembre 2025

---

## 📞 **CONTACTO GM-EXPRESS**

- **Teléfono**: +569 7615 9518 / +569 4785 4598
- **Email**: ventas@gmexpress.cl / proveedores@gmexpress.cl
- **Facebook**: https://www.facebook.com/GMEXPRESSCL
- **Instagram**: https://www.instagram.com/gmexpress_cl/

---

<div align="center">
   <b>✨ Proyecto completamente funcional y listo para despliegue ✨</b>
</div>

### **� Características Principales:**
- ✅ **4 Aplicaciones Django** independientes
- ✅ **Sistema de autenticación** completo
- ✅ **Panel administrativo** personalizado
- ✅ **Sitio web responsive** con Bootstrap 5
- ✅ **Base de datos** poblada con datos reales
- ✅ **50+ registros** de servicios, productos y usuarios
- ✅ **32 imágenes** asignadas automáticamente

---

## 🗂️ **Estructura del Proyecto**

```text
GM-Express/
│
├── 📁 APLICACIONES PRINCIPALES
│   ├── usuarios/           # 👥 Gestión de usuarios y tipos
│   ├── catalogue/          # 📋 Catálogo de productos y categorías  
│   ├── ventas/            # 💰 Sistema de ventas y detalles
│   └── catalogo/          # 🌐 Navegación web y servicios
│
├── 📁 CONFIGURACIÓN
│   ├── gmexpress/         # ⚙️ Configuración principal Django
│   ├── templates/         # 🎨 Plantillas HTML responsive
│   └── static/           # 🖼️ CSS, imágenes y recursos
│
├── 📁 BASE DE DATOS
│   ├── db.sqlite3        # 🗄️ Base de datos SQLite
│   └── migrate_to_mysql.sh # 🔄 Script migración MySQL
│
└── 📁 DOCUMENTACIÓN
    ├── README.md         # 📖 Este archivo
    ├── CHECKLIST.md      # ✅ Lista verificación completa
    └── manage.py         # 🛠️ Script gestión Django
```

---

## � **Aplicaciones del Sistema**

### **👥 `usuarios` - Gestión de Usuarios**
| Modelo | Descripción | Registros |
|--------|-------------|-----------|
| `TipoUsuario` | Tipos: Cliente, Admin, Empleado | 3 tipos |
| `Usuario` | Usuarios con datos chilenos reales | 10+ usuarios |

### **📋 `catalogue` - Catálogo de Productos**
| Modelo | Descripción | Registros |
|--------|-------------|-----------|
| `Categoria` | Almuerzos, Bebidas, Repostería, Snacks | 4 categorías |
| `Producto` | Productos alimenticios con precios | 31 productos |

### **💰 `ventas` - Sistema de Ventas**
| Modelo | Descripción | Registros |
|--------|-------------|-----------|
| `Venta` | Transacciones con usuarios | Múltiples ventas |
| `DetalleVenta` | Detalles de productos vendidos | Detalles completos |

### **🌐 `catalogo` - Navegación Web**
| Modelo | Descripción | Registros |
|--------|-------------|-----------|
| `Servicio` | Servicios de GM-Express | 6 servicios |
| `Producto` | Productos para navegación web | 31 productos |

---

## 🌐 **Sitio Web y Navegación**

### **🏠 Páginas Principales:**
- **🏠 Inicio:** `http://127.0.0.1:8000/` - Servicios con imágenes
- **📋 Catálogo:** `http://127.0.0.1:8000/catalogo/tradicional/` - Productos
- **📊 Dashboard:** `http://127.0.0.1:8000/dashboard/` - Panel administrativo
- **⚙️ Admin:** `http://127.0.0.1:8000/admin/` - Administración Django

### **🎨 Características del Sitio:**
- ✅ **Responsive Design** con Bootstrap 5
- ✅ **Navegación intuitiva** entre servicios
- ✅ **Imágenes automáticas** para productos
- ✅ **Autenticación** de usuarios
- ✅ **Dashboard administrativo** con estadísticas

---

## 🔐 **Acceso y Credenciales**

### **👨‍💼 Usuario Administrador:**
```
Usuario: admin
Contraseña: admin123

---

## 🛠️ **Instalación y Ejecución**

### **📋 Requisitos:**
- Python 3.11+
- Django 5.2.7
- SQLite (incluido)

### **🚀 Instalación Rápida:**

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/PandaAkiraNakai/GM-Express.git
   cd GM-Express
   ```

2. **Crea y activa entorno virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # venv\Scripts\activate   # Windows
   ```

3. **Instala dependencias:**
   ```bash
   pip install django
   ```

4. **Ejecuta migraciones:**
   ```bash
   python manage.py migrate
   ```

5. **Inicia el servidor:**
   ```bash
   python manage.py runserver
   ```

6. **Accede al sitio:**
   - Abre: `http://127.0.0.1:8000/`

---

## �️ **Comandos Personalizados**

### **📊 Verificar Servicios:**
```bash
python manage.py crear_servicios
```

### **🖼️ Actualizar Imágenes:**
```bash
python manage.py actualizar_imagenes
```

### **🔄 Migrar a MySQL:**
```bash
./migrate_to_mysql.sh
```

---

## 🔄 **Base de Datos**

### **🗄️ SQLite (Desarrollo):**
- ✅ **Configurado** y funcionando
- ✅ **Datos migrados** completamente
- ✅ **Listo para desarrollo**

### **� MySQL (Producción):**
- ✅ **Script de migración** creado
- ✅ **Configuración XAMPP** disponible
- ✅ **Comandos automáticos** incluidos

---

## 📝 **Documentación Adicional**

- **📋 [CHECKLIST.md](CHECKLIST.md)** - Lista completa de verificación
- **🔧 [catalogo/management/commands/](catalogo/management/commands/)** - Comandos personalizados
- **🎨 [static/CSS/style.css](static/CSS/style.css)** - Estilos personalizados
- **📊 [templates/](templates/)** - Plantillas HTML

---

## 🤝 **Contribuciones**

Sergio el Nazer
Savkapleito
Dante's Inferno

---

## 🔌 **API RESTful con Autenticación JWT**

### **📖 Descripción de la API**

El proyecto incluye una API RESTful completa con autenticación JWT que expone todos los recursos del sistema en formato JSON. La API está completamente documentada y lista para integrarse con aplicaciones externas (frontend React, aplicaciones móviles, etc.).

### **🔑 Características de la API:**
- ✅ **Autenticación JWT**: Tokens de acceso (60 min) y refresh (1 día)
- ✅ **Endpoints RESTful**: CRUD completo para todas las entidades
- ✅ **Permisos Granulares**: Públicos para consultas, protegidos para modificaciones
- ✅ **Paginación**: 10 elementos por página por defecto
- ✅ **Filtrado y Búsqueda**: Filtros por estado, categoría, servicio, etc.
- ✅ **Validaciones**: Validaciones de negocio en todos los serializers
- ✅ **Códigos HTTP**: Respuestas con códigos HTTP estándar (200, 201, 400, 401, 404)
- ✅ **Tests Completos**: 20 tests unitarios que validan toda la funcionalidad

### **🚀 Configuración de la API**

La API está configurada en `/api/` con las siguientes características:

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}
```

---

### **📍 Endpoints de la API**

#### **🔐 Autenticación (público)**

##### **Obtener Token JWT**
```bash
POST /api/auth/login/
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}

# Respuesta (200 OK)
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

##### **Renovar Token de Acceso**
```bash
POST /api/auth/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}

# Respuesta (200 OK)
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

##### **Verificar Token**
```bash
POST /api/auth/verify/
Content-Type: application/json

{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}

# Respuesta (200 OK)
{}
```

##### **Registro de Usuario**
```bash
POST /api/auth/register/
Content-Type: application/json

{
  "run": "12345678-9",
  "nombre": "Juan",
  "paterno": "Pérez",
  "materno": "González",
  "correo": "juan@example.com",
  "contrasenia": "Password123!",
  "telefono": "+56912345678",
  "fecha_nacimiento": "1990-01-01",
  "tipo_usuario": 1
}

# Respuesta (201 Created)
{
  "message": "Usuario registrado exitosamente",
  "usuario": {
    "id": 1,
    "nombre": "Juan Pérez González",
    "correo": "juan@example.com"
  }
}
```

---

#### **🌐 Servicios (GET público, modificaciones requieren JWT)**

##### **Listar Servicios**
```bash
GET /api/servicios/

# Respuesta (200 OK)
{
  "count": 6,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "nombre": "Alimentación transportada",
      "imagen": "http://localhost:8000/media/transporte.png",
      "servicio_tipo": "transportado",
      "descripcion": "Servicio de alimentación con transporte a domicilio",
      "estado": "1"
    }
  ]
}
```

##### **Obtener Servicio por ID**
```bash
GET /api/servicios/1/

# Respuesta (200 OK)
{
  "id": 1,
  "nombre": "Alimentación transportada",
  "imagen": "http://localhost:8000/media/transporte.png",
  "servicio_tipo": "transportado",
  "descripcion": "Servicio de alimentación con transporte a domicilio",
  "estado": "1"
}
```

##### **Crear Servicio (requiere JWT)**
```bash
POST /api/servicios/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "nombre": "Catering Empresarial",
  "servicio_tipo": "catering-empresarial",
  "descripcion": "Servicio de catering para eventos empresariales",
  "estado": "1"
}

# Respuesta (201 Created)
{
  "id": 7,
  "nombre": "Catering Empresarial",
  "imagen": null,
  "servicio_tipo": "catering-empresarial",
  "descripcion": "Servicio de catering para eventos empresariales",
  "estado": "1"
}
```

##### **Actualizar Servicio (requiere JWT)**
```bash
PUT /api/servicios/7/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "nombre": "Catering Corporativo",
  "servicio_tipo": "catering-corporativo",
  "descripcion": "Servicio actualizado",
  "estado": "1"
}

# Respuesta (200 OK)
```

##### **Eliminar Servicio (requiere JWT)**
```bash
DELETE /api/servicios/7/
Authorization: Bearer <access_token>

# Respuesta (204 No Content)
```

##### **Filtrar Servicios por Estado**
```bash
GET /api/servicios/?estado=1

# Respuesta: Solo servicios activos
```

---

#### **📦 Productos Web (GET público, modificaciones requieren JWT)**

##### **Listar Productos Web**
```bash
GET /api/productos-web/

# Respuesta (200 OK)
{
  "count": 31,
  "next": "http://localhost:8000/api/productos-web/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "nombre": "Almuerzo tradicional",
      "descripcion": "Comida casera tradicional chilena",
      "precio": 4500,
      "imagen": "http://localhost:8000/media/Pasta%20al%20pesto.png",
      "categoria": 1,
      "categoria_nombre": "Almuerzos",
      "servicio": 1,
      "servicio_nombre": "Alimentación transportada"
    }
  ]
}
```

##### **Filtrar Productos por Servicio**
```bash
GET /api/productos-web/?servicio=1

# Respuesta: Solo productos del servicio con ID 1
```

##### **Filtrar Productos por Categoría**
```bash
GET /api/productos-web/?categoria=2

# Respuesta: Solo productos de la categoría con ID 2
```

---

#### **👥 Usuarios (requiere JWT)**

##### **Listar Usuarios**
```bash
GET /api/usuarios/
Authorization: Bearer <access_token>

# Respuesta (200 OK)
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "run": "12345678-9",
      "nombre": "Juan",
      "paterno": "Pérez",
      "materno": "González",
      "correo": "juan@example.com",
      "telefono": "+56912345678",
      "fecha_nacimiento": "1990-01-01",
      "fecha_registro": "2024-12-14T10:00:00Z",
      "estado": "1",
      "tipo_usuario": 1,
      "tipo_usuario_nombre": "Cliente",
      "nombre_completo": "Juan Pérez González"
    }
  ]
}
```

##### **Obtener Usuario por ID**
```bash
GET /api/usuarios/1/
Authorization: Bearer <access_token>

# Respuesta (200 OK)
```

##### **Crear Usuario**
```bash
POST /api/usuarios/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "run": "98765432-1",
  "nombre": "María",
  "paterno": "González",
  "materno": "López",
  "correo": "maria@example.com",
  "contrasenia": "Password123!",
  "telefono": "+56987654321",
  "fecha_nacimiento": "1995-05-15",
  "tipo_usuario": 1,
  "estado": "1"
}

# Respuesta (201 Created)
```

##### **Actualizar Usuario**
```bash
PUT /api/usuarios/1/
Authorization: Bearer <access_token>
Content-Type: application/json

# Respuesta (200 OK)
```

##### **Eliminar Usuario**
```bash
DELETE /api/usuarios/1/
Authorization: Bearer <access_token>

# Respuesta (204 No Content)
```

---

#### **💰 Ventas (requiere JWT)**

##### **Listar Ventas**
```bash
GET /api/ventas/
Authorization: Bearer <access_token>

# Respuesta (200 OK)
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "fecha_venta": "2024-12-14",
      "estado": "1",
      "tipo_venta": "p",
      "monto_total": 15000,
      "usuario": 1,
      "usuario_nombre": "Juan Pérez González",
      "detalles": [
        {
          "id": 1,
          "producto": 1,
          "producto_nombre": "Almuerzo",
          "precio_unitario": 5000,
          "cantidad": 3,
          "subtotal": 15000
        }
      ]
    }
  ]
}
```

##### **Crear Venta con Detalles**
```bash
POST /api/ventas/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "fecha_venta": "2024-12-14",
  "estado": "1",
  "tipo_venta": "p",
  "monto_total": 10000,
  "usuario": 1,
  "detalles": [
    {
      "producto": 1,
      "precio_unitario": 5000,
      "cantidad": 2
    }
  ]
}

# Respuesta (201 Created)
```

##### **Filtrar Ventas por Estado**
```bash
GET /api/ventas/?estado=1
Authorization: Bearer <access_token>

# Respuesta: Solo ventas pendientes
```

##### **Filtrar Ventas por Usuario**
```bash
GET /api/ventas/?usuario=1
Authorization: Bearer <access_token>

# Respuesta: Solo ventas del usuario con ID 1
```

---

#### **📦 Productos Inventario (requiere JWT)**

##### **Listar Productos Inventario**
```bash
GET /api/productos/
Authorization: Bearer <access_token>

# Respuesta (200 OK)
{
  "count": 31,
  "results": [
    {
      "id": 1,
      "nombre": "Almuerzo Ejecutivo",
      "descripcion": "Almuerzo completo",
      "precio": 5000,
      "stock": 50,
      "imagen": "http://localhost:8000/media/producto.png",
      "categoria_id": 1,
      "categoria_nombre": "Almuerzos",
      "categoria_web_id": 1,
      "categoria_web_nombre": "Almuerzos",
      "servicio_id": 1,
      "servicio_nombre": "Alimentación transportada"
    }
  ]
}
```

---

#### **📂 Categorías y Tipos de Usuario**

##### **Tipos de Usuario (requiere JWT)**
```bash
GET /api/tipos-usuario/
Authorization: Bearer <access_token>

POST /api/tipos-usuario/
Authorization: Bearer <access_token>
```

##### **Categorías Web (GET público)**
```bash
GET /api/categorias-web/
```

##### **Categorías Inventario (requiere JWT)**
```bash
GET /api/categorias/
Authorization: Bearer <access_token>
```

---

### **🧪 Tests de la API**

El proyecto incluye 20 tests completos que validan toda la funcionalidad de la API:

```bash
# Ejecutar todos los tests
python manage.py test api

# Ejecutar tests específicos
python manage.py test api.tests.JWTAuthenticationTestCase
python manage.py test api.tests.ServicioAPITestCase
python manage.py test api.tests.VentaAPITestCase
```

**Tests incluidos:**
- ✅ Autenticación JWT (login, refresh, verify)
- ✅ Endpoints públicos sin autenticación
- ✅ Endpoints protegidos con JWT
- ✅ Filtrado y paginación
- ✅ Validaciones de datos
- ✅ Códigos HTTP correctos
- ✅ CRUD completo para todas las entidades

---

### **📝 Códigos de Estado HTTP**

| Código | Significado | Uso en la API |
|--------|-------------|---------------|
| 200 OK | Petición exitosa | GET, PUT, PATCH |
| 201 Created | Recurso creado | POST |
| 204 No Content | Eliminación exitosa | DELETE |
| 400 Bad Request | Datos inválidos | Validación fallida |
| 401 Unauthorized | Sin autenticación | JWT inválido o ausente |
| 403 Forbidden | Sin permisos | Falta de permisos |
| 404 Not Found | Recurso no existe | ID inexistente |
| 500 Server Error | Error del servidor | Error interno |

---

### **🔒 Seguridad de la API**

- ✅ **Autenticación JWT**: Tokens seguros con expiración
- ✅ **Permisos Granulares**: Control de acceso por endpoint
- ✅ **Validaciones**: Sanitización de datos de entrada
- ✅ **HTTPS**: Recomendado para producción
- ✅ **CORS**: Configurable para frontend externo
- ✅ **Rate Limiting**: Recomendado para producción

---

### **🌐 Integración con Frontend**

#### **Ejemplo con JavaScript (Fetch API)**

```javascript
// Obtener token JWT
async function login(username, password) {
  const response = await fetch('http://localhost:8000/api/auth/login/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ username, password }),
  });
  const data = await response.json();
  localStorage.setItem('access_token', data.access);
  localStorage.setItem('refresh_token', data.refresh);
  return data;
}

// Obtener servicios (público)
async function getServicios() {
  const response = await fetch('http://localhost:8000/api/servicios/');
  return await response.json();
}

// Crear usuario (protegido)
async function createUsuario(userData) {
  const token = localStorage.getItem('access_token');
  const response = await fetch('http://localhost:8000/api/usuarios/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify(userData),
  });
  return await response.json();
}
```

#### **Ejemplo con Python (Requests)**

```python
import requests

# Login
response = requests.post('http://localhost:8000/api/auth/login/', json={
    'username': 'admin',
    'password': 'admin123'
})
tokens = response.json()
access_token = tokens['access']

# Obtener servicios
response = requests.get('http://localhost:8000/api/servicios/')
servicios = response.json()

# Crear venta (con autenticación)
headers = {'Authorization': f'Bearer {access_token}'}
response = requests.post('http://localhost:8000/api/ventas/', 
    headers=headers,
    json={
        'fecha_venta': '2024-12-14',
        'estado': '1',
        'tipo_venta': 'p',
        'monto_total': 10000,
        'usuario': 1,
        'detalles': [
            {'producto': 1, 'precio_unitario': 5000, 'cantidad': 2}
        ]
    }
)
```

---

### **📦 Paquetes Instalados para la API**

```txt
djangorestframework>=3.14.0
djangorestframework-simplejwt>=5.3.0
django-filter>=25.0
```

---

<div align="center">
   <b>🎉 ¡Proyecto GM-Express completado exitosamente! 🎉</b>
   <br/>
   <i>Desarrollado con Django 5.2.7 • Django REST Framework • JWT • Bootstrap 5 • SQLite/MySQL</i>
</div>
   <img src="static/images/servicio.png" alt="Servicio GM Express" width="120"/>
</div>
