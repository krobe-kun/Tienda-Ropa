from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Producto

@login_required
def inicio(request):
    return render(request, 'tienda/inicio.html')

def register_view(request):
    return render(request, 'tienda/register.html')  

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render('producto_list')  # Redirige a la página de inicio tras el login
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'tienda/login.html')

def logout_view(request):
    logout(request)
    return redirect('inicio')  # Redirige a la página de inicio tras el logout

# ------------------------------------------
# VISTAS RELACIONADAS CON PRODUCTOS
# ------------------------------------------

def producto_list(request):
    # Obtener todos los productos
    productos = Producto.objects.all()
    return render(request, 'tienda/producto_list.html', {'productos': productos})

def añadir_al_carrito(request, producto_id):
    # Aquí puedes agregar lógica para añadir el producto al carrito (esto es solo un ejemplo)
    producto = Producto.objects.get(id=producto_id)
    # Podrías almacenar el producto en la sesión, por ejemplo:
    carrito = request.session.get('carrito', [])
    carrito.append(producto.id)
    request.session['carrito'] = carrito
    return redirect('producto_list')  # Redirige a la lista de productos

# ------------------------------------------
# VISTAS RELACIONADAS CON EL CARRITO DE COMPRAS
# ------------------------------------------

def agregar_al_carrito(request, producto_id):
    """
    Agrega un producto al carrito de compras.
    """
    carrito = request.session.get('carrito', {})
    carrito[str(producto_id)] = carrito.get(str(producto_id), 0) + 1
    request.session['carrito'] = carrito
    return redirect('producto_list')

def mostrar_carrito(request):
    """
    Muestra los productos que están en el carrito.
    """
    carrito = request.session.get('carrito', {})
    productos = Producto.objects.filter(id__in=carrito.keys())
    items = [
        {
            'producto': p,
            'cantidad': carrito[str(p.id)],
            'subtotal': carrito[str(p.id)] * p.precio,
        }
        for p in productos
    ]
    total = sum(item['subtotal'] for item in items)
    return render(request, 'tienda/carrito.html', {'items': items, 'total': total})

def eliminar_del_carrito(request, producto_id):
    """
    Elimina un producto del carrito de compras.
    """
    carrito = request.session.get('carrito', {})
    if str(producto_id) in carrito:
        del carrito[str(producto_id)]
    request.session['carrito'] = carrito
    return redirect('mostrar_carrito')

def vaciar_carrito(request):
    """
    Vacía el carrito de compras.
    """
    request.session['carrito'] = {}
    return redirect('producto_list')

# ------------------------------------------
# OTRAS VISTAS (LOGIN, ADMINISTRACIÓN, ETC.)
# ------------------------------------------

def inicio(request):
    """
    Página principal de la tienda.
    """
    return render(request, 'tienda/inicio.html')
