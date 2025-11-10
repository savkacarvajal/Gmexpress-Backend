# Configuración AWS S3 para Sistema de Carga de Imágenes
## GM-Express - Guía de Despliegue con PuTTY

Esta guía te ayudará a configurar el sistema de carga de imágenes con drag & drop en AWS, usando PuTTY para conectarte a tu instancia EC2.

---

## 📋 Requisitos Previos

### En tu PC Local:
- ✅ PuTTY instalado
- ✅ Clave privada `.ppk` para conectarte a EC2
- ✅ FileZilla o WinSCP para transferir archivos (opcional)

### En AWS:
- ✅ Cuenta de AWS activa
- ✅ Instancia EC2 corriendo (Amazon Linux 2 o Ubuntu)
- ✅ Elastic Beanstalk configurado (opcional)

---

## 🎯 PASO 1: Crear Bucket S3 para Imágenes

### 1.1 Crear el Bucket

1. Ingresa a **AWS Console** → **S3**
2. Click en **"Create bucket"**
3. Configuración:
   - **Bucket name**: `gmexpress-media` (o el nombre que prefieras)
   - **AWS Region**: `us-east-1` (o tu región preferida)
   - **Block Public Access**: **DESMARCAR** "Block all public access"
     - ⚠️ Marca el checkbox de confirmación (las imágenes deben ser públicas)
   - **Bucket Versioning**: Disabled (opcional)
   - **Tags**: (opcional) Key: `Project`, Value: `GM-Express`
4. Click **"Create bucket"**

### 1.2 Configurar Política del Bucket (Bucket Policy)

