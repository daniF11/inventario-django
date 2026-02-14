from django import forms
from .models import Movimiento, Material

class MovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = ['material', 'tipo', 'cantidad', 'motivo']
        widgets = {
            'material': forms.Select(attrs={'class': 'form-select'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'motivo': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def save(self, user=None, commit=True):
        movimiento = super().save(commit=False)

        if user is not None:
            movimiento.usuario = user

        if commit:
            movimiento.save()

        return movimiento


