from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from .models import Empleado
from .forms import EmpleadoForm


class EmpleadoListView(ListView):
    model = Empleado
    template_name = 'personal/empleado_list.html'
    context_object_name = 'empleados'


class EmpleadoCreateView(CreateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'personal/empleado_form.html'
    success_url = reverse_lazy('empleado_list')
