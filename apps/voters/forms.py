from django import forms
from django.core.exceptions import ValidationError
from .models import Voter, VotingPoint
from django_select2.forms import Select2Widget

class VotersForm(forms.ModelForm):
    nuip = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Ingrese su Cedula',
            'autocomplete':'off',
            'class':'max-w-lg block w-full shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:max-w-xs sm:text-sm border-gray-300 rounded-md'
            }),
        required=True)
    fullName = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Ingrese el Nombre completo',
            'autocomplete':'off',
            'class':'max-w-lg block w-full shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:max-w-xs sm:text-sm border-gray-300 rounded-md'
            }),
        required=True)
    quarter = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Ingrese el Barrio',
            'autocomplete':'off',
            'class':'max-w-lg block w-full shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:max-w-xs sm:text-sm border-gray-300 rounded-md'
            }),
        required=True)
    votingPoint = forms.ModelChoiceField(
        queryset=VotingPoint.objects.all(),
        empty_label="Selecciona un punto de votación",
        widget=Select2Widget(attrs={
            'autocomplete':'off',
            'class':'max-w-lg block w-full shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:max-w-xs sm:text-sm border-gray-300 rounded-md'
        }),
        required=True
    )
    numberPhone = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': '3111234567',
            'autocomplete':'off',
            'class':'max-w-lg block w-full shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:max-w-xs sm:text-sm border-gray-300 rounded-md'
            }),
        required=True)
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Ingrese el Correo Electrónico',
            'autocomplete':'off',
            'class':'max-w-lg block w-full shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:max-w-xs sm:text-sm border-gray-300 rounded-md'
            }),
        required=True)

    def clean_nuip(self):
        nuip = self.cleaned_data.get('nuip')
        if len(nuip) < 7 or len(nuip) > 10:
            raise ValidationError("La Cedula debe tener un mínimo de 7 y un máximo de 10 dígitos.")
        return nuip

    def clean_numberPhone(self):
        numberPhone = self.cleaned_data.get('numberPhone')
        if len(str(numberPhone)) != 10 or not str(numberPhone).startswith('3'):
            raise ValidationError("El número de telefono debe tener 10 digitos y comenzar con 3")
        return numberPhone

    class Meta:
        model = Voter
        fields = ['nuip', 'fullName', 'quarter', 'votingPoint', 'numberPhone', 'email']