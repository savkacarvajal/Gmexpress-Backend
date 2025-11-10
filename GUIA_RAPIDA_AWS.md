# 🚀 Guía Rápida de Despliegue AWS con PuTTY

## Pasos Esenciales

### 1️⃣ Crear Bucket S3
```
- Nombre: gmexpress-media
- Región: us-east-1
- Block Public Access: DESACTIVAR
- Bucket Policy: Permitir public-read
```

### 2️⃣ Crear Usuario IAM
```
- Nombre: gmexpress-s3-user
- Permisos: AmazonS3FullAccess (o política personalizada)
- Guardar: Access Key ID + Secret Access Key
```

### 3️⃣ Conectar con PuTTY
```powershell
Host: ec2-user@tu-ip.compute.amazonaws.com
Port: 22
Auth: Tu archivo .ppk
```

### 4️⃣ Configurar Variables de Entorno
```bash
# Opción A: Via archivo .ebextensions/django.config
mkdir -p .ebextensions
nano .ebextensions/django.config
```

```yaml
option_settings:
  aws:elasticbeanstalk:application:environment:
    AWS_ACCESS_KEY_ID: "TU_KEY_AQUI"
    AWS_SECRET_ACCESS_KEY: "TU_SECRET_AQUI"
    AWS_STORAGE_BUCKET_NAME: "gmexpress-media"
    AWS_S3_REGION_NAME: "us-east-1"
```

```bash
# Opción B: Via Elastic Beanstalk Console
# Configuration → Software → Environment properties
```

### 5️⃣ Subir Archivos Actualizados
```powershell
# Con WinSCP (recomendado)
# O con PSCP:
pscp -i tu-clave.ppk requirements.txt ec2-user@tu-ip:/var/app/current/
pscp -i tu-clave.ppk -r static ec2-user@tu-ip:/var/app/current/
pscp -i tu-clave.ppk -r templates ec2-user@tu-ip:/var/app/current/
```

### 6️⃣ Instalar Dependencias
```bash
source /var/app/venv/*/bin/activate
pip install -r requirements.txt
```

### 7️⃣ Recolectar Estáticos y Migrar
```bash
python manage.py collectstatic --noinput
python manage.py migrate
```

### 8️⃣ Reiniciar Aplicación
```bash
# Elastic Beanstalk
eb deploy

# O
sudo systemctl restart gunicorn
```

## ✅ Verificación Rápida

1. **Local**: `python manage.py runserver` → http://127.0.0.1:8000/productos/crear/
2. **AWS**: http://tu-app.elasticbeanstalk.com/productos/crear/
3. **S3**: Verifica que la imagen aparezca en tu bucket

## 🆘 Comandos Útiles PuTTY

```bash
# Ver logs en tiempo real
sudo tail -f /var/log/eb-engine.log

# Verificar servicio
sudo systemctl status gunicorn

# Listar archivos en S3
aws s3 ls s3://gmexpress-media/

# Verificar variables de entorno
printenv | grep AWS
```

## 📁 Archivos Clave Modificados

```
✅ requirements.txt              → Pillow, boto3, django-storages
✅ gmexpress/settings.py         → Configuración S3
✅ static/JS/image-upload.js     → Drag & drop
✅ static/CSS/style.css          → Estilos
✅ catalogo/forms.py             → FileInput
✅ catalogue/forms.py            → FileInput
✅ catalogo/views.py             → request.FILES
✅ catalogue/views.py            → request.FILES
✅ templates/*/producto_form.html → enctype
✅ templates/*/servicio_form.html → enctype
```

## 💡 Tips

- **Probar localmente primero**: Menos costoso y más rápido
- **Usar WinSCP**: Más fácil que PSCP para transferir archivos
- **Variables de entorno**: Nunca hardcodear en settings.py
- **Logs**: Siempre revisar logs si algo falla

Para guía completa ver: `CONFIGURACION_AWS_S3_PUTTY.md`
