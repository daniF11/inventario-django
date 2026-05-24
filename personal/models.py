from django.db import models
from django.db import models
from django.core.validators import RegexValidator


class Cargo(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Skill(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Habilidad"
        verbose_name_plural = "Habilidades"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Empleado(models.Model):
    RH_CHOICES = [
        ('O+', 'O+'), ('O-', 'O-'),
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
    ]

    documento_validator = RegexValidator(
        regex=r'^\d+$',
        message="El documento solo debe contener números"
    )

    nombre = models.CharField(max_length=150)
    documento = models.CharField(
        max_length=20,
        unique=True,
        validators=[documento_validator]
    )
    fecha_nacimiento = models.DateField()
    cargo = models.ForeignKey(
        Cargo,
        on_delete=models.SET_NULL,
        null=True,
        related_name="empleados"
    )
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(unique=True)
    rh = models.CharField(max_length=3, choices=RH_CHOICES)

    skills = models.ManyToManyField(
        Skill,
        blank=True,
        related_name="empleados"
    )

    activo = models.BooleanField(default=True)

    avatar = models.ImageField(
        upload_to="empleados/avatars/",
        blank=True,
        null=True
    )

    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre} - {self.documento}"