1. Ingresa al bucket recién creado
2. Ve a la pestaña **"Permissions"**
3. En **"Bucket policy"**, click **"Edit"**
4. Pega esta política (reemplaza `gmexpress-media` con tu nombre de bucket):

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::gmexpress-media/*"
        }
    ]
}
```

5. Click **"Save changes"**

### 1.3 Configurar CORS del Bucket

1. En la misma pestaña **"Permissions"**
2. Baja hasta **"Cross-origin resource sharing (CORS)"**
3. Click **"Edit"**
4. Pega esta configuración:

```json
[
    {
        "AllowedHeaders": [
            "*"
        ],
        "AllowedMethods": [
            "GET",
            "POST",
            "PUT",
            "DELETE",
            "HEAD"
        ],
        "AllowedOrigins": [
            "*"
        ],
        "ExposeHeaders": [
            "ETag"
        ],
        "MaxAgeSeconds": 3000
    }
]
```

5. Click **"Save changes"**

---

## 🔑 PASO 2: Crear Usuario IAM con Permisos S3

### 2.1 Crear Usuario IAM

1. Ve a **AWS Console** → **IAM** → **Users**
2. Click **"Add users"**
3. **User name**: `gmexpress-s3-user`
4. **Access type**: Marca **"Programmatic access"**
5. Click **"Next: Permissions"**

### 2.2 Asignar Permisos

**Opción A: Política Personalizada (Recomendado - Más Seguro)**

1. Click **"Attach existing policies directly"**
2. Click **"Create policy"**
3. En la pestaña **JSON**, pega:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:DeleteObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::gmexpress-media",
                "arn:aws:s3:::gmexpress-media/*"
            ]
        }
    ]
}
```

4. Click **"Next: Tags"** → **"Next: Review"**
5. **Name**: `GMExpressS3Policy`
6. Click **"Create policy"**
7. Vuelve a la pestaña anterior, refresca y selecciona `GMExpressS3Policy`

**Opción B: Política AWS (Más Rápido - Menos Seguro)**

1. Busca y selecciona: **`AmazonS3FullAccess`**

### 2.3 Guardar Credenciales

1. Click **"Next: Tags"** → **"Next: Review"** → **"Create user"**
2. **⚠️ IMPORTANTE**: Guarda estas credenciales en un lugar seguro:
   - **Access key ID**: `AKIA...` 
   - **Secret access key**: `wJalrXUtn...`
   
   **Nunca las compartas ni las subas a GitHub!**

3. Click **"Download .csv"** para backup
4. Click **"Close"**

---

## 🖥️ PASO 3: Conectar con PuTTY y Configurar Variables de Entorno

### 3.1 Conectar a tu Instancia EC2 con PuTTY

1. Abre **PuTTY**
2. En **"Host Name"**: `ec2-user@tu-ip-publica.compute.amazonaws.com`
3. En **"Port"**: `22`
4. En el panel izquierdo: **Connection** → **SSH** → **Auth**
5. En **"Private key file"**: Browse y selecciona tu archivo `.ppk`
6. Vuelve a **Session**, guarda la configuración
7. Click **"Open"**

### 3.2 Configurar Variables de Entorno

Una vez conectado vía SSH, ejecuta estos comandos:

```bash
# Navegar al directorio de tu proyecto
cd /var/app/current/  # O la ruta donde está tu proyecto

# Editar el archivo de configuración de Elastic Beanstalk
sudo nano .ebextensions/django.config
```

Si el archivo no existe, créalo con:

```bash
mkdir -p .ebextensions
sudo nano .ebextensions/django.config
```

Pega este contenido (reemplaza con tus valores):

```yaml
option_settings:
  aws:elasticbeanstalk:application:environment:
    DJANGO_SETTINGS_MODULE: "gmexpress.settings"
    PYTHONPATH: "/var/app/current:$PYTHONPATH"
    AWS_ACCESS_KEY_ID: "TU_ACCESS_KEY_ID_AQUI"
    AWS_SECRET_ACCESS_KEY: "TU_SECRET_ACCESS_KEY_AQUI"
    AWS_STORAGE_BUCKET_NAME: "gmexpress-media"
    AWS_S3_REGION_NAME: "us-east-1"
```

**Guarda el archivo**: `Ctrl+X` → `Y` → `Enter`

### 3.3 Método Alternativo - Variables de Entorno en AWS Console

Si prefieres usar la interfaz web:

1. Ve a **Elastic Beanstalk** → Tu aplicación → **Configuration**
2. En **Software**, click **"Edit"**
3. Baja hasta **"Environment properties"**
4. Agrega cada variable:

| Name                      | Value                           |
|---------------------------|---------------------------------|
| `AWS_ACCESS_KEY_ID`       | Tu Access Key ID               |
| `AWS_SECRET_ACCESS_KEY`   | Tu Secret Access Key           |
| `AWS_STORAGE_BUCKET_NAME` | `gmexpress-media`              |
| `AWS_S3_REGION_NAME`      | `us-east-1`                    |

5. Click **"Apply"**

---

## 📤 PASO 4: Subir Archivos al Servidor con PuTTY/SFTP

### Opción A: Usar WinSCP (Recomendado)

1. Descarga **WinSCP**: https://winscp.net/
2. Abre WinSCP
3. Configuración:
   - **File protocol**: `SFTP`
   - **Host name**: Tu IP pública de EC2
   - **Port**: `22`
   - **User name**: `ec2-user` (o `ubuntu` si usas Ubuntu)
4. Click **"Advanced"** → **"SSH"** → **"Authentication"**
5. En **"Private key file"**: Selecciona tu `.ppk`
6. Click **"OK"** → **"Login"**
7. Arrastra los archivos modificados a `/var/app/current/`

### Opción B: Usar PSCP (PuTTY SCP)

Desde tu PC local (CMD o PowerShell):

```powershell
# Navegar a la carpeta de tu proyecto
cd "C:\Users\savka\OneDrive - INACAP\Escritorio\Backend\Savka\Gmexpress-Backend"

# Subir archivos específicos
pscp -i "C:\ruta\a\tu\clave.ppk" requirements.txt ec2-user@tu-ip:/var/app/current/
pscp -i "C:\ruta\a\tu\clave.ppk" gmexpress\settings.py ec2-user@tu-ip:/var/app/current/gmexpress/
pscp -i "C:\ruta\a\tu\clave.ppk" static\JS\image-upload.js ec2-user@tu-ip:/var/app/current/static/JS/
pscp -i "C:\ruta\a\tu\clave.ppk" static\CSS\style.css ec2-user@tu-ip:/var/app/current/static/CSS/
```

### Opción C: Clonar desde GitHub

Si subes tu proyecto a GitHub:

```bash
# En tu servidor via PuTTY
cd /var/app/current/
git pull origin main
```

---

## 🔧 PASO 5: Instalar Dependencias en el Servidor

Conectado via PuTTY, ejecuta:

```bash
# Activar entorno virtual (si usas uno)
source /var/app/venv/*/bin/activate

