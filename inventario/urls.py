from django.urls import path
from . import views
from .views import MovimientoCreateView, MovimientoListView, DashboardView
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from inventario.views import dashboard

app_name = 'inventario'

urlpatterns = [
    path('', login_required(dashboard), name='dashboard'),
    path('materiales/', views.material_list, name='material_list'),
    path('materiales/nuevo/', views.material_create, name='material_create'),
    path('materiales/editar/<int:pk>/', views.material_update, name='material_update'),
    path('materiales/toggle/<int:pk>/', views.material_toggle, name='material_toggle'),
    path('movimientos/', MovimientoListView.as_view(), name='movimiento_list'),
    path('movimientos/nuevo/', MovimientoCreateView.as_view(), name='movimiento_create'),
    # path('', views.dashboard, name='dashboard'),
    
]