from django import forms
from .models import Empleado


class EmpleadoForm(forms.ModelForm):

    class Meta:
        
        
        
        model = Empleado

        fields = [
            'nombre',
            'documento',
            'fecha_nacimiento',
            'cargo',
            'telefono',
            'email',
            'rh',
            'skills',
            'activo',
            'avatar',
        ]

        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo'
            }),

            'documento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Documento'
            }),

            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),

            'cargo': forms.Select(attrs={
                'class': 'form-select'
            }),

            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Teléfono'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@empresa.com'
            }),

            'rh': forms.Select(attrs={
                'class': 'form-select'
            }),

            'skills': forms.SelectMultiple(attrs={
                'class': 'form-select'
            }),

            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),

            'avatar': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }
        
        
        
    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']

        if len(nombre) < 5:
            raise forms.ValidationError(
                "El nombre debe tener al menos 5 caracteres."
            )

        return nombre    