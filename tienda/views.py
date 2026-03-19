from django.shortcuts import render
from .models import Producto
import json
from django.http import JsonResponse
from .models import Producto, Venta, DetalleVenta

def punto_de_venta(request):
    # Traemos todos los productos que tengan stock mayor a 0
    productos = Producto.objects.filter(stock__gt=0)
    return render(request, 'pos.html', {'productos': productos})

def procesar_venta(request):
    if request.method == 'POST':
        try:
            # Recibimos los datos del carrito desde JavaScript
            data = json.loads(request.body)
            carrito = data.get('carrito', [])

            if not carrito:
                return JsonResponse({'error': 'El carrito está vacío'}, status=400)

            # 1. Creamos el registro de la Venta general
            total_venta = sum(float(item['precio']) * int(item['cantidad']) for item in carrito)
            venta = Venta.objects.create(total=total_venta)

            # 2. Creamos los Detalles de la Venta (productos)
            for item in carrito:
                producto = Producto.objects.get(id=item['id'])
                cantidad = int(item['cantidad'])
                precio = float(item['precio'])
                
                # Al crear el detalle, nuestro models.py restará el stock automáticamente
                DetalleVenta.objects.create(
                    venta=venta, 
                    producto=producto, 
                    cantidad=cantidad, 
                    precio_unitario=precio
                )

            return JsonResponse({'success': True, 'mensaje': 'Venta exitosa'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            
    return JsonResponse({'error': 'Método no permitido'}, status=405)