# O si usas virtualenv directamente:
# source venv/bin/activate

# Instalar nuevas dependencias
pip install -r requirements.txt

# Verificar que Pillow, boto3 y django-storages estén instalados
pip list | grep -E 'Pillow|boto3|django-storages'
```

Deberías ver:
```
boto3                1.34.14
django-storages      1.14.2
Pillow               10.1.0
```

---

## 🚀 PASO 6: Recolectar Archivos Estáticos y Migrar

```bash
# Recolectar archivos estáticos (CSS, JS)
python manage.py collectstatic --noinput

# Aplicar migraciones
python manage.py migrate

# Crear superusuario (si no tienes)
python manage.py createsuperuser
```

---

## 🔄 PASO 7: Reiniciar la Aplicación

### Si usas Elastic Beanstalk:

```bash
# Desde tu PC local con EB CLI
eb deploy

# O desde AWS Console:
# Elastic Beanstalk → Tu ambiente → Actions → Restart app server(s)
```

### Si usas EC2 con Gunicorn:

```bash
# Reiniciar el servicio
sudo systemctl restart gunicorn

# O si usas supervisor
sudo supervisorctl restart gmexpress
```

### Si usas Apache/nginx:

```bash
# Apache
sudo systemctl restart apache2

# nginx
sudo systemctl restart nginx
```

---

## ✅ PASO 8: Verificar que Funciona

### 8.1 Probar Localmente Primero

En tu PC local:

```powershell
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
python manage.py runserver
```

Visita: `http://127.0.0.1:8000/productos/crear/`

- Arrastra una imagen
- Verifica que aparezca la vista previa
- Click "Guardar"
- La imagen debe guardarse en `media/productos/`

### 8.2 Probar en Producción AWS

1. Visita tu URL de AWS: `http://tu-aplicacion.elasticbeanstalk.com/productos/crear/`
2. Arrastra una imagen
3. Click "Guardar"
4. Verifica en S3:
   - Ve a tu bucket `gmexpress-media`
   - Deberías ver una carpeta `productos/` con la imagen subida
5. La imagen debería mostrarse en la lista de productos

---

## 🐛 Solución de Problemas

### Error: "Access Denied" al subir imagen

**Causa**: Credenciales incorrectas o permisos insuficientes

**Solución**:
```bash
# Verificar variables de entorno
echo $AWS_ACCESS_KEY_ID
echo $AWS_STORAGE_BUCKET_NAME

# Si están vacías, agregarlas manualmente
export AWS_ACCESS_KEY_ID="tu_key_aqui"
export AWS_SECRET_ACCESS_KEY="tu_secret_aqui"
export AWS_STORAGE_BUCKET_NAME="gmexpress-media"
```

### Error: "No module named 'storages'"

**Causa**: django-storages no instalado

**Solución**:
```bash
pip install django-storages boto3
```

### Error: "Bucket does not exist"

**Causa**: Nombre de bucket incorrecto o no creado

**Solución**:
1. Verifica el nombre en S3 Console
2. Asegúrate de que `AWS_STORAGE_BUCKET_NAME` sea correcto
3. El bucket debe existir ANTES de subir archivos

### Las imágenes no se muestran (404)

**Causa**: Bucket no es público o política incorrecta

