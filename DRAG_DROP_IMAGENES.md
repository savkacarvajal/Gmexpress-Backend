# Sistema de Carga de Imágenes con Drag & Drop

## Resumen de Implementación

Se ha implementado un sistema completo de carga de imágenes con funcionalidad de **arrastrar y soltar (drag & drop)** en los formularios de Servicios y Productos de GM-Express.

## ✅ Cambios Realizados

### 1. JavaScript - `static/JS/image-upload.js`
**Archivo creado con funcionalidad completa:**
- ✅ Detección automática de campos de imagen (`input[type="file"][accept="image/*"]`)
- ✅ Zona visual de arrastrar y soltar con retroalimentación visual
- ✅ Botón "Elegir archivo" para selección manual
- ✅ Vista previa de la imagen seleccionada
- ✅ Validación de tipo de archivo (solo imágenes)
- ✅ Validación de tamaño (máximo 5MB)
- ✅ Botón para remover imagen seleccionada
- ✅ Efectos visuales durante el arrastre (drag-over)

### 2. CSS - `static/CSS/style.css`
**Estilos agregados al final del archivo:**
- ✅ Diseño responsive para la zona de drop
- ✅ Colores del tema verde de GM-Express (#28a745)
- ✅ Animaciones suaves (transiciones y fadeIn)
- ✅ Estilos para vista previa de imagen
- ✅ Estados hover y drag-over
- ✅ Diseño de botones consistente con el resto del sitio

**Corrección adicional:** Se arregló un error de sintaxis CSS en la regla `main` (líneas 308-315)

### 3. Formularios Actualizados

#### `catalogo/forms.py`
**Cambios en `ServicioForm`:**
```python
# ANTES:
'imagen': forms.TextInput(attrs={
    'class': 'form-control',
    'placeholder': 'Ej: catering.jpg (debe existir en static/images/)'
})

# DESPUÉS:
'imagen': forms.FileInput(attrs={
    'class': 'form-control',
    'accept': 'image/*'
})
```

**Cambios en `ProductoWebForm`:**
- Widget cambiado de `TextInput` a `FileInput`
- Label actualizado de "Nombre del Archivo de Imagen" a "Imagen del Producto"

#### `catalogue/forms.py`
**Cambios en `ProductoForm`:**
```python
# ANTES:
'imagen': forms.TextInput(attrs={
    'class': 'form-control',
    'placeholder': 'Ej: producto.jpg (debe existir en static/images/)'
})

# DESPUÉS:
'imagen': forms.FileInput(attrs={
    'class': 'form-control',
    'accept': 'image/*'
})
```
- Label actualizado de "Nombre del Archivo de Imagen" a "Imagen del Producto"

### 4. Templates Actualizados

#### `templates/templateCatalogue/producto_form.html`
**Cambios realizados:**
```django
{% load static %}  <!-- Agregado -->

{% block extra_css %}
<link rel="stylesheet" href="{% static 'CSS/style.css' %}">
{% endblock %}

<form method="post" enctype="multipart/form-data">  <!-- enctype agregado -->
    ...
</form>

{% block extra_js %}
<script src="{% static 'JS/image-upload.js' %}"></script>
{% endblock %}
```

#### `templates/templateCatalogo/servicio_form.html`
**Mismos cambios que producto_form.html**

### 5. Vistas Actualizadas

#### `catalogo/views.py`
**Funciones modificadas:**
```python
# servicio_crear
form = ServicioForm(request.POST, request.FILES)  # request.FILES agregado

# servicio_editar
form = ServicioForm(request.POST, request.FILES, instance=servicio)  # request.FILES agregado
```

#### `catalogue/views.py`
**Funciones modificadas:**
```python
# producto_crear
form = ProductoForm(request.POST, request.FILES)  # request.FILES agregado

# producto_editar
form = ProductoForm(request.POST, request.FILES, instance=producto)  # request.FILES agregado
```

## 🎯 Funcionalidades Implementadas

### Para el Usuario:
1. **Arrastrar y Soltar**
   - Arrastra una imagen desde tu explorador de archivos
   - Suelta en la zona marcada con borde verde punteado
   - Retroalimentación visual inmediata

2. **Selección Manual**
   - Click en "Elegir archivo"
   - Selecciona desde el explorador de archivos del sistema

3. **Vista Previa**
   - Muestra la imagen seleccionada antes de guardar
   - Permite verificar que es la imagen correcta

4. **Remover Imagen**
   - Botón "Remover imagen" para cancelar la selección
   - Vuelve a mostrar la zona de drop

5. **Validaciones**
   - Solo acepta archivos de imagen (JPG, PNG, GIF, etc.)
   - Tamaño máximo: 5MB
   - Mensajes de error claros

### Estados Visuales:
- **Normal**: Zona con borde punteado verde
- **Hover**: Fondo verde claro (#e9f7ef)
- **Arrastrando sobre la zona**: Fondo verde más intenso (#d4edda), borde sólido, escala aumentada
- **Imagen seleccionada**: Vista previa grande, zona de drop oculta

## 📁 Configuración Existente Verificada

### `gmexpress/settings.py`
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```
✅ Ya está configurado correctamente

### `gmexpress/urls.py`
```python
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```
✅ URLs de media ya servidas en desarrollo

### Modelos
```python
# catalogo/models.py - Servicio
imagen = models.ImageField(upload_to='servicios/', default='servicios/default.jpg')

# catalogo/models.py - Producto
imagen = models.ImageField(upload_to='productos/', default='productos/default.jpg')

# catalogue/models.py - Producto
imagen = models.ImageField(upload_to='productos/', default='productos/default.jpg')
```
✅ ImageField ya definidos correctamente

## 🚀 Cómo Usar

1. **Iniciar el servidor:**
   ```bash
   python manage.py runserver
   ```

2. **Navegar a:**
   - Crear/Editar Producto: `/productos/crear/` o `/productos/<id>/editar/`
   - Crear/Editar Servicio: `/servicios/crear/` o `/servicios/<id>/editar/`

3. **Cargar una imagen:**
   - **Opción 1 (Drag & Drop):** Arrastra la imagen desde tu carpeta y suéltala en la zona marcada
   - **Opción 2 (Manual):** Click en "Elegir archivo" y selecciona desde el explorador

4. **Verificar:**
   - La vista previa aparecerá inmediatamente
   - Completa el resto del formulario
   - Click en "Guardar"

5. **Las imágenes se guardan en:**
   - Servicios: `media/servicios/`
   - Productos: `media/productos/`

## 🎨 Diseño Visual

- **Colores**: Verde GM-Express (#28a745)
- **Iconos**: Font Awesome (cloud-upload, folder-open, trash)
- **Animaciones**: Transiciones suaves de 0.3s
- **Responsive**: Funciona en todos los tamaños de pantalla
- **Consistencia**: Mantiene el estilo Bootstrap 5 del resto del sitio

## 📝 Notas Importantes

1. **Compatibilidad:** Compatible con navegadores modernos (Chrome, Firefox, Edge, Safari)
2. **JavaScript requerido:** La funcionalidad drag & drop requiere JavaScript habilitado
3. **Fallback:** Si JavaScript está deshabilitado, el input file estándar sigue funcionando
4. **Validación del servidor:** Django valida el tipo y tamaño en el backend
5. **PIL/Pillow:** Asegúrate de tener Pillow instalado (`pip install Pillow`) para ImageField

## 🔄 Migración desde el Sistema Antiguo

**Sistema Anterior:**
- Campo de texto para nombre de archivo
- Imágenes debían existir previamente en `static/images/`
- Sin validación de tipo
- Sin vista previa

**Sistema Nuevo:**
- Carga directa de archivos
- Imágenes se almacenan en `media/servicios/` y `media/productos/`
- Validación automática de tipo y tamaño
- Vista previa instantánea
- Interfaz drag & drop intuitiva

## ✅ Testing Recomendado

- [ ] Crear un nuevo servicio con imagen
- [ ] Editar un servicio existente cambiando la imagen
- [ ] Crear un nuevo producto con imagen
- [ ] Editar un producto existente cambiando la imagen
- [ ] Probar drag & drop
- [ ] Probar selección manual
- [ ] Verificar validación de tipo (intentar subir PDF, TXT, etc.)
- [ ] Verificar validación de tamaño (archivo > 5MB)
- [ ] Verificar vista previa
- [ ] Verificar botón de remover imagen
- [ ] Verificar guardado correcto en base de datos
- [ ] Verificar que las imágenes se muestren en los listados

## 🐛 Posibles Problemas y Soluciones

**Problema:** Las imágenes no se cargan
- **Solución:** Verificar que Pillow esté instalado: `pip install Pillow`

**Problema:** Error 500 al subir imagen
- **Solución:** Verificar permisos de escritura en carpeta `media/`

**Problema:** La vista previa no aparece
- **Solución:** Verificar que `static/JS/image-upload.js` se está cargando correctamente

**Problema:** CSS no se aplica
- **Solución:** Ejecutar `python manage.py collectstatic` o verificar STATIC_URL

---

**Fecha de implementación:** 10 de noviembre de 2025  
**Desarrollado para:** GM-Express Backend Django 5.2.7
