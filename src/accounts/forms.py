from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistroForm(UserCreationForm):
    # Agregamos los campos que pide tu diagrama
    first_name = forms.CharField(max_length=30, required=True, label="Nombre")
    last_name = forms.CharField(max_length=30, required=True, label="Apellido")
    email = forms.EmailField(required=True, label="Correo Electrónico")

    class Meta:
        model = User
        # El orden en que aparecerán en el formulario HTML
        fields = ['username', 'first_name', 'last_name', 'email']