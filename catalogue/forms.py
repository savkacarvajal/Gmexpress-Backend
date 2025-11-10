from django import forms
from django.core.exceptions import ValidationError
from .models import Categoria, Producto

class CategoriaForm(forms.ModelForm):
    """
    Formulario para crear y editar categorías de productos.
    Incluye validación para evitar nombres duplicados.
    """
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion', 'estado']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Almuerzos, Bebidas, Repostería'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción de la categoría',
                'rows': 3
            }),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'nombre': 'Nombre de la Categoría',
            'descripcion': 'Descripción',
            'estado': 'Estado',
        }
    
    def clean_nombre(self):
        """Valida que el nombre de categoría no esté duplicado"""
        nombre = self.cleaned_data.get('nombre')
        
        # Si estamos editando, excluir el registro actual
        if self.instance.pk:
            if Categoria.objects.filter(nombre__iexact=nombre).exclude(pk=self.instance.pk).exists():
                raise ValidationError('Ya existe una categoría con este nombre.')
        else:
            if Categoria.objects.filter(nombre__iexact=nombre).exists():
                raise ValidationError('Ya existe una categoría con este nombre.')
        
        return nombre


class ProductoForm(forms.ModelForm):
    """
    Formulario para crear y editar productos del catálogo.
    Incluye validaciones de negocio:
    - Precio mayor a 0
    - Stock no negativo
    - Categoría activa
    """
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'imagen', 'categoria_id', 'categoria_web_id', 'servicio_id']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del producto'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción del producto',
                'rows': 3
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Precio en pesos chilenos',
                'min': 1
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cantidad disponible',
                'min': 0
            }),
            'imagen': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'categoria_id': forms.Select(attrs={'class': 'form-control'}),
            'categoria_web_id': forms.Select(attrs={'class': 'form-control'}),
            'servicio_id': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'nombre': 'Nombre del Producto',
            'descripcion': 'Descripción',
            'precio': 'Precio (CLP)',
            'stock': 'Stock Disponible',
            'imagen': 'Imagen del Producto',
            'categoria_id': 'Categoría Inventario',
            'categoria_web_id': 'Categoría Web (Catálogo)',
            'servicio_id': 'Servicio',
        }
    
    def __init__(self, *args, **kwargs):
        """Inicializa el formulario con categorías activas y servicios"""
        super().__init__(*args, **kwargs)
        
        # Filtrar solo categorías de inventario activas
        self.fields['categoria_id'].queryset = Categoria.objects.filter(estado='1').order_by('nombre')
        self.fields['categoria_id'].empty_label = "Seleccione categoría inventario"
        self.fields['categoria_id'].required = True
        
        # Importar modelos de catalogo
        from catalogo.models import Servicio, Categoria as CategoriaWeb
        
        # Filtrar categorías web activas
        self.fields['categoria_web_id'].queryset = CategoriaWeb.objects.filter(estado='1').order_by('nombre')
        self.fields['categoria_web_id'].empty_label = "Seleccione categoría web (opcional)"
        self.fields['categoria_web_id'].required = False
        
        # Filtrar servicios activos
        self.fields['servicio_id'].queryset = Servicio.objects.filter(estado='1').order_by('nombre')
        self.fields['servicio_id'].empty_label = "Seleccione un servicio (opcional)"
        self.fields['servicio_id'].required = False
    
    def clean_precio(self):
        """Valida que el precio sea mayor a 0"""
        precio = self.cleaned_data.get('precio')
        
        if precio <= 0:
            raise ValidationError('El precio debe ser mayor a 0.')
        
        if precio > 10000000:
            raise ValidationError('El precio no puede ser mayor a $10.000.000.')
        
        return precio
    
    def clean_stock(self):
        """Valida que el stock no sea negativo"""
        stock = self.cleaned_data.get('stock')
        
        if stock < 0:
            raise ValidationError('El stock no puede ser negativo.')
        
        return stock
    
    def clean_nombre(self):
        """Valida que el nombre del producto no esté duplicado en la misma categoría"""
        nombre = self.cleaned_data.get('nombre')
        
        # Validar duplicados
        if self.instance.pk:
            if Producto.objects.filter(nombre__iexact=nombre).exclude(pk=self.instance.pk).exists():
                raise ValidationError('Ya existe un producto con este nombre.')
        else:
            if Producto.objects.filter(nombre__iexact=nombre).exists():
                raise ValidationError('Ya existe un producto con este nombre.')
        
        return nombre
