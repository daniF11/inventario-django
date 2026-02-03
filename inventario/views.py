from django.shortcuts import render, redirect
from .models import Material, Categoria
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView
from .models import Material, Movimiento
from .forms import MovimientoForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin


# Create your views here.
@login_required
def dashboard(request):
    context = {
        'total_materiales': Material.objects.count(),
        'materiales_activos': Material.objects.filter(activo=True).count(),
        'total_movimientos': Movimiento.objects.count(),
        'ultimos_movimientos': Movimiento.objects.select_related('material')
                                .order_by('-fecha')[:5],
    }
    return render(request, 'inventario/dashboard.html', context)


@login_required(login_url='usuarios:login')
def material_list(request):
    materiales = Material.objects.filter(activo=True)
    return render(request, 'inventario/material_list.html', {
        'materiales': materiales})


@login_required(login_url='usuarios:login')
def material_create(request):
    categoria = Categoria.objects.all()
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        categoria_id = request.POST.get('categoria')
        unidad = request.POST.get('unidad')
        
        categoria = Categoria.objects.get(id=categoria_id)
        
        Material.objects.create(
            nombre=nombre,
            categoria=categoria,
            unidad=unidad,
            stock=0
        )
        return redirect('inventario:material_list')
    
    return render(request, 'inventario/material_form.html', {
        'categorias': categoria
    })
    
    
@login_required(login_url='usuarios:login')    
def material_update(request, pk):
    material = Material.objects.get(pk=pk)
    categoria = Categoria.objects.all()
    
    if request.method == 'POST':
        material.nombre = request.POST.get('nombre')
        categoria_id = request.POST.get('categoria')
        material.unidad = request.POST.get('unidad')
        
        material.categoria = Categoria.objects.get(id=categoria_id)
        material.save()
        
        return redirect('inventario:material_list')
    
    return render(request, 'inventario/material_form.html', {
        'material': material,
        'categorias': categoria
    })
    
@login_required(login_url='usuarios:login')
def material_toggle(request, pk):
    material = Material.objects.get(pk=pk)
    material.activo = not material.activo
    material.save()
    return redirect('inventario:material_list')




class MovimientoCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView
):
    model = Movimiento
    form_class = MovimientoForm
    template_name = 'inventario/movimiento_form.html'
    permission_required = 'inventario.add_movimiento'
    login_url = 'usuarios:login'
    
    
class MovimientoListView(LoginRequiredMixin, ListView):
    model = Movimiento
    template_name = 'inventario/movimiento_list.html'
    context_object_name = 'movimientos'
    ordering = ['-fecha']
    paginate_by = 20
    
    
    
    
class MaterialListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView
):
    model = Material
    template_name = 'inventario/material_list.html'
    permission_required = 'inventario.view_material'
    login_url = 'usuarios:login'


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'inventario/dashboard.html'
    login_url = 'usuarios:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['total_materiales'] = Material.objects.count()
        context['materiales_activos'] = Material.objects.filter(activo=True).count()
        context['total_movimientos'] = Movimiento.objects.count()
        context['ultimos_movimientos'] = Movimiento.objects.order_by('-fecha')[:5]

        return context

