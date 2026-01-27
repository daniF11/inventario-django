from django import forms
from .models import Movimiento, Material

class MovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = ['material', 'tipo', 'cantidad']

    def clean(self):
        cleaned_data = super().clean()
        material = cleaned_data.get('material')
        tipo = cleaned_data.get('tipo')
        cantidad = cleaned_data.get('cantidad')

        if not material or not cantidad:
            return cleaned_data

        if tipo == Movimiento.SALIDA and cantidad > material.stock:
            raise forms.ValidationError("Stock insuficiente.")


            if cantidad > material.stock:
                raise forms.ValidationError(
                    f"Stock insuficiente. Disponible: {material.stock}"
                )

        return cleaned_data

