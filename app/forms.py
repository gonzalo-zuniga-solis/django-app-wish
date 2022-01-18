from cProfile import label
from dataclasses import field
from tkinter import Widget
from tkinter.ttk import LabeledScale
from django import forms
from django.db.models import fields
from app.models import User, Deseo
from django.core.exceptions import ValidationError

# from deseos.app.models import Deseo

class UserForm(forms.ModelForm):
    def clean_name(self):
        data = self.cleaned_data['name']
        if len(data) < 3:
            raise ValidationError("El campo 'Nombre' debe tener al menos 3 caracteres")
        return data

    def clean_password(self):
        data = self.cleaned_data['password']
        if len(data) < 8:
            raise ValidationError("El campo 'Contraseña' debe tener al menos 8 caracteres")
        return data

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "La contraseña y la confirmación de la contraseña no coinciden"
            )

    class Meta:
        model = User
        fields = ['name', 'username','password', 'confirm_password']
        labels = {
            'name': 'Nombre',
            'username': 'Username',
            'password': 'Contraseña',
            'confirm_password': 'Confirmar contraseña'
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'confirm_password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class LoginForm(forms.ModelForm):
    def clean_item(self):
        data = self.cleaned_data['item']
        if len(data) < 3:
            raise ValidationError("El campo 'Contraseña' debe tener al menos 3 caracteres")
        return data
    
    class Meta:
        model = User
        fields = ['username', 'password']
        labels = {
            'username': 'Username',
            'password': 'Contraseña',
        }
        
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class DeseoForm(forms.ModelForm):
    class Meta:
        model = Deseo
        fields = ['item']
        labels = {
            'item': 'Ítem',
        }

        widgets = {
            'item': forms.TextInput(attrs={'class': 'form-control'}),
        }