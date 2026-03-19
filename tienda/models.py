from django.db import models
from django.db.models import F

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    codigo_barras = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=200)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.nombre} - Stock: {self.stock}"

# ==========================================
# MÓDULO DE INGRESO DE MERCANCÍA (COMPRAS)
# ==========================================
class IngresoMercancia(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    proveedor = models.CharField(max_length=200, blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Ingreso #{self.id} - {self.fecha.strftime('%d/%m/%Y')}"

class DetalleIngreso(models.Model):
    ingreso = models.ForeignKey(IngresoMercancia, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.IntegerField()
    costo_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # Al guardar el ingreso, sumamos el stock al producto
        if not self.pk: # Solo la primera vez que se crea
            Producto.objects.filter(pk=self.producto.pk).update(stock=F('stock') + self.cantidad)
        super().save(*args, **kwargs)

# ==========================================
# MÓDULO DE PUNTO DE VENTA (VENTAS)
# ==========================================
class Venta(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pago_con = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cambio = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Venta #{self.id} - Total: ${self.total}"

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # Al vender, restamos el stock del producto
        if not self.pk:
            Producto.objects.filter(pk=self.producto.pk).update(stock=F('stock') - self.cantidad)
        super().save(*args, **kwargs)