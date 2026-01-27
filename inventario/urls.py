from django.urls import path
from . import views
from .views import MovimientoCreateView, MovimientoListView

app_name = 'inventario'

urlpatterns = [
    path('materiales/', views.material_list, name='material_list'),
    path('materiales/nuevo/', views.material_create, name='material_create'),
    path('materiales/editar/<int:pk>/', views.material_update, name='material_update'),
    path('materiales/toggle/<int:pk>/', views.material_toggle, name='material_toggle'),
    path('movimientos/', MovimientoListView.as_view(), name='movimiento_list'),
    path('movimientos/nuevo/', MovimientoCreateView.as_view(), name='movimiento_create'),
    
]