from django.shortcuts import render, redirect
from .models import Material, Categoria
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from .models import Movimiento
from .forms import MovimientoForm
from django.urls import reverse_lazy

# Create your views here.

def material_list(request):
    materiales = Material.objects.filter(activo=True)
    return render(request, 'inventario/material_list.html', {
        'materiales': materiales})
    
    
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
    

def material_toggle(request, pk):
    material = Material.objects.get(pk=pk)
    material.activo = not material.activo
    material.save()
    return redirect('inventario:material_list')




class MovimientoCreateView(CreateView):
    model = Movimiento
    form_class = MovimientoForm
    template_name = 'inventario/movimiento_form.html'
    success_url = reverse_lazy('inventario:movimiento_list')
    
    
class MovimientoListView(ListView):
    model = Movimiento
    template_name = 'inventario/movimiento_list.html'
    context_object_name = 'movimientos'
    ordering = ['-fecha']
    paginate_by = 20


