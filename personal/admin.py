from django.contrib import admin
from .models import Empleado, Cargo, Skill


@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "documento", "cargo", "activo")
    list_filter = ("activo", "cargo", "skills")
    search_fields = ("nombre", "documento", "email")


admin.site.register(Cargo)
admin.site.register(Skill)