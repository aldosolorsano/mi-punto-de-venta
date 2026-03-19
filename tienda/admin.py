from django.contrib import admin
from .models import Categoria, Producto, IngresoMercancia, DetalleIngreso, Venta, DetalleVenta

# Registramos la categoría de forma sencilla
admin.site.register(Categoria)

# Personalizamos cómo se ven los productos en la lista
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('codigo_barras', 'nombre', 'categoria', 'precio_compra', 'precio_venta', 'stock')
    search_fields = ('codigo_barras', 'nombre')
    list_filter = ('categoria',)

# ==========================================
# CONFIGURACIÓN PARA EL INGRESO DE MERCANCÍA
# ==========================================
class DetalleIngresoInline(admin.TabularInline):
    model = DetalleIngreso
    extra = 1  # Filas en blanco que aparecen por defecto

@admin.register(IngresoMercancia)
class IngresoMercanciaAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha', 'proveedor', 'total')
    inlines = [DetalleIngresoInline]

# ==========================================
# CONFIGURACIÓN PARA VENTAS (Opcional en admin, 
# pero útil para ver el historial)
# ==========================================
class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 0

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha', 'total')
    inlines = [DetalleVentaInline]