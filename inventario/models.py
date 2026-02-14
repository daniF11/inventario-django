from django.db import models
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.conf import settings

# Create your models here.

#MODELO CATEGORIA

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre
    
    
#MODELO MATERIAL

class Material(models.Model):
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='materiales'
    )
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    unidad = models.CharField(max_length=50)
    stock = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)
    stock_minimo = models.PositiveIntegerField(default=5)

    def __str__(self):
        return f"{self.nombre} ({self.stock} {self.unidad})"
    
    @property
    def stock_bajo(self):
        return self.stock <= self.stock_minimo

    
    
#MODELO MOVIMIENTO

class Movimiento(models.Model):
    ENTRADA = 'ENTRADA'
    SALIDA = 'SALIDA'
    TIPO_CHOICES = (
        ('ENTRADA', 'Entrada'),
        ('SALIDA', 'Salida'),
    )

    material = models.ForeignKey(
        Material,
        on_delete=models.PROTECT,
        related_name='movimientos'
    )
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    cantidad = models.PositiveIntegerField()
    motivo = models.CharField(max_length=200)
    stock_resultante = models.PositiveIntegerField(default=0, editable=False)
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='movimientos',
        editable=False
    )

    def __str__(self):
        return f"{self.tipo} - {self.material.nombre} - {self.cantidad}"

    def clean(self):
        if not self.motivo or len(self.motivo.strip()) < 5:
            raise ValidationError(
                'El motivo debe tener al menos 5 caracteres.'
        )

        if self.tipo == 'SALIDA' and self.cantidad > self.material.stock:
            raise ValidationError(
                f'Stock insuficiente. Disponible: {self.material.stock}'
        )

    def save(self, *args, **kwargs):
        is_new = self.pk is None  # 👈 clave

        with transaction.atomic():
            self.clean()

        # Primero guarda el movimiento
        super().save(*args, **kwargs)

        # SOLO si es nuevo, impacta stock
        if is_new:
            if self.tipo == self.ENTRADA:
                self.material.stock += self.cantidad
            elif self.tipo == self.SALIDA:
                self.material.stock -= self.cantidad

            self.material.save()

            # Actualiza stock resultante
            self.stock_resultante = self.material.stock
            super().save(update_fields=['stock_resultante'])


        
