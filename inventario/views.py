from urllib import request
from django.shortcuts import render, redirect

from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView
from .models import Material, Movimiento, Categoria
from .forms import MovimientoForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import F


# Create your views here.
@login_required
def dashboard(request):
    

    context = {
        'total_materiales': Material.objects.count(),
        'materiales_activos': Material.objects.filter(activo=True).count(),
        'total_movimientos': Movimiento.objects.count(),
        'ultimos_movimientos': Movimiento.objects.select_related('material')
                                .order_by('-fecha')[:5],
        'materiales_bajo_stock': Material.objects.filter(
            activo=True,
            stock__lte=F('stock_minimo'))    
    }
    
    
    return render(request, 'inventario/dashboard.html', context)


@login_required(login_url='usuarios:login')
def material_list(request):
    materiales = Material.objects.filter(activo=True)
    return render(request, 'inventario/material_list.html', {
        'materiales': materiales})


@permission_required('inventario.add_material', raise_exception=True)
def material_create(request):
    categorias = Categoria.objects.all()
    
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
        'categorias': categorias
    })
    
    
@permission_required('inventario.change_material', raise_exception=True)   
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
    
@permission_required('inventario.change_material', raise_exception=True)
def material_toggle(request, pk):
    material = Material.objects.get(pk=pk)
    material.activo = not material.activo
    material.save()
    return redirect('inventario:material_list')




class MovimientoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Movimiento
    form_class = MovimientoForm
    template_name = 'inventario/movimiento_form.html'
    success_url = reverse_lazy('inventario:movimiento_list')
    permission_required = 'inventario.add_movimiento'

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)




    
    
class MovimientoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Movimiento
    template_name = 'inventario/movimiento_list.html'
    context_object_name = 'movimientos'
    ordering = ['-fecha']
    paginate_by = 20
    permission_required = 'inventario.view_movimiento'
    
    
    
    
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
    permission_required = 'inventario.view_dashboard'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['total_materiales'] = Material.objects.count()
        context['materiales_activos'] = Material.objects.filter(activo=True).count()
        context['total_movimientos'] = Movimiento.objects.count()
        context['ultimos_movimientos'] = Movimiento.objects.order_by('-fecha')[:5]

        return context


