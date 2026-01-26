from django.contrib import admin
from .models import Categoria, Material, Movimiento

# Register your models here.

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)
    
    
@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'get_categoria', 'stock', 'unidad', 'activo')
    list_filter = ('activo',)
    search_fields = ('nombre',)
    list_editable = ('stock', 'activo')

    def get_categoria(self, obj):
        return obj.categoria.nombre
    get_categoria.short_description = 'Categoría'

    
    
@admin.register(Movimiento)
class MovimientoAdmin(admin.ModelAdmin):
    list_display = ('material', 'tipo', 'cantidad', 'fecha')
    list_filter = ('tipo', 'fecha')
    search_fields = ('material__nombre',)