from django.contrib.auth import views as auth_views
from django.urls import path
from . import views



urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('producto_list/', views.producto_list, name='producto_list'),
    path('añadir_al_carrito/<int:producto_id>/', views.añadir_al_carrito, name='añadir_al_carrito'),
    
    # Otras URLs...
]