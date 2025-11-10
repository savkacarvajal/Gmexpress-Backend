#!/usr/bin/env python
"""
Script para verificar y poblar datos en la base de datos
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmexpress.settings')
django.setup()

from catalogo.models import Servicio, Categoria as CategoriaWeb, Producto as ProductoWeb
from catalogue.models import Categoria, Producto
from usuarios.models import Usuario, TipoUsuario
from ventas.models import Venta, DetalleVenta

def verificar_y_crear_datos():
    """Verificar y crear datos necesarios"""
    
    print("=" * 60)
    print("VERIFICACIÓN DE BASE DE DATOS GM-EXPRESS")
    print("=" * 60)
    
    # ===== USUARIOS =====
    print("\n📋 USUARIOS:")
    print(f"  Total usuarios: {Usuario.objects.count()}")
    print(f"  Usuarios activos: {Usuario.objects.filter(estado='1').count()}")
    
    print("\n📋 TIPOS DE USUARIO:")
    tipos_count = TipoUsuario.objects.count()
    print(f"  Total tipos: {tipos_count}")
    if tipos_count == 0:
        print("  ⚠️  Creando tipos de usuario...")
        TipoUsuario.objects.create(descripcion='Administrador', estado='1')
        TipoUsuario.objects.create(descripcion='Cliente', estado='1')
        TipoUsuario.objects.create(descripcion='Empleado', estado='1')
        print("  ✅ Tipos de usuario creados")
    
    # ===== CATALOGUE (Inventario) =====
    print("\n📦 CATEGORÍAS (Inventario - catalogue):")
    categorias_count = Categoria.objects.count()
    categorias_activas = Categoria.objects.filter(estado='1').count()
    print(f"  Total: {categorias_count} | Activas: {categorias_activas}")
    
    if categorias_count == 0:
        print("  ⚠️  Creando categorías de inventario...")
        categorias_inventario = [
            {'nombre': 'Almuerzos', 'descripcion': 'Platos de almuerzo variados', 'estado': '1'},
            {'nombre': 'Bebidas', 'descripcion': 'Bebidas frías y calientes', 'estado': '1'},
            {'nombre': 'Desayunos', 'descripcion': 'Opciones para el desayuno', 'estado': '1'},
            {'nombre': 'Repostería', 'descripcion': 'Pasteles, tortas y postres', 'estado': '1'},
            {'nombre': 'Snacks', 'descripcion': 'Aperitivos y bocadillos', 'estado': '1'},
            {'nombre': 'Veganos', 'descripcion': 'Productos 100% vegetales', 'estado': '1'},
            {'nombre': 'Vegetarianos', 'descripcion': 'Productos sin carne', 'estado': '1'},
        ]
        for cat_data in categorias_inventario:
            Categoria.objects.create(**cat_data)
        print(f"  ✅ {len(categorias_inventario)} categorías creadas")
    else:
        print("  Categorías existentes:")
        for cat in Categoria.objects.filter(estado='1')[:5]:
            print(f"    - {cat.nombre}")
    
    print(f"\n📦 PRODUCTOS (Inventario - catalogue):")
    productos_count = Producto.objects.count()
    print(f"  Total: {productos_count}")
    
    # ===== CATALOGO WEB =====
    print("\n🌐 SERVICIOS (Catálogo Web):")
    servicios_count = Servicio.objects.count()
    servicios_activos = Servicio.objects.filter(estado='1').count()
    print(f"  Total: {servicios_count} | Activos: {servicios_activos}")
    
    if servicios_count == 0:
        print("  ⚠️  NO HAY SERVICIOS. Ejecuta: python poblar_servicios.py")
    else:
        print("  Servicios existentes:")
        for serv in Servicio.objects.filter(estado='1')[:5]:
            print(f"    - {serv.nombre} ({serv.servicio_tipo})")
    
    print("\n🌐 CATEGORÍAS WEB (Catálogo Web):")
    categorias_web_count = CategoriaWeb.objects.count()
    categorias_web_activas = CategoriaWeb.objects.filter(estado='1').count()
    print(f"  Total: {categorias_web_count} | Activas: {categorias_web_activas}")
    
    if categorias_web_count == 0:
        print("  ⚠️  Creando categorías web...")
        categorias_web = [
            {'nombre': 'Almuerzo ratas', 'descripcion': 'Almuerzos económicos', 'estado': '1'},
            {'nombre': 'Almuerzo Friki', 'descripcion': 'Almuerzos especiales', 'estado': '1'},
            {'nombre': 'Servicios de Personal', 'descripcion': 'Servicios personalizados', 'estado': '1'},
            {'nombre': 'Menús Ejecutivos', 'descripcion': 'Menús corporativos', 'estado': '1'},
            {'nombre': 'Cenas', 'descripcion': 'Opciones para la cena', 'estado': '1'},
        ]
        for cat_data in categorias_web:
            CategoriaWeb.objects.create(**cat_data)
        print(f"  ✅ {len(categorias_web)} categorías web creadas")
    else:
        print("  Categorías web existentes:")
        for cat in CategoriaWeb.objects.filter(estado='1')[:5]:
            print(f"    - {cat.nombre}")
    
    print("\n🌐 PRODUCTOS WEB (Catálogo Web):")
    productos_web_count = ProductoWeb.objects.count()
    print(f"  Total: {productos_web_count}")
    
    # ===== VENTAS =====
    print("\n💰 VENTAS:")
    ventas_count = Venta.objects.count()
    print(f"  Total ventas: {ventas_count}")
    print(f"  Detalles de venta: {DetalleVenta.objects.count()}")
    
    print("\n" + "=" * 60)
    print("RESUMEN:")
    print("=" * 60)
    print(f"✅ Usuarios: {Usuario.objects.count()}")
    print(f"✅ Tipos Usuario: {TipoUsuario.objects.count()}")
    print(f"✅ Categorías Inventario: {Categoria.objects.filter(estado='1').count()}")
    print(f"✅ Productos Inventario: {Producto.objects.count()}")
    print(f"✅ Servicios: {Servicio.objects.filter(estado='1').count()}")
    print(f"✅ Categorías Web: {CategoriaWeb.objects.filter(estado='1').count()}")
    print(f"✅ Productos Web: {ProductoWeb.objects.count()}")
    print(f"✅ Ventas: {Venta.objects.count()}")
    print("=" * 60)

if __name__ == '__main__':
    verificar_y_crear_datos()
