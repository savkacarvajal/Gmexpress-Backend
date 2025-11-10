
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Categoria, Producto, Servicio
from .forms import ServicioForm, CategoriaWebForm, ProductoWebForm

# ==================== VISTAS PÚBLICAS ====================

# Vista para mostrar el catálogo principal de servicios
def catalogoServicios(request):
    # Obtener todos los servicios activos
    catalogo_servicios = Servicio.objects.filter(estado='1')
    data = {
        'catalogo_servicios': catalogo_servicios,
    }
    return render(request, 'templateEmpresa/inicio.html', data)


# Vista para mostrar productos de una categoría/servicio
def catalogoProductos(request, servicio_tipo):
    # Buscar el servicio por tipo
    try:
        servicio = Servicio.objects.get(servicio_tipo=servicio_tipo, estado='1')
        # Obtener productos relacionados a ese servicio
        productos = Producto.objects.filter(servicio=servicio)
        data = {
            'catalogo_productos': productos,
            'titulo_servicio': servicio.nombre,
            'servicio_tipo': servicio_tipo,
        }
        return render(request, 'templateCatalogo/catalogo2.html', data)
    except Servicio.DoesNotExist:
        # Si el servicio no existe, redirigir al catálogo principal
        return catalogoServicios(request)


# Vista para mostrar el detalle de un producto
def catalogoMenu(request, servicio_tipo, producto_id):
    try:
        producto = get_object_or_404(Producto, pk=producto_id)
        servicio = get_object_or_404(Servicio, servicio_tipo=servicio_tipo, estado='1')
        
        data = {
            'menu_detalle': producto,
            'producto_nombre': producto.nombre,
            'producto_imagen': producto.imagen,
            'servicio_tipo': servicio_tipo,
        }
        return render(request, 'templateCatalogo/catalogo3.html', data)
    except (Producto.DoesNotExist, Servicio.DoesNotExist):
        # Si no existe el producto o servicio, redirigir al catálogo
        return catalogoServicios(request)


# ==================== CRUD SERVICIO ====================

@login_required
def servicio_lista(request):
    """Vista para listar todos los servicios"""
    servicios = Servicio.objects.all().order_by('nombre')
    context = {'servicios': servicios}
    return render(request, 'templateCatalogo/servicio_lista.html', context)


@login_required
def servicio_crear(request):
    """Vista para crear un nuevo servicio"""
    if request.method == 'POST':
        form = ServicioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Servicio creado exitosamente.')
            return redirect('servicio_lista')
    else:
        form = ServicioForm()
    
    context = {'form': form, 'accion': 'Crear'}
    return render(request, 'templateCatalogo/servicio_form.html', context)


@login_required
def servicio_editar(request, pk):
    """Vista para editar un servicio existente"""
    servicio = get_object_or_404(Servicio, pk=pk)
    
    if request.method == 'POST':
        form = ServicioForm(request.POST, request.FILES, instance=servicio)
        if form.is_valid():
            form.save()
            messages.success(request, 'Servicio actualizado exitosamente.')
            return redirect('servicio_lista')
    else:
        form = ServicioForm(instance=servicio)
    
    context = {'form': form, 'accion': 'Editar', 'servicio': servicio}
    return render(request, 'templateCatalogo/servicio_form.html', context)


@login_required
def servicio_eliminar(request, pk):
    """Vista para eliminar un servicio"""
    servicio = get_object_or_404(Servicio, pk=pk)
    
    if request.method == 'POST':
        try:
            servicio.delete()
            messages.success(request, 'Servicio eliminado exitosamente.')
        except Exception as e:
            messages.error(request, f'No se puede eliminar. Hay productos asociados. Error: {str(e)}')
        return redirect('servicio_lista')
    
    context = {'servicio': servicio}
    return render(request, 'templateCatalogo/servicio_eliminar.html', context)


# ==================== CRUD CATEGORÍA WEB ====================

@login_required
def categoria_web_lista(request):
    """Vista para listar todas las categorías web"""
    categorias = Categoria.objects.all().order_by('nombre')
    context = {'categorias': categorias}
    return render(request, 'templateCatalogo/categoria_web_lista.html', context)


@login_required
def categoria_web_crear(request):
    """Vista para crear una nueva categoría web"""
    if request.method == 'POST':
        form = CategoriaWebForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría web creada exitosamente.')
            return redirect('categoria_web_lista')
    else:
        form = CategoriaWebForm()
    
    context = {'form': form, 'accion': 'Crear'}
    return render(request, 'templateCatalogo/categoria_web_form.html', context)


@login_required
def categoria_web_editar(request, pk):
    """Vista para editar una categoría web existente"""
    categoria = get_object_or_404(Categoria, pk=pk)
    
    if request.method == 'POST':
        form = CategoriaWebForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría web actualizada exitosamente.')
            return redirect('categoria_web_lista')
    else:
        form = CategoriaWebForm(instance=categoria)
    
    context = {'form': form, 'accion': 'Editar', 'categoria': categoria}
    return render(request, 'templateCatalogo/categoria_web_form.html', context)


@login_required
def categoria_web_eliminar(request, pk):
    """Vista para eliminar una categoría web"""
    categoria = get_object_or_404(Categoria, pk=pk)
    
    if request.method == 'POST':
        try:
            categoria.delete()
            messages.success(request, 'Categoría web eliminada exitosamente.')
        except Exception as e:
            messages.error(request, f'No se puede eliminar. Hay productos asociados. Error: {str(e)}')
        return redirect('categoria_web_lista')
    
    context = {'categoria': categoria}
    return render(request, 'templateCatalogo/categoria_web_eliminar.html', context)


# ==================== CRUD PRODUCTO WEB ====================

@login_required
def producto_web_lista(request):
    """Vista para listar todos los productos web"""
    productos = Producto.objects.all().select_related('categoria', 'servicio').order_by('nombre')
    context = {'productos': productos}
    return render(request, 'templateCatalogo/producto_web_lista.html', context)


@login_required
def producto_web_crear(request):
    """Vista para crear un nuevo producto web"""
    if request.method == 'POST':
        form = ProductoWebForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto web creado exitosamente.')
            return redirect('producto_web_lista')
    else:
        form = ProductoWebForm()
    
    context = {'form': form, 'accion': 'Crear'}
    return render(request, 'templateCatalogo/producto_web_form.html', context)


@login_required
def producto_web_editar(request, pk):
    """Vista para editar un producto web existente"""
    producto = get_object_or_404(Producto, pk=pk)
    
    if request.method == 'POST':
        form = ProductoWebForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto web actualizado exitosamente.')
            return redirect('producto_web_lista')
    else:
        form = ProductoWebForm(instance=producto)
    
    context = {'form': form, 'accion': 'Editar', 'producto': producto}
    return render(request, 'templateCatalogo/producto_web_form.html', context)


@login_required
def producto_web_eliminar(request, pk):
    """Vista para eliminar un producto web"""
    producto = get_object_or_404(Producto, pk=pk)
    
    if request.method == 'POST':
        try:
            producto.delete()
            messages.success(request, 'Producto web eliminado exitosamente.')
        except Exception as e:
            messages.error(request, f'No se puede eliminar. Error: {str(e)}')
        return redirect('producto_web_lista')
    
    context = {'producto': producto}
    return render(request, 'templateCatalogo/producto_web_eliminar.html', context)