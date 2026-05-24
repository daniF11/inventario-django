from django.urls import path
from .views import (
    EmpleadoListView,
    EmpleadoCreateView,
    EmpleadoDetailView
)

urlpatterns = [
    path('', EmpleadoListView.as_view(), name='empleado_list'),
    path('nuevo/', EmpleadoCreateView.as_view(), name='empleado_create'),
    path('<int:pk>/', EmpleadoDetailView.as_view(), name='empleado_detail'),
]