**Solución**:
1. Verifica la Bucket Policy (Paso 1.2)
2. Verifica que "Block all public access" esté desactivado
3. Verifica la URL de la imagen en S3: debe ser accesible desde el navegador

### Error: "Connection timeout" al subir

**Causa**: Security Group de EC2 no permite tráfico HTTPS a S3

**Solución**:
1. Ve a **EC2** → **Security Groups**
2. Selecciona el security group de tu instancia
3. Agrega regla **Outbound**:
   - Type: `HTTPS`
   - Protocol: `TCP`
   - Port: `443`
   - Destination: `0.0.0.0/0`

---

## 📊 Monitoreo y Logs

### Ver logs en tiempo real con PuTTY:

```bash
# Logs de aplicación
sudo tail -f /var/log/eb-engine.log

# Logs de web server
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/httpd/error_log

# Logs de Python
sudo tail -f /var/log/web.stdout.log
```

### Comandos útiles de diagnóstico:

```bash
# Ver estado del servidor
sudo systemctl status gunicorn

# Ver procesos Python
ps aux | grep python

# Ver uso de disco
df -h

# Ver memoria
free -m

# Verificar conexión a S3
aws s3 ls s3://gmexpress-media/ --region us-east-1
```

---

## 💰 Consideraciones de Costos AWS

### Costos Aproximados (us-east-1):

- **S3 Storage**: $0.023 por GB/mes
  - 1,000 imágenes (~100MB): ~$0.002/mes
- **S3 Requests**: 
  - PUT/POST: $0.005 por 1,000 requests
  - GET: $0.0004 por 1,000 requests
- **Data Transfer**: Primeros 100 GB/mes gratis

**Ejemplo**: 10,000 imágenes subidas/mes + 50,000 visualizaciones = ~$0.50/mes

### Recomendaciones para Optimizar Costos:

1. **Usar CloudFront CDN**: Reduce costos de transferencia
2. **Lifecycle Policies**: Eliminar imágenes antiguas automáticamente
3. **Compresión**: Comprimir imágenes antes de subir
4. **Intelligent Tiering**: Para archivos poco accedidos

---

## 🔐 Seguridad - Best Practices

### ✅ Hacer:
- Usar variables de entorno para credenciales
- Rotar Access Keys cada 90 días
- Usar políticas IAM restrictivas (solo permisos S3 necesarios)
- Habilitar CloudTrail para auditoría
- Usar HTTPS siempre

### ❌ NO Hacer:
- Hardcodear credenciales en settings.py
- Subir `.env` o `settings.py` con credenciales a GitHub
- Usar `AmazonS3FullAccess` en producción
- Dejar buckets completamente públicos (solo los objetos)

---

## 📚 Archivos de Referencia

### Archivos Modificados en este Sistema:
```
✅ requirements.txt           (Agregado Pillow, boto3, django-storages)
✅ gmexpress/settings.py      (Agregado configuración S3)
✅ static/JS/image-upload.js  (Nuevo - Drag & drop)
✅ static/CSS/style.css       (Agregado estilos drag & drop)
✅ catalogo/forms.py          (FileInput en vez de TextInput)
✅ catalogue/forms.py         (FileInput en vez de TextInput)
✅ catalogo/views.py          (request.FILES agregado)
✅ catalogue/views.py         (request.FILES agregado)
✅ templates/.../producto_form.html (enctype multipart)
✅ templates/.../servicio_form.html (enctype multipart)
```

---

## 📞 Soporte y Recursos

- **Documentación django-storages**: https://django-storages.readthedocs.io/
- **Documentación boto3**: https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
- **AWS S3 Console**: https://s3.console.aws.amazon.com/
- **IAM Console**: https://console.aws.amazon.com/iam/

---

**Fecha de creación**: 10 de noviembre de 2025  
**Versión**: 1.0  
**Proyecto**: GM-Express Backend Django 5.2.7  
**Autor**: Sistema de carga de imágenes con drag & drop
