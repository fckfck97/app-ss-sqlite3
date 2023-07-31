from django import forms
from .models import Voter, VotingPoint
from django_select2.forms import Select2Widget
from .queartes import QUARTERS

DEFAULT_ATTRS = {
    'autocomplete': 'off',
    'class': 'max-w-lg block w-full shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:max-w-xs sm:text-sm border-gray-300 rounded-md'
}

def create_charfield(name, placeholder, min_length=None, max_length=None):
    return forms.CharField(
        min_length=min_length,
        max_length=max_length,
        widget=forms.TextInput(attrs={
            **DEFAULT_ATTRS, 'placeholder': placeholder
        }),
        required=True
    )

class VotersForm(forms.ModelForm):
    DOCUMENT_TYPES = [
        ('','Selecciona un tipo de documento'),
        ('CC','CEDULA DE CIUDADANIA'),
        ('CE','CEDULA DE EXTRANJERIA'),
    ]

    typeDocument = forms.ChoiceField(choices=DOCUMENT_TYPES, widget=forms.Select(attrs=DEFAULT_ATTRS), required=True) 

    nuip = create_charfield('nuip', 'Ingrese el numero de identidad', min_length=7, max_length=10)

    fullName = create_charfield('fullName', 'Ingrese el nombre completo')

    quarter = forms.ChoiceField(choices=QUARTERS, widget=forms.Select(attrs=DEFAULT_ATTRS), required=True) 

    address = forms.CharField(widget=forms.TextInput(attrs={**DEFAULT_ATTRS, 'placeholder': 'Direccion (Opcional)'}), max_length=150, required=False)
    
    numberPhone = create_charfield('numberPhone', '3111234567', min_length=10, max_length=10)

    votingPoint = forms.ModelChoiceField(queryset=VotingPoint.objects.all(),empty_label="Selecciona un punto de votación", widget=Select2Widget(attrs=DEFAULT_ATTRS),required=True)  

    email = forms.EmailField(widget=forms.EmailInput(attrs={**DEFAULT_ATTRS, 'placeholder': 'Ingrese el correo electrónico'}), required=True)

    def clean(self):
        cleaned_data = super().clean()

        typeDocument = cleaned_data.get('typeDocument')
        if typeDocument not in [doc_type[0] for doc_type in self.DOCUMENT_TYPES[1:]]: 
            self.add_error('typeDocument', "Por favor selecciona un tipo de documento valido.")
            
        nuip = cleaned_data.get('nuip')
        if nuip and (not nuip.isdigit() or len(nuip) < 7 or len(nuip) > 10):
            self.add_error('nuip', "El Numero de identidad debe contener únicamente dígitos numéricos y tener un mínimo de 7 y un máximo de 10 dígitos.")
        
        numberPhone = cleaned_data.get('numberPhone')
        if numberPhone and (len(str(numberPhone)) != 10 or not str(numberPhone).startswith('3')):
            self.add_error('numberPhone', "El número de telefono debe tener 10 digitos y comenzar con 3")
        
        address = cleaned_data.get('address')
        if address and len(address) > 150: 
            self.add_error('address', "La dirección debe tener un máximo de 150 caracteres.")

    class Meta:
        model = Voter
        fields = ['typeDocument', 'nuip', 'fullName', 'quarter', 'votingPoint', 'numberPhone', 'email', 